import json
import jmespath
from collections import OrderedDict

def flat_state(state):
    ret = OrderedDict()
    state_doc = json.loads(state)
    if "modules" in state_doc:
        for module in state_doc["modules"]:
            if "outputs" in module:
                for key, val in module["outputs"].items():
                    ret[key] = str(val["value"])
            if "resources" in module:
                for key, val in module["resources"].items():
                    if "primary" in val:
                        primary = val["primary"]
                        name = ".".join(key.split(".")[1:])
                        if "id" in primary:
                            ret[name + ".id"] = primary["id"]
                        if "attributes" in primary:
                            for attribute, attr_val in primary["attributes"].items():
                                ret[name + "." + attribute] = attr_val
    return ret

def jmespath_var(state, jmespath_expr):
    state_doc = json.loads(state)
    ret = jmespath.search(jmespath_expr, state_doc)
    if isinstance(ret[0], dict):
        return json.dumps(ret[0])
    else:
        return "\n".join(ret)
