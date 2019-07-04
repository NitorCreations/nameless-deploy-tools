#!/usr/bin/env python

# Copyright 2016-2017 Nitor Creations Oy
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from future import standard_library
standard_library.install_aliases()
from builtins import str
from builtins import range
import json
import os
import re
import subprocess
import sys
import yaml
import six
from base64 import b64encode
from collections import OrderedDict
from glob import glob
from yaml import ScalarNode, SequenceNode, MappingNode
from io import StringIO
from botocore.exceptions import ClientError
from copy import deepcopy
from ec2_utils.instance_info import resolve_account, stack_params_and_outputs_and_stack
from n_utils import _to_str
from n_utils.utils import expand_vars, get_images, ParamNotAvailable
from n_utils.git_utils import Git
from n_utils.ndt import find_include
from n_utils.ecr_utils import repo_uri
from n_utils.tf_utils import pull_state, flat_state, jmespath_var
from n_vault import Vault
from threadlocal_aws import region
stacks = dict()
terraforms = dict()
parameters = dict()
CFG_PREFIX = "AWS::CloudFormation::Init_config_files_"

############################################################################
# _THE_ yaml & json deserialize/serialize functions


def descalar(target):
    if isinstance(target, ScalarNode) or isinstance(target, SequenceNode) or \
       isinstance(target, MappingNode):
        if target.tag in INTRISINC_FUNCS:
            return INTRISINC_FUNCS[target.tag](None, '', target)
        else:
            return descalar(target.value)
    elif isinstance(target, list):
        ret = []
        for nxt in target:
            ret.append(descalar(nxt))
        return ret
    else:
        return target


def base64_ctor(loader, tag_suffix, node):
    return {'Fn::Base64': descalar(node.value)}


def findinmap_ctor(loader, tag_suffix, node):
    return {'Fn::FindInMap': descalar(node.value)}


def getatt_ctor(loader, tag_suffix, node):
    return {'Fn::GetAtt': descalar(node.value)}


def getazs_ctor(loader, tag_suffix, node):
    return {'Fn::GetAZs': descalar(node.value)}


def importvalue_ctor(loader, tag_suffix, node):
    return {'Fn::ImportValue': descalar(node.value)}


def join_ctor(loader, tag_suffix, node):
    return {'Fn::Join': descalar(node.value)}


def select_ctor(loader, tag_suffix, node):
    return {'Fn::Select': descalar(node.value)}


def split_ctor(loader, tag_suffix, node):
    return {'Fn::Split': descalar(node.value)}


def sub_ctor(loader, tag_suffix, node):
    return {'Fn::Sub': descalar(node.value)}


def ref_ctor(loader, tag_suffix, node):
    return {'Ref': descalar(node.value)}


def and_ctor(loader, tag_suffix, node):
    return {'Fn::And': descalar(node.value)}


def equals_ctor(loader, tag_suffix, node):
    return {'Fn::Equals': descalar(node.value)}


def if_ctor(loader, tag_suffix, node):
    return {'Fn::If': descalar(node.value)}


def not_ctor(loader, tag_suffix, node):
    return {'Fn::Not': descalar(node.value)}


def or_ctor(loader, tag_suffix, node):
    return {'Fn::Or': descalar(node.value)}


def importfile_ctor(loader, tag_suffix, node):
    return {'Fn::ImportFile': descalar(node.value)}


def importyaml_ctor(loader, tag_suffix, node):
    return {'Fn::ImportYaml': descalar(node.value)}


def merge_ctor(loader, tag_suffix, node):
    return {'Fn::Merge': descalar(node.value)}


INTRISINC_FUNCS = {
    '!Base64': base64_ctor,
    '!FindInMap': findinmap_ctor,
    '!GetAtt': getatt_ctor,
    '!GetAZs': getazs_ctor,
    '!ImportValue': importvalue_ctor,
    '!Join': join_ctor,
    '!Select': select_ctor,
    '!Split': split_ctor,
    '!Sub': sub_ctor,
    '!Ref': ref_ctor,
    '!And': and_ctor,
    '!Equals': equals_ctor,
    '!If': if_ctor,
    '!Not': not_ctor,
    '!Or': or_ctor,
    '!ImportFile': importfile_ctor,
    '!ImportYaml': importyaml_ctor,
    '!Merge': merge_ctor
}

SOURCED_PARAMS = None


def run_command(command):
    proc = subprocess.Popen(command, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, universal_newlines=True)
    output = proc.communicate()
    if proc.returncode:
        raise Exception("Failed to run " + str(command))
    return output[0]

def _resolve_stackref_from_dict(stack_var):
    if "region" in stack_var and "stackName" in stack_var and "paramName" in stack_var:
        return _resolve_stackref(stack_var['region'], stack_var['stackName'], stack_var['paramName'])
    elif "component" in stack_var and "stack" in stack_var and "paramName" in stack_var:
        param_name = stack_var["paramName"]
        del stack_var["paramName"]
        params = load_parameters(**stack_var)
        region = params["REGION"]
        stack_name = params["STACK_NAME"]
        return _resolve_stackref(region, stack_name, param_name)
    else:
        return None

def _resolve_stackref(region, stack_name, stack_param):
    stack_key = region + "." + stack_name
    stack_params = {}
    if stack_key in stacks:
        stack_params = stacks[stack_key]
    else:
        stack_params, _ = stack_params_and_outputs_and_stack(stack_name=stack_name, stack_region=region)
        stacks[stack_key] = stack_params
    if stack_param in stack_params:
        return stack_params[stack_param]
    return None

def _resolve_tfref_from_dict(tfref_var):
    if "component" in tfref_var and "terraform" in tfref_var and ("paramName" in tfref_var or "jmespath" in tfref_var):
        with Git() as git:
            current_branch = git.get_current_branch()
            if "branch" in tfref_var:
                branch = tfref_var["branch"]
            else:
                branch = current_branch
            tf_key = (tfref_var["component"], tfref_var["terraform"], branch)
            if tf_key in terraforms:
                terraform = terraforms[tf_key]
            else:
                root = "."
                if branch != current_branch:
                    root = git.export_branch(branch)
                terraform = pull_state(tfref_var["component"], tfref_var["terraform"], root=root)
                terraforms[tf_key] = terraform
            if "paramName" in tfref_var:
                flat_state_dict = flat_state(terraform)
                if tfref_var["paramName"] in flat_state_dict:
                    return flat_state_dict[tfref_var["paramName"]]
                else:
                    return None
            if "jmespath" in tfref_var:
                return jmespath_var(terraform, tfref_var["jmespath"])
    else:
        return None

def _process_infra_prop_line(line, params, used_params):
    key_val = line.split("=", 1)
    if len(key_val) == 2:
        key = re.sub("[^a-zA-Z0-9_]", "", key_val[0].strip())
        if key in os.environ:
            value = os.environ[key]
        else:
            value = key_val[1]
        value = _process_value(value, used_params)
        params[key] = value
        used_params[key] = value

def _process_value(value, used_params):
    value = value.strip()
    if (value.startswith("\"") and value.endswith("\"")) or (value.startswith("'") and value.endswith("'")):
        value = value[1:-1]
    value = expand_vars(value, used_params, None, [])
    # Don't go into external refs if:
    #   a) resolving base variables like REGION and paramEnvId
    #   b) resolving basic variables used in terraform backend configuration
    if  "DO_NOT_RESOLVE_EXTERNAL_REFS" not in os.environ and "TF_INIT_OUTPUT" not in os.environ:
        if value.strip().startswith("StackRef:"):
            stackref_doc = yaml_load(StringIO(_to_str(value)))
            stack_value = _resolve_stackref_from_dict(stackref_doc['StackRef'])
            if stack_value:
                value = stack_value
        if value.strip().startswith("TFRef:"):
            tfref_doc = yaml_load(StringIO(_to_str(value)))
            tf_value = _resolve_tfref_from_dict(tfref_doc['TFRef'])
            if tf_value:
                value = tf_value
        if value.strip().startswith("Encrypt:"):
            enc_doc = yaml_load(StringIO(_to_str(value)))
            enc_conf = enc_doc["Encrypt"]
            if isinstance(enc_conf, OrderedDict):
                to_encrypt = yaml_save(enc_conf["value"])
            else:
                to_encrypt = enc_conf["value"]
            value = _process_value(to_encrypt, used_params)
            del enc_conf["value"]
            vault = Vault(**enc_conf)
            value = b64encode(vault.direct_encrypt(value))
    return value

def import_parameter_file(filename, params):
    used_params = deepcopy(os.environ)
    used_params.update(params)
    with open(filename, "r") as propfile:
        prevline = ""
        for line in propfile.readlines():
            if line.startswith("#"):
                prevline = ""
                continue
            if line.endswith("\\"):
                prevline = prevline + line[:-1]
            else:
                line = prevline + line
                prevline = ""
                _process_infra_prop_line(line, params, used_params)
        if prevline:
            _process_infra_prop_line(prevline, params, used_params)


def _add_subcomponent_file(component, branch, type, name, files):
    if name:
        os.environ["ORIG_" + type.upper() + "_NAME"] = name
        files.append(component + os.sep + type + "-" + name + os.sep + "infra.properties")
        files.append(component + os.sep + type + "-" + name + os.sep + "infra-" + branch + ".properties")

def resolve_docker_uri(component, uriParam, image_branch, git):
    if not git:
        git = Git()
    with git:
        if uriParam in os.environ:
            return os.environ[uriParam]
        docker = uriParam[14:]
        docker_params = load_parameters(component=component, docker=docker, branch=image_branch, git=git)
        return repo_uri(docker_params['DOCKER_NAME'])

def lreplace(pattern, sub, string):
    return sub + string[len(pattern):] if string.startswith(pattern) else string

def rreplace(pattern, sub, string):
    return string[:-len(pattern)] + sub if string.endswith(pattern) else string

def resolve_ami(component_params, component, image, imagebranch, branch, git):
    if not git:
        git = Git()
    with git:
        if "paramAmi" + image in os.environ:
            return { "ImageId": os.environ["paramAmi" + image],
                    "Name": os.environ["paramAmiName" + image] \
                    if "paramAmiName" + image in os.environ else "Unknown" }
        images = []
        image_params = {}
        job = ""
        if "IMAGE_JOB" in os.environ and not image:
            job = re.sub(r'\W', '_', os.environ["IMAGE_JOB"])
        else:
            image_params = load_parameters(component=component, image=image, branch=imagebranch, git=git)
            if "JOB_NAME" in image_params:
                job = re.sub(r'\W', '_', image_params["JOB_NAME"])
            else:
                prefix = ""
                prefix = image_params["JENKINS_JOB_PREFIX"]
                job = prefix + "_" + component + "_bake"
                if image:
                    job = job + "_" + image
                job = re.sub(r'\W', '_', job)
        build_param = "paramAmi" + image + "Build"
        latest_baked = build_param in component_params and component_params[build_param] == 'latest'
        if latest_baked:
            # get current branch latest images
            images = get_images(job)
        if build_param in component_params and component_params[build_param] != 'latest':
            # resolve with a specifically set image build number
            build = component_params[build_param]
            image_tag = job + "_" + build
            job_tag_func = lambda image, image_name_prefix: len([tag for tag in image["Tags"] if tag["Value"] == image_tag]) > 0
            images = get_images(job, job_tag_function=job_tag_func)
        elif imagebranch != branch and not latest_baked:
            # resolve promote job
            suffix = "_bake"
            repl_suffix = "_promote"
            if image:
                suffix += "_" + image 
                repl_suffix += "_" + image
            if not image_params:
                image_params = load_parameters(component=component, image=image, branch=imagebranch, git=git)
            this_branch_prefix = re.sub(r'\W', '_', component_params["JENKINS_JOB_PREFIX"] + "_")
            image_branch_prefix = re.sub(r'\W', '_', image_params["JENKINS_JOB_PREFIX"] + "_")
            job = lreplace(image_branch_prefix, this_branch_prefix, job)
            job = rreplace(suffix, repl_suffix, job)
            images = get_images(job)
        else:
            # get current branch latest images
            images = get_images(job)
        if images:
            return images[0]
        else:
            return None

def load_parameters(component=None, stack=None, serverless=None, docker=None, image=None, 
                    cdk=None, terraform=None, branch=None, resolve_images=False,
                    git=None):
    subc_name = ""
    if stack:
        subc_name = "stack=" + stack
    if serverless:
        subc_name = "serverless=" + serverless
    if docker:
        subc_name = "docker=" + docker
    if isinstance(image, six.string_types):
        subc_name = "image=" + image
    if cdk:
        subc_name = "cdk=" + cdk
    if terraform:
        subc_name = "terraform=" + terraform
    if not git:
        git = Git()
    with git:
        current_branch = git.get_current_branch()
        if not branch:
            branch = current_branch
        branch = branch.strip().split("origin/")[-1:][0]
        params_key = (component, subc_name, branch)
        if params_key in parameters:
            return parameters[params_key]
        ret = {
            "GIT_BRANCH": branch
        }
        account = resolve_account()
        if account:
            ret["ACCOUNT_ID"] = account
        if component:
            ret["COMPONENT"] = component
        prefix = ""
        if current_branch != branch:
            prefix = git.export_branch(branch) + os.sep
        files = [prefix + "infra.properties", prefix + "infra-" + branch + ".properties"]
        if component:
            files.append(prefix + component + os.sep + "infra.properties")
            files.append(prefix + component + os.sep + "infra-" + branch + ".properties")
            _add_subcomponent_file(prefix + component, branch, "stack", stack, files)
            _add_subcomponent_file(prefix + component, branch, "serverless", serverless, files)
            _add_subcomponent_file(prefix + component, branch, "cdk", cdk, files)
            _add_subcomponent_file(prefix + component, branch, "terraform", terraform, files)
            _add_subcomponent_file(prefix + component, branch, "docker", docker, files)
            _add_subcomponent_file(prefix + component, branch, "image", image, files)
            if isinstance(image, six.string_types):
                files.append(prefix + component + os.sep + "image" + os.sep + "infra.properties")
                files.append(prefix + component + os.sep + "image" + os.sep + "infra-" + branch + ".properties")
        initial_resolve = ret.copy()
        os.environ["DO_NOT_RESOLVE_EXTERNAL_REFS"] = "true"
        for file in files:
            if os.path.exists(file):
                import_parameter_file(file, initial_resolve)
        del os.environ["DO_NOT_RESOLVE_EXTERNAL_REFS"]
        if "REGION" not in initial_resolve:
            ret["REGION"] = region()
        else:
            ret["REGION"] = initial_resolve["REGION"]
        if not "AWS_DEFAULT_REGION" in os.environ:
            os.environ["AWS_DEFAULT_REGION"] = ret["REGION"]
        if "paramEnvId" not in initial_resolve:
            ret["paramEnvId"] = branch
        else:
            ret["paramEnvId"] = initial_resolve["paramEnvId"]
        for file in files:
            if os.path.exists(file):
                import_parameter_file(file, ret)
        if (serverless or stack or cdk or terraform) and resolve_images:
            image_branch = branch
            if 'BAKE_IMAGE_BRANCH' in ret:
                image_branch = ret['BAKE_IMAGE_BRANCH']
            for docker in [dockerdir.split("/docker-")[1] for dockerdir in glob(component + os.sep + "docker-*")]:
                try:
                    ret['paramDockerUri' + docker] = resolve_docker_uri(component, 'paramDockerUri' + docker, image_branch, git)
                except ClientError:
                    # Best effor to load docker uris, but ignore errors since the repo might not
                    # actually be in use. Missing and used uris will result in an error later.
                    pass
            for image_name in [imagedir.split("/image")[1].replace("-", "").lower() for imagedir in glob(component + os.sep + "image*")]:
                try:
                    image = resolve_ami(ret, component, image_name, image_branch, branch, git)
                    if image:
                        ret['paramAmi' + image_name] = image['ImageId']
                        ret['paramAmiName' + image_name] = image['Name']
                        env_param_name = "AMI_ID"
                        if image_name:
                            env_param_name +=  "_" + image_name.upper()
                        ret[env_param_name] = image['ImageId']
                except ClientError:
                    # Best effor to load ami info, but ignore errors since the image might not
                    # actually be in use. Missing and used images will result in an error later.
                    pass
        if "REGION" not in ret:
            ret["REGION"] = region()
        if "paramEnvId" not in ret:
            ret["paramEnvId"] = branch
        if "ORIG_STACK_NAME" in os.environ:
            ret["ORIG_STACK_NAME"] = os.environ["ORIG_STACK_NAME"]
            if "STACK_NAME" not in ret:
                ret["STACK_NAME"] = component + "-" + ret["ORIG_STACK_NAME"] + "-" + ret["paramEnvId"]
        for k, v in list(os.environ.items()):
            if k.startswith("ORIG_") and k.endswith("_NAME"):
                ret[k] = v
        if "ORIG_DOCKER_NAME" in os.environ:
            if "DOCKER_NAME" not in ret:
                ret["DOCKER_NAME"] = component + "/" + ret["paramEnvId"] + "-" + ret["ORIG_DOCKER_NAME"]
        if "JENKINS_JOB_PREFIX" not in ret:
            ret["JENKINS_JOB_PREFIX"] = "ndt" + ret["paramEnvId"]
        parameters[params_key] = ret
        return ret


def yaml_load(stream):
    for name in INTRISINC_FUNCS:
        yaml.add_multi_constructor(name, INTRISINC_FUNCS[name], Loader=yaml.SafeLoader)

    class OrderedLoader(yaml.SafeLoader):
        pass

    def construct_mapping(loader, node):
        loader.flatten_mapping(node)
        return OrderedDict(loader.construct_pairs(node))
    OrderedLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
        construct_mapping)

    return yaml.load(stream, OrderedLoader)


def yaml_save(data):
    class OrderedDumper(yaml.SafeDumper):
        pass

    def _dict_representer(dumper, data):
        return dumper.represent_mapping(
            yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
            list(data.items()))

    OrderedDumper.add_representer(OrderedDict, _dict_representer)
    return yaml.dump(data, None, OrderedDumper, default_flow_style=False)


def json_load(stream):
    return json.loads(stream, object_pairs_hook=OrderedDict)


def json_save(data):
    return json.dumps(data, indent=2)


def json_save_small(data):
    return json.dumps(data, indent=None)


############################################################################
# import_scripts
gotImportErrors = False

# the CF_ prefix is expected already to have been stripped


def decode_parameter_name(name):
    return re.sub('__', '::', name)

# the "var " prefix is to support javascript as well
VAR_DECL_RE = re.compile(
    r'^((\s*var\s+)|(\s*const\s+))?CF_([^\s=]+)[\s="\']*([^#"\'\`]*)(?:["\'\s\`]*)(#optional)?')
EMBED_DECL_RE = re.compile(
    r'^(.*?=\s*)?(.*?)(?:(?:\`?#|//)CF([^#\`]*))[\"\`\s]*(#optional)?')
IN_PLACE_RE = re.compile(r'^([^\$]*?)\$CF{([^}\|]*)(\|[^}]*)?}(#optional)?(.*)')

def import_script(filename):
    arr = []
    with open(filename) as fd:
        for line in fd:
            next_arr = do_replace(line, filename)
            arr = arr + next_arr
    return arr

def do_replace(line, filename):
    arr = []
    result = VAR_DECL_RE.match(line)
    if result:
        js_prefix = result.group(1)
        encoded_varname = result.group(4)
        var_name = decode_parameter_name(encoded_varname)
        ref = OrderedDict()
        ref['Ref'] = var_name
        ref['__source'] = filename
        if str(result.group(6)) == "#optional":
            ref['__optional'] = "true"
            ref['__default'] = str(result.group(5)).strip(" \"'")
        arr.append(line[0:result.end(4)] + "='")
        arr.append(ref)
        if js_prefix:
            arr.append("';\n")
        else:
            arr.append("'\n")
    else:
        result = EMBED_DECL_RE.match(line)
        if result:
            prefix = result.group(1)
            if not prefix:
                prefix = result.group(2)
                default_val = ""
            else:
                default_val = str(result.group(2)).strip(" \"'")
            arr.append(prefix + "'")
            for entry in yaml_load("[" + result.group(3) + "]"):
                apply_source(entry, filename, str(result.group(4)),
                                default_val)
                arr.append(entry)
            if filename.endswith(".ps1"):
                arr.append("'\r\n")
            else:
                arr.append("'\n")
        else:
            result = IN_PLACE_RE.match(line)
            if result:
                arr.append(result.group(1))
                var_name = decode_parameter_name(result.group(2))
                ref = OrderedDict()
                ref['Ref'] = var_name
                ref['__source'] = filename
                if str(result.group(4)) == "#optional":
                    ref['__optional'] = "true"
                    if result.group(3):
                        ref['__default'] = str(result.group(3)[1:])
                    else:
                        ref['__default'] = ""
                arr.append(ref)
                arr = arr + do_replace(result.group(5), filename)
            else:
                arr.append(line)
    return arr


def resolve_file(filename, basefile):
    if filename[0] == "/":
        return existing(filename)
    if re.match(r"^(\.\./\.\./|\.\./|\./)?aws-utils/.*", filename):
        return existing(find_include(re.sub(r"^(\.\./\.\./|\.\./|\./)?aws-utils/", "", filename)))
    if re.match(r"^\(\(\s?includes\s?\)\)/.*", filename):
        return existing(find_include(re.sub(r"^\(\(\s?includes\s?\)\)/", "", filename)))
    base = os.path.dirname(basefile)
    if len(base) == 0:
        base = "."
    return existing(base + "/" + filename)


def existing(filename):
    if filename and os.path.exists(filename):
        return filename
    else:
        return None

PARAM_NOT_AVAILABLE = ParamNotAvailable()


def _add_params(target, source, source_prop, use_value):
    if source_prop in source:
        if isinstance(source[source_prop], OrderedDict) or isinstance(source[source_prop], dict):
            for k, val in list(source[source_prop].items()):
                target[k] = val['Default'] if use_value and 'Default' in val else PARAM_NOT_AVAILABLE
        elif isinstance(source[source_prop], list):
            for list_item in source[source_prop]:
                for k, val in list(list_item.items()):
                    target[k] = val['Default'] if use_value and 'Default' in val else PARAM_NOT_AVAILABLE

def _get_params(data, template):
    params = OrderedDict()

    # first load defaults for all parameters in "Parameters"
    if 'Parameters' in data:
        _add_params(params, data, 'Parameters', True)
        if 'Fn::Merge' in data['Parameters'] and 'Result' in data['Parameters']['Fn::Merge']:
            _add_params(params, data['Parameters']['Fn::Merge'], 'Result', True)
        if 'Fn::ImportYaml' in data['Parameters'] and 'Result' in data['Parameters']['Fn::ImportYaml']:
            _add_params(params, data['Parameters']['Fn::ImportYaml'], 'Result', True)
    if "resources" in data and 'Parameters' in data['resources']:
        params['ServerlessDeploymentBucket'] = PARAM_NOT_AVAILABLE
        _add_params(params, data['resources'], 'Parameters', True)
        if 'Fn::Merge' in data['resources']['Parameters'] and 'Result' in data['resources']['Parameters']['Fn::Merge']:
            _add_params(params, data['resources']['Parameters']['Fn::Merge'], 'Result', True)
        if 'Fn::ImportYaml' in data['resources']['Parameters'] and 'Result' in data['resources']['Parameters']['Fn::ImportYaml']:
            _add_params(params, data['resources']['Parameters']['Fn::ImportYaml'], 'Result', True)

    params['STACK_NAME'] = PARAM_NOT_AVAILABLE

    if 'REGION' not in os.environ:
        os.environ['REGION'] = region()
    params['REGION'] = os.environ['REGION']

    if 'ACCOUNT_ID' not in os.environ:
        if resolve_account():
            os.environ['ACCOUNT_ID'] = resolve_account()
        else:
            os.environ['ACCOUNT_ID'] = "None"
    params['ACCOUNT_ID'] = os.environ['ACCOUNT_ID']

    global SOURCED_PARAMS
    if not SOURCED_PARAMS:
        SOURCED_PARAMS = {}
        # then override them with values from infra
        template_dir = os.path.dirname(os.path.abspath(template))
        image_dir = os.path.dirname(template_dir)

        image_name = os.path.basename(image_dir)
        stack_name = os.path.basename(template_dir)
        stack_name = re.sub('^stack-', '', stack_name)
        SOURCED_PARAMS = load_parameters(component=image_name, stack=stack_name)
        SOURCED_PARAMS.update(os.environ)

    params.update(SOURCED_PARAMS)

    # source_infra_properties.sh always resolves a region, account id and stack
    # name
    params["AWS::Region"] = params['REGION']
    params["AWS::AccountId"] = params['ACCOUNT_ID']
    params["AWS::StackName"] = params['STACK_NAME']

    # finally load AWS-provided and "Resources"
    params["AWS::NotificationARNs"] = PARAM_NOT_AVAILABLE
    params["AWS::NoValue"] = PARAM_NOT_AVAILABLE
    params["AWS::StackId"] = PARAM_NOT_AVAILABLE
    _add_params(params, data, 'Resources', False)
    if "resources" in data:
        _add_params(params, data['resources'], 'Resources', False)
    return params


# Applies recursively source to script inline expression


def apply_source(data, filename, optional, default):
    if isinstance(data, OrderedDict):
        if 'Ref' in data:
            data['__source'] = filename
            if optional == "#optional":
                data['__optional'] = "true"
                data['__default'] = default
        for k, val in list(data.items()):
            apply_source(k, filename, optional, default)
            apply_source(val, filename, optional, default)

# returns new data


def _preprocess_template(data, root, basefile, path, templateParams):
    param_refresh_callback = lambda: templateParams.update(_get_params(root, basefile))
    param_refresh_callback()
    global gotImportErrors
    if isinstance(data, OrderedDict):
        if 'Fn::ImportFile' in data:
            val = data['Fn::ImportFile']
            file = expand_vars(val, templateParams, None, [])
            script_import = resolve_file(file, basefile)
            if script_import:
                data.clear()
                contents = import_script(script_import)
                data['Fn::Join'] = ["", contents]
            else:
                print("ERROR: " + val + ": Can't import file \"" + val +
                      "\" - file not found on include paths or relative to " +
                      basefile)
                gotImportErrors = True
        elif 'Fn::ImportYaml' in data:
            val = data['Fn::ImportYaml']
            file = expand_vars(val, templateParams, None, [])
            yaml_file = resolve_file(file, basefile)
            del data['Fn::ImportYaml']
            if yaml_file:
                contents = yaml_load(open(yaml_file))
                params = OrderedDict(list(templateParams.items()))
                params.update(data)
                contents = expand_vars(contents, params, None, [])
                data['Fn::ImportYaml'] = OrderedDict()
                data['Fn::ImportYaml']['Result'] = contents
                param_refresh_callback()
                while True:
                    expanded_result = expand_vars(contents, templateParams, None, [])
                    if expanded_result == contents:
                        break
                    else:
                        contents.clear()
                        contents.update(expanded_result)
                        param_refresh_callback()
                data.clear()
                if isinstance(contents, OrderedDict):
                    for k, val in list(contents.items()):
                        data[k] = _preprocess_template(val, root, yaml_file, path +
                                                       k + "_", templateParams)
                elif isinstance(contents, list):
                    data = contents
                    for i in range(0, len(data)):
                        data[i] = _preprocess_template(data[i], root, yaml_file,
                                                       path + str(i) + "_", templateParams)
                else:
                    print("ERROR: " + path + ": Can't import yaml file \"" +
                          yaml_file + "\" that isn't an associative array or" +
                          " a list in file " + basefile)
                    gotImportErrors = True
            else:
                if not ('optional' in data and data['optional']):
                    print("ERROR: " + val + ": Can't import file \"" + val +
                          "\" - file not found on include paths or relative to " +
                          basefile)
                    gotImportErrors = True
                else:
                    for k in data:
                        del data[k]
            if "optional" in data:
                del data["optional"]
        elif 'Fn::Merge' in data:
            merge_list = data['Fn::Merge']['Source'] if 'Source' in data['Fn::Merge'] else data['Fn::Merge']
            result = data['Fn::Merge']['Result'] if 'Result' in data['Fn::Merge'] else OrderedDict()
            data['Fn::Merge'] = OrderedDict([('Source', merge_list), ('Result', result)])
            if not isinstance(merge_list, list):
                print("ERROR: " + path + ": Fn::Merge must associate to a list in file " + basefile)
                gotImportErrors = True
                return data
            merge = _preprocess_template(expand_vars(merge_list.pop(0), templateParams, None, []), root, basefile,
                                         path + "/", templateParams)
            if not result:
                result = merge
                data['Fn::Merge'] = OrderedDict([('Source', merge_list), ('Result', result)])
            elif not isinstance(merge, type(result)):
                print("ERROR: " + path + ": First Fn::Merge entries " +
                        "were of type " + str(type(result)) + ", but the following entry was not: \n" + \
                        json.dumps(merge, indent=2) + "\nIn file " + basefile)
                gotImportErrors = True
            elif isinstance(merge, OrderedDict):
                result.update(merge)
            elif isinstance(merge, list):
                result.extend(merge)
            else:
                print("ERROR: " + path + ": Unsupported " + str(type(merge)))
                gotImportErrors = True
            param_refresh_callback()
            while True:
                expanded_result = expand_vars(result, templateParams, None, [])
                if expanded_result == result:
                    break
                else:
                    result.clear()
                    result.update(expanded_result)
                    param_refresh_callback()
            if not merge_list:
                del data['Fn::Merge']
                return result
            else:
                return _preprocess_template(data, root, basefile, path + "/", templateParams)
        elif 'StackRef' in data:
            stack_var = expand_vars(data['StackRef'], templateParams, None, [])
            stack_var = _check_refs(stack_var, basefile,
                                    path + "StackRef_", templateParams,
                                    True)
            data.clear()
            stack_value = _resolve_stackref_from_dict(stack_var)
            if not stack_value:
                raise StackRefUnresolved("Did not find value for: " + stack_var['paramName'] + \
                                        " in stack " + stack_var['region'] + "." + stack_var['stackName'])
            param_refresh_callback()
            return stack_value
        elif 'TFRef' in data:
            tf_var = expand_vars(data['TFRef'], templateParams, None, [])
            tf_var = _check_refs(tf_var, basefile,
                                 path + "TFRef_", templateParams, True)
            data.clear()
            tf_value = _resolve_tfref_from_dict(tf_var)
            if not tf_value:
                ref = stack_var['paramName'] if 'paramName' in stack_var else stack_var['jmespath']
                raise TFRefUnresolved("Did not find value for: " + ref + \
                                    " in terraform compnent " + stack_var['component'] + "." + stack_var['terraform'])
            param_refresh_callback()
            return tf_value
        elif 'Encrypt' in data and 'value' in data['Encrypt']:
            to_encrypt = data['Encrypt']['value']
            enc_conf = data['Encrypt']
            del enc_conf['value']
            vault = Vault(**enc_conf)
            resolved_value = _preprocess_template(to_encrypt, root, basefile, path + "Encrypt_", templateParams)
            if not isinstance(resolved_value, six.string_types):
                raise EncryptException("Encrypted value needs to be a string")
            return b64encode(vault.direct_encrypt(resolved_value))
        elif 'Ref' in data:
            data['__source'] = basefile
        else:
            if 'Parameters' in data:
                data['Parameters'] = _preprocess_template(data['Parameters'], root, basefile, path + "Parameters_",
                                                          templateParams)
                param_refresh_callback()
            for k, val in list(data.items()):
                if k != 'Parameters':
                    data[k] = expand_vars(_preprocess_template(val, root, basefile, path + k + "_", templateParams), templateParams, None, [])
    elif isinstance(data, list):
        for i in range(0, len(data)):
            data[i] = _preprocess_template(data[i], root, basefile, path + str(i) + "_", templateParams)
    return data

# returns new data


def _check_refs(data, templateFile, path, templateParams, resolveRefs):
    global gotImportErrors
    if isinstance(data, OrderedDict):
        if 'Ref' in data:
            var_name = data['Ref']
            if '__source' in data:
                filename = data['__source']
                del data['__source']
            else:
                filename = "unknown"
            if var_name not in templateParams:
                if '__optional' in data:
                    data = data['__default']
                else:
                    print("ERROR: " + path + ": Referenced parameter \"" +
                          var_name + "\" in file " + filename +
                          " not declared in template parameters in " +
                          templateFile)
                    gotImportErrors = True
            else:
                if resolveRefs:
                    data = templateParams[var_name]
                    if data == PARAM_NOT_AVAILABLE:
                        print("ERROR: " + path + ": Referenced parameter \"" +
                              var_name + "\" in file " + filename +
                              " is resolved later by AWS; cannot resolve its" +
                              " value now")
                        gotImportErrors = True
            if '__optional' in data:
                del data['__optional']
            if '__default' in data:
                del data['__default']
        else:
            for k, val in list(data.items()):
                data[k] = _check_refs(val, templateFile, path + k +
                                               "_", templateParams, resolveRefs)
    elif isinstance(data, list):
        for i in range(0, len(data)):
            data[i] = _check_refs(data[i], templateFile, path +
                                           str(i) + "_", templateParams,
                                           resolveRefs)
    return data


def import_scripts(data, basefile):
    global gotImportErrors
    gotImportErrors = False

    data = expand_vars(data, _get_params(data, basefile), None, [])
    data = _preprocess_template(data, data, basefile, "", _get_params(data, basefile))
    data = _check_refs(data, basefile, "", _get_params(data, basefile), False)
    if gotImportErrors:
        sys.exit(1)
    return data

############################################################################
# extract_scripts


def bash_encode_parameter_name(name):
    return "CF_" + re.sub('::', '__', name)


def encode_script_filename(prefix, path):
    if path.find("UserData_Fn::Base64") != -1:
        return prefix + "-userdata.sh"
    idx = path.find(CFG_PREFIX)
    if idx != -1:
        soff = idx + len(CFG_PREFIX)
        eoff = path.find("_content_", soff)
        cfg_path = path[soff:eoff]
        return prefix + "-" + cfg_path[cfg_path.rfind("/") + 1:]
    return prefix + "-" + path


def extract_script(prefix, path, join_args):
    # print prefix, path
    # "before" and "after" code blocks, placed before and after var declarations
    code = ["", ""]
    var_decls = OrderedDict()
    code_idx = 0
    for element in join_args:
        if isinstance(element, OrderedDict):
            if 'Ref' not in element:
                print("Dict with no ref")
                json_save(element)
            else:
                var_name = element['Ref']
                if not len(var_name) > 0:
                    raise Exception("Failed to convert reference inside " +
                                    "script: " + str(element))
                bash_varname = bash_encode_parameter_name(var_name)
                var_decl = ""
                # var_decl += "#" + var_name + "\n"
                var_decl += bash_varname + "=\"\";\n"
                var_decls[var_name] = var_decl
                code[code_idx] += "${" + bash_varname + "}"
        else:
            code[code_idx] += element
        code_idx = 1  # switch to "after" block

    filename = encode_script_filename(prefix, path)
    sys.stderr.write(prefix + ": Exported path '" + path +
                     "' contents to file '" + filename + "'\n")
    with open(filename, "w") as script_file:  # opens file with name of "test.txt"
        script_file.write(code[0])
        script_file.write("\n")
        for var_name, var_decl in list(var_decls.items()):
            script_file.write(var_decl)
        script_file.write("\n")
        script_file.write(code[1])
    return filename

# data argument is mutated


def extract_scripts(data, prefix, path=""):
    if not isinstance(data, OrderedDict):
        return
    for k, val in list(data.items()):
        extract_scripts(val, prefix, path + k + "_")
        if k == "Fn::Join":
            if not val[0] == "":
                continue
            if isinstance(val[1][0], six.string_types) and (val[1][0].find("#!") != 0):
                continue
            script_file = extract_script(prefix, path, val[1])
            del data[k]
            data['Fn::ImportFile'] = script_file

############################################################################
# simple apis


def yaml_to_dict(yaml_file_to_convert, merge=[]):
    data = OrderedDict()
    with open(yaml_file_to_convert) as yaml_file:
        data = yaml_load(yaml_file)
    if merge:
        for i in range(0, len(merge)):
            with open(merge[i]) as yaml_file:
                merge[i] = yaml_load(yaml_file)
        merge.append(data)
        merge_data = OrderedDict()
        merge_data['Fn::Merge'] = merge
        data = merge_data
    data = import_scripts(data, yaml_file_to_convert)
    _patch_launchconf(data)
    return data


def yaml_to_json(yaml_file_to_convert, merge=[]):
    data = yaml_to_dict(yaml_file_to_convert, merge)
    return json_save(data)


def yaml_to_yaml(yaml_file_to_convert):
    data = yaml_to_dict(yaml_file_to_convert)
    return yaml_save(data)


def json_to_yaml(json_file_to_convert):
    data = json_load(open(json_file_to_convert).read())
    extract_scripts(data, json_file_to_convert)
    return yaml_save(data)


############################################################################
# misc json
def locate_launchconf_metadata(data):
    if "Resources" in data:
        resources = data["Resources"]
        for val in list(resources.values()):
            if "Type" in val and val["Type"] == "AWS::AutoScaling::LaunchConfiguration" and \
                    "Metadata" in val:
                return val["Metadata"]
    return None


def locate_launchconf_userdata(data):
    resources = data["Resources"]
    for val in list(resources.values()):
        if "Type" in val and val["Type"] == "AWS::AutoScaling::LaunchConfiguration":
            if "Properties" in val and "UserData" in val["Properties"] and \
               "Fn::Base64" in val["Properties"]["UserData"] and \
               "Fn::Join" in val["Properties"]["UserData"]["Fn::Base64"] and \
               len(val["Properties"]["UserData"]["Fn::Base64"]["Fn::Join"]) >= 2:
                return val["Properties"]["UserData"]["Fn::Base64"]["Fn::Join"][1]
            else:
                if "Properties" in val and "UserData" in val["Properties"] and \
                   "Fn::Base64" in val["Properties"]["UserData"] and \
                   "Fn::Sub" in val["Properties"]["UserData"]["Fn::Base64"]:
                    return val["Properties"]["UserData"]["Fn::Base64"]["Fn::Sub"]
    return None


def reset_launchconf_userdata(data, lc_userdata):
    resources = data["Resources"]
    for val in list(resources.values()):
        if "Type" in val and val["Type"] == "AWS::AutoScaling::LaunchConfiguration":
            val["Properties"]["UserData"]["Fn::Base64"]["Fn::Sub"] = lc_userdata


def get_refs(data, reflist=None):
    if not reflist:
        reflist = []
    if isinstance(data, OrderedDict):
        if "Ref" in data:
            reflist.append(data["Ref"])
        for val in list(data.values()):
            get_refs(val, reflist)
    elif isinstance(data, list):
        for ref in data:
            get_refs(ref, reflist)
    return reflist


def _patch_launchconf(data):
    lc_meta = locate_launchconf_metadata(data)
    if lc_meta is not None:
        lc_userdata = locate_launchconf_userdata(data)
        if lc_userdata:
            if isinstance(lc_userdata, list):
                lc_userdata.append("\nexit 0\n# metadata hash: " + str(hash(json_save(lc_meta))) + "\n")
            else:
                lc_userdata += "\nexit 0\n# metadata hash: " + str(hash(json_save(lc_meta))) + "\n"
                reset_launchconf_userdata(data, lc_userdata)
        lc_meta_refs = set(get_refs(lc_meta))
        if len(lc_meta_refs) > 0:
            first = 1
            for ref in lc_meta_refs:
                lc_userdata.append("# metadata params: " if first else ", ")
                lc_userdata.append({"Ref": ref})
                first = 0
            lc_userdata.append("\n")

class StackRefUnresolved(Exception):
    pass

class TFRefUnresolved(Exception):
    pass

class EncryptException(Exception):
    pass
