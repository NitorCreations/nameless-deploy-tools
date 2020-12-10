import json
from os import devnull
from subprocess import Popen, PIPE

ARR_START = "[".encode()
OBJ_START = "{".encode()

def az_login():
    proc = Popen(
        ["az", "login"],
        stdout=PIPE,
        stderr=PIPE,
    )
    output, err = proc.communicate()
    if proc.returncode != 0:
        return []
    return json.loads(output[output.find(ARR_START):])

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
    return json.loads(output[output.find(OBJ_START):])

def az_account_list():
    proc = Popen(
        ["az", "account", "list"],
        stdout=PIPE,
        stderr=PIPE,
    )
    output, err = proc.communicate()
    if proc.returncode != 0:
        return []
    return json.loads(output[output.find(ARR_START):])

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
