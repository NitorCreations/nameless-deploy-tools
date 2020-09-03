import json
import six
from collections import OrderedDict
from subprocess import Popen, PIPE

from jmespath import search

from n_utils import _to_str

def flat_state(state_doc):
    ret = OrderedDict()
    if "outputs" in state_doc:
        for key, entry in state_doc["outputs"].items():
            ret[key] = entry["value"]
    if "resources" in state_doc:
        for entry in state_doc["resources"]:
            prefix = entry["name"]
            if "instances" in entry:
                if len(entry["instances"]) == 1:
                    for key, value in entry["instances"][0]["attributes"].items():
                        ret[prefix + "." + key] = value
                else:
                    for i in range(0, len(entry["instances"])):
                        for key, value in entry["instances"][i]["attributes"].items():
                            ret[prefix + "." + str(i) + "." + key] = value
    return ret

def jmespath_var(state_doc, jmespath_expr):
    ret = search(jmespath_expr, state_doc)
    if isinstance(ret[0], dict):
        return json.dumps(ret[0])
    else:
        return "\n".join(ret)

def pull_state(component, terraform, root="."):
    cmd = ["ndt", "terraform-pull-state", component, terraform]
    process = Popen(cmd, cwd=root, stdout=PIPE, stderr=PIPE)
    stdout, _  = process.communicate()
    if process.returncode != 0:
        return {}
    return json.loads(stdout)