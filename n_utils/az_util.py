import json
from subprocess import PIPE, Popen

ARR_START = b"["
OBJ_START = b"{"


def az_login():
    proc = Popen(
        ["az", "login"],
        stdout=PIPE,
        stderr=PIPE,
    )
    output, err = proc.communicate()
    if proc.returncode != 0:
        return []
    return json.loads(output[output.find(ARR_START) :])


def az_logout():
    proc = Popen(
        ["az", "logout"],
        stdout=PIPE,
        stderr=PIPE,
    )
    output, err = proc.communicate()
    return proc.returncode == 0


def az_account_show():
    proc = Popen(
        ["az", "account", "show"],
        stdout=PIPE,
        stderr=PIPE,
    )
    output, _err = proc.communicate()
    if proc.returncode != 0:
        return {}
    return json.loads(output[output.find(OBJ_START) :])


def az_account_list():
    proc = Popen(
        ["az", "account", "list"],
        stdout=PIPE,
        stderr=PIPE,
    )
    output, err = proc.communicate()
    if proc.returncode != 0:
        return []
    return json.loads(output[output.find(ARR_START) :])


def az_find_subscription_id(name, account_list):
    for subscription in account_list:
        if subscription["name"] == name or subscription["id"] == name:
            return subscription["id"]
    return None


def az_set_subscription(subscription_id):
    proc = Popen(
        ["az", "account", "set", "--subscription", subscription_id],
        stdout=PIPE,
        stderr=PIPE,
    )
    output, err = proc.communicate()
    return proc.returncode == 0


def az_select_subscription(name):
    curr_account = az_account_show()
    subscription_id = None
    if "name" in curr_account and "id" in curr_account:
        if curr_account["name"] == name or curr_account["id"] == name:
            return curr_account["id"]
        else:
            subscription_id = az_find_subscription_id(name, az_account_list())
    if not subscription_id:
        az_logout()
        subscription_id = az_find_subscription_id(name, az_login())

    if subscription_id:
        az_set_subscription(subscription_id)
    return subscription_id


def ensure_group(location, group_name):
    proc = Popen(
        ["az", "group", "list", "--query", "[?name=='" + group_name + "']"],
        stdout=PIPE,
        stderr=PIPE,
    )
    output, err = proc.communicate()
    groups = json.loads(output[output.find(ARR_START) :])
    if len(groups) == 0:
        proc = Popen(
            ["az", "group", "create", "--name", group_name, "--location", location],
            stdout=PIPE,
            stderr=PIPE,
        )
        output, err = proc.communicate()
        if proc.returncode == 0:
            groups = [json.loads(output[output.find(OBJ_START) :])]
        else:
            groups = [{}]
    return groups[0]


def ensure_management_group(group_name):
    proc = Popen(
        [
            "az",
            "account",
            "management-group",
            "list",
            "--query",
            "[?name=='" + group_name + "']",
        ],
        stdout=PIPE,
        stderr=PIPE,
    )
    output, err = proc.communicate()
    groups = json.loads(output[output.find(ARR_START) :])
    if len(groups) == 0:
        proc = Popen(
            ["az", "account", "management-group", "create", "--name", group_name],
            stdout=PIPE,
            stderr=PIPE,
        )
        output, err = proc.communicate()
        if proc.returncode == 0:
            groups = [json.loads(output[output.find(OBJ_START) :])]
        else:
            groups = [{}]


def delete_group(group_name):
    proc = Popen(
        ["az", "group", "delete", "-y", "--name", group_name],
        stdout=PIPE,
        stderr=PIPE,
    )
    output, err = proc.communicate()
    return proc.returncode == 0


def fetch_properties(parameters):
    cmd = get_az_command("show", parameters) + ["--query", "properties"]
    process = Popen(cmd, stdout=PIPE, stderr=PIPE)
    stdout, _ = process.communicate()
    if process.returncode != 0:
        return {}
    props = json.loads(stdout)
    ret = {}
    if "parameters" in props:
        for parameter, value in props["parameters"].items():
            if "value" in value:
                ret[parameter] = str(value["value"])
    if "outputs" in props:
        for output, value in props["outputs"].items():
            if "value" in value:
                ret[output] = str(value["value"])
    return ret


def get_az_command(command, parameters):
    scope = parameters.get("AZURE_SCOPE", "group")
    if "DEPLOYMENT_NAME" in parameters:
        name = parameters["DEPLOYMENT_NAME"]
    else:
        name = f"{parameters['BUILD_JOB_PREFIX']}_{parameters['COMPONENT']}_{parameters['ORIG_AZURE_NAME']}"
    ret = ["az", "deployment", command, "--name", name]
    if scope == "group":
        if "AZURE_GROUP" not in parameters:
            raise MissingAzureGroup
        ret.insert(2, "group")
        ret.append("--resource-group")
        ret.append(parameters["AZURE_GROUP"])
    elif scope == "management-group":
        if "AZURE_MANAGEMENT_GROUP" not in parameters:
            raise MissingAzureManagementGroup
        ret.insert(2, "mg")
        ret.append("--management-group-id")
        ret.append(parameters["AZURE_MANAGEMENT_GROUP"])
    elif scope == "subscription":
        ret.insert(2, "sub")
    elif scope == "tenant":
        ret.insert(2, "tenant")
    else:
        raise UnknownAzureGroupException
    return ret


class UnknownAzureGroupException(Exception):
    pass


class MissingAzureGroup(Exception):
    pass


class MissingAzureManagementGroup(Exception):
    pass
