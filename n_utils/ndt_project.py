from builtins import object
import sys
import inspect
from operator import attrgetter
from os import sep, path, mkdir
import re
try:
    from os import scandir
except ImportError:
    from scandir import scandir

from n_utils.git_utils import Git
from n_utils.aws_infra_util import load_parameters

class Component(object):
    subcomponent_classes = []
    def __init__(self, name, project):
        self.name = name
        self.subcomponents = []
        self.project = project
        if not self.subcomponent_classes:
            self.subcomponent_classes = [name_and_obj for name_and_obj in inspect.getmembers(sys.modules["n_utils.ndt_project"]) if name_and_obj[0].startswith("SC") and inspect.isclass(name_and_obj[1])]
    
    def get_subcomponents(self):
        if not self.subcomponents:
            self.subcomponents = sorted(self._find_subcomponents(), key=attrgetter("name"))
        return self.subcomponents
    
    def _find_subcomponents(self):
        ret = []
        for subdir in [de.name for de in scandir(self.project.root + sep + self.name) if self._is_subcomponent(de.name)]:
            for _, obj in self.subcomponent_classes:
                if obj(self, "").match_dirname(subdir):
                    if subdir == "image":
                        sc_name = ""
                    else:
                        sc_name = "-".join(subdir.split("-")[1:])
                    ret.append(obj(self, sc_name))
        return ret

    def _is_subcomponent(self, dir):
        for _, obj in self.subcomponent_classes:
            if obj(self, "").match_dirname(dir):
                return True
        return False

class SubComponent(object):
    def __init__(self, component, name):
        self.component = component
        self.name = name
        self.type = self.__class__.__name__[2:].lower()

    def get_dir(self):
        return self.component.name + sep + self.type + "-" + self.name

    def match_dirname(self, dir):
        return dir.startswith(self.type + "-")

    def list_row(self, branch):
        return ":".join([self.component.name, branch, self.type, self.name])

    def job_properties_filename(self, branch, root):
        name_arr = [self.type, re.sub(r'[^\w-]', '_', branch), self.component.name, self.name]
        return root + sep + "job-properties" + sep + "-".join(name_arr) + ".properties"

class SCImage(SubComponent):
    def get_dir(self):
        if self.name:
            return self.component.name + sep + "image-" + self.name
        else:
            return self.component.name + sep + "image"

    def match_dirname(self, dir):
        return dir == "image" or dir.startswith("image-")

    def list_row(self, branch):
        if not self.name:
            name = "-"
        else:
            name = self.name
        return ":".join([self.component.name, branch, self.type, name])

    def job_properties_filename(self, branch, root):
        name_arr = [self.type, re.sub(r'[^\w-]', '_', branch), self.component.name]
        if self.name:
            name_arr.append(self.name)
        return root + sep + "job-properties" + sep + "-".join(name_arr) + ".properties"

class SCStack(SubComponent):
    pass

class SCDocker(SubComponent):
    pass

class SCServerless(SubComponent):
    pass

class SCCDK(SubComponent):
    pass

class SCTerraform(SubComponent):
    pass



class Project(object):
    def __init__(self, root=".", branch=None):
        if not branch:
            self.branch = Git().get_current_branch()
        else:
            self.branch = branch
        self.componets = []
        self.root = root if root else guess_project_root()
        self.all_subcomponents = []

    def get_components(self):
        if not self.componets:
            self.componets = sorted(self._find_components(), key=attrgetter("name"))
        return self.componets

    def get_component(self, component):
        filtered = [c for c in self.get_components() if c.name == component]
        if len(filtered) == 1:
            return filtered[0]
        return None

    def _find_components(self):
        return [Component(de.name, self) for de in scandir(self.root) if de.is_dir() and self._is_component(de.path)]

    def get_all_subcomponents(self, sc_type=None):
        if not self.all_subcomponents:
            for component in self.get_components():
                self.all_subcomponents.extend(component.get_subcomponents())
        if not sc_type:
            return self.all_subcomponents
        else:
            return [sc for sc in self.all_subcomponents if sc.type == sc_type]

    def _is_component(self, dir):
        return len([de for de in scandir(dir) if de.is_file() and (de.name == "infra.properties" or (de.name.startswith("infra-") and de.name.endswith(".properties")))]) > 0

def guess_project_root():
    
    for guess in [".", Git().get_git_root(), "..", "../..", "../../..", "../../../.."]:
        if len(Project(root=guess).get_all_subcomponents()) > 0:
            if guess == ".":
                return guess
            else:
                return path.abspath(guess)

def list_jobs(export_job_properties=False, branch=None, json=False, component=None):
    ret = {"branches":[]}
    arr = []
    param_files = {}
    with Git() as git:
        current_project = Project(root=guess_project_root())
        if branch:
            branches = [ branch ]
        else:
            branches = git.get_branches()
        components = []
        for c_branch in branches:
            branch_obj = {"name": c_branch, "components": []}
            ret["branches"].append(branch_obj)
            if c_branch == git.get_current_branch():
                project = current_project
            else:
                root = git.export_branch(c_branch)
                project = Project(root=root, branch=c_branch)
            if component:
                c_component = project.get_component(component)
                if not c_component:
                    print("No matching components")
                    if json:
                        return {}
                    else:
                        return []
                branch_obj["components"].append({"name": c_component.name, "subcomponents": []})
                components.append(c_component)
            else:
                for c_component in project.get_components():
                    branch_obj["components"].append({"name": c_component.name, "subcomponents": []})
                    components.append(c_component)
        if not json and export_job_properties:
            try:
                mkdir(current_project.root + sep + "job-properties")
            except OSError as err:
                # Directory already exists is ok
                if err.errno == 17:
                    pass
                else:
                    raise err
        if json:
            _collect_json(components, ret, export_job_properties ,git)
        else:
            arr, param_files = _collect_prop_files(components, export_job_properties, current_project.root, git)
            if export_job_properties:
                _write_prop_files(param_files)
    if json:
        return ret
    else:
        return arr

def _collect_json(components, ret, export_job_properties, git):
    with git:
        for component in components:
            subcomponents = component.get_subcomponents()
            for subcomponent in subcomponents:
                branch_elem = [b for b in ret["branches"] if b["name"] == component.project.branch][0]
                component_elem = [c for c in branch_elem["components"] if c["name"] == component.name][0]
                subc_elem = {"type": subcomponent.type}
                if subcomponent.name:
                    subc_elem["name"] = subcomponent.name
                component_elem["subcomponents"].append(subc_elem)
                if export_job_properties:
                    prop_args = {
                        "component": subcomponent.component.name,
                        subcomponent.type: subcomponent.name,
                        "branch": component.project.branch,
                        "git": git
                    }
                    subc_elem["properties"] = load_parameters(**prop_args)

def _collect_prop_files(components, export_job_properties, root, git):
    arr = []
    param_files = {}
    with git:
        for component in components:
            subcomponents = component.get_subcomponents()
            for subcomponent in subcomponents:
                arr.append(subcomponent.list_row(component.project.branch))
                if export_job_properties:
                    #$TYPE-$GIT_BRANCH-$COMPONENT-$NAME.properties
                    filename = subcomponent.job_properties_filename(component.project.branch, root)
                    prop_args = {
                        "component": subcomponent.component.name,
                        subcomponent.type: subcomponent.name,
                        "branch": component.project.branch,
                        "git": git
                    }
                    parameters = load_parameters(**prop_args)
                    param_files[filename] = parameters
    return arr, param_files

def _write_prop_files(param_files):
    for filename, parameters in list(param_files.items()):
        with open(filename, 'w+') as prop_file:
            for key, value in list(parameters.items()):
                prop_file.write(key + "=" + value + "\n")

def list_components(branch=None, json=None):
    return [c.name for c in Project(branch=branch).get_components()]