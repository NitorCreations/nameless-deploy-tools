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

""" Utilities to work with instances made by nameless-deploy-tools stacks
"""

import io
import json
import os
import random
import re
import shutil
import string
import tempfile
import time
from builtins import object
from builtins import range
from builtins import str
from collections import OrderedDict
from copy import deepcopy
from operator import itemgetter

import six
from botocore.exceptions import ClientError
from ec2_utils.instance_info import resolve_account, info, is_ec2, stack_params_and_outputs_and_stack
from n_vault import Vault
from threadlocal_aws import region
from threadlocal_aws.clients import cloudformation, ec2, sts

from n_utils import _to_str
from n_utils.mfa_utils import mfa_read_token, mfa_generate_code

NoneType = type(None)
ACCOUNT_ID = None
ROLE_NAME = None
INSTANCE_IDENTITY_URL = 'http://169.254.169.254/latest/dynamic/instance-identity/document'
USER_DATA_URL = 'http://169.254.169.254/latest/user-data'
INSTANCE_DATA_LINUX = '/opt/nameless/instance-data.json'
INSTANCE_DATA_WIN = 'C:/nameless/instance-data.json'

dthandler = lambda obj: obj.isoformat() if hasattr(obj, 'isoformat') else json.JSONEncoder().default(obj)

class ParamNotAvailable(object):
    def __init__(self):
        return
    def isoformat(self):
        return "PARAM_NOT_AVAILABLE"

def id_generator(size=10, chars=string.ascii_uppercase + string.digits +
                 string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))

def assume_role(role_arn, mfa_token_name=None, duration_minutes=60):
    if mfa_token_name:
        token = mfa_read_token(mfa_token_name)
        code = mfa_generate_code(mfa_token_name)
        response = sts().assume_role(RoleArn=role_arn,
                                   RoleSessionName="n-sess-" + id_generator(),
                                   SerialNumber=token['token_arn'],
                                   TokenCode=code,
                                   DurationSeconds=(duration_minutes * 60))
    else:
        response = sts().assume_role(RoleArn=role_arn, RoleSessionName="n-sess-" +
                                   id_generator(),
                                   DurationSeconds=(duration_minutes * 60))
    return response['Credentials']

def assumed_role_name():
    global ROLE_NAME
    if not ROLE_NAME:
        try:
            roleArn = sts().get_caller_identity()['Arn']
            if ":assumed-role/" in roleArn:
                ROLE_NAME = roleArn.split("/")[1]
        except BaseException:
            pass
    return ROLE_NAME

def share_to_another_region(ami_id, regn, ami_name, account_ids, timeout_sec=900):
    if not regn == region():
        resp = ec2(region=regn).copy_image(SourceRegion=region(), SourceImageId=ami_id, Name=ami_name)
        ami_id = resp['ImageId']
    status = "initial"
    start = time.time()
    while status != 'available':
        time.sleep(2)
        if time.time() - start > timeout_sec:
            raise Exception("Failed waiting for status 'available' for " +
                            ami_id + " (timeout: " + str(timeout_sec) + ")")
        try:
            images_resp = ec2(region=regn).describe_images(ImageIds=[ami_id])
            status = images_resp['Images'][0]['State']
        except ClientError:
            print("Did not find image " + ami_id)
    perms = {"Add": []}
    my_acco = resolve_account()
    for acco in account_ids:
        if not acco == my_acco:
            perms['Add'].append({"UserId": acco})
    if len(perms['Add']) > 0:
        ec2(region=regn).modify_image_attribute(ImageId=ami_id, LaunchPermission=perms)

def _has_job_tag(image, image_name_prefix):
    for tag in image['Tags']:
        if re.match('^' + image_name_prefix + '_\\d{4,14}', tag['Value']):
            return True
    return False

def get_images(image_name_prefix, job_tag_function=_has_job_tag):
    image_name_prefix = re.sub(r'\W', '_', image_name_prefix)
    ami_data = ec2().describe_images(Filters=[{'Name': 'tag-value',
                                               'Values': [image_name_prefix + "_*"]}])
    if len(ami_data['Images']) > 0:
        return [image for image in sorted(ami_data['Images'],
                                          key=itemgetter('CreationDate'),
                                          reverse=True)
                if job_tag_function(image, image_name_prefix)]
    else:
        return []

def promote_image(ami_id, job_name):
    image_name_prefix = re.sub(r'\W', '_', job_name)
    build_number = time.strftime("%Y%m%d%H%M%S", time.gmtime())
    if 'BUILD_NUMBER' in os.environ:
        build_number = "%04d" % int(os.environ['BUILD_NUMBER'])
    images_resp = ec2().describe_images(ImageIds=[ami_id])
    ami_name = images_resp['Images'][0]['Name']
    with open("ami.properties", 'w') as ami_props:
        ami_props.write("AMI_ID=" + ami_id + "\nNAME=" + ami_name + "\n")
    ec2().create_tags(Resources=[ami_id], Tags=[{'Key': image_name_prefix,
                                               'Value': image_name_prefix +
                                               "_" + build_number}])


def interpolate_file(file_name, destination=None, stack_name=None,
                     use_vault=False, use_environ=False, skip_stack=False,
                     encoding='utf-8'):
    if not destination:
        destination = file_name
        dstfile = tempfile.NamedTemporaryFile(dir=os.path.dirname(file_name),
                                              prefix=os.path.basename(file_name),
                                              delete=False)
    else:
        dstfile = tempfile.NamedTemporaryFile(dir=os.path.dirname(destination),
                                              prefix=os.path.basename(destination),
                                              delete=False)
    if use_environ:
        params = deepcopy(os.environ)
    else:
        params = {}
    if not stack_name and is_ec2() and not skip_stack:
        params.update(info().stack_data_dict())
    elif stack_name and not skip_stack:
        stack_params, _ = stack_params_and_outputs_and_stack(stack_name=stack_name)
        params.update(stack_params)
    vault = None
    vault_keys = []
    if use_vault:
        vault = Vault()
        vault_keys = vault.list_all()
    with io.open(file_name, "r", encoding=encoding) as _infile:
        with dstfile as _outfile:
            for line in _infile:
                line = _process_line(line, params, vault, vault_keys)
                _outfile.write(line.encode(encoding))
    shutil.copy(dstfile.name, destination)
    os.unlink(dstfile.name)


PARAM_RE = re.compile(r"\$\{([^\$\{\}]*)\}", re.M)
SIMPLE_PARAM_RE = re.compile(r"\$([a-zA-Z0-9_]*)", re.M)
DOUBLE_PARANTHESIS_RE = re.compile(r'\(\(([^)]+)\)\)', re.M)


def _apply_simple_regex(RE, line, params, vault, vault_keys):
    ret = line
    next_start = 0
    match = RE.search(line)
    while match is not None:
        param_value = None
        param_name = match.group(1)
        if param_name in vault_keys:
            param_value = vault.lookup(param_name)
        elif param_name in params:
            param_value = params[param_name]
        else:
            next_start = match.end()
        if not isinstance(param_value, NoneType):
            if isinstance(param_value, OrderedDict):
                return param_value
            else:
                ret = ret[:match.start()] + str(param_value) + ret[match.end():]
        match = RE.search(ret, next_start)
    return ret


def expand_vars(line, params, vault, vault_keys):
    if isinstance(line, OrderedDict) or isinstance(line, dict):
        ret = OrderedDict(list(line.items()))
        if "Fn::" in [x[:4] for x in list(ret.keys()) if isinstance(x, six.string_types)]:
            return expand_only_double_paranthesis_params(ret, params, vault, vault_keys)
        for key, value in list(line.items()):
            if isinstance(key, six.string_types) and key.startswith("Fn::"):
                new_value = expand_only_double_paranthesis_params(value, params, vault, vault_keys)
                ret = OrderedDict([(key, new_value) if k == key else (k, v) for k, v in list(ret.items())])
            else:
                new_key = expand_vars(key, params, vault, vault_keys)
                new_value = expand_vars(value, params, vault, vault_keys)
                ret = OrderedDict([(new_key, new_value) if k == key else (k, v) for k, v in list(ret.items())])
        return ret
    if isinstance(line, list):
        return [expand_vars(x, params, vault, vault_keys) for x in line]
    if isinstance(line, six.string_types):
        ret = _apply_simple_regex(SIMPLE_PARAM_RE, line, params, vault, vault_keys)
        if isinstance(ret, OrderedDict):
            return expand_vars(ret, params, vault, vault_keys)
        ret = _apply_simple_regex(DOUBLE_PARANTHESIS_RE, ret, params, vault, vault_keys)
        if isinstance(ret, OrderedDict):
            return expand_vars(ret, params, vault, vault_keys)
        return _process_line(ret, params, vault, vault_keys)
    return line

def expand_only_double_paranthesis_params(line, params, vault, vault_keys):
    if isinstance(line, OrderedDict) or isinstance(line, dict):
        ret = OrderedDict(list(line.items()))
        for key, value in list(line.items()):
            new_key = expand_only_double_paranthesis_params(key, params, vault, vault_keys)
            new_value = expand_only_double_paranthesis_params(value, params, vault, vault_keys)
            ret = OrderedDict([(new_key, new_value) if k == key else (k, v) for k, v in list(ret.items())])
        return ret
    if isinstance(line, list):
        return [expand_only_double_paranthesis_params(x, params, vault, vault_keys) for x in line]
    if isinstance(line, six.string_types):
        ret = _apply_simple_regex(DOUBLE_PARANTHESIS_RE, line, params, vault, vault_keys)
        if isinstance(ret, OrderedDict):
            return expand_only_double_paranthesis_params(ret, params, vault, vault_keys)
        return ret
    return line

def _process_line(line, params, vault, vault_keys):
    ret = line
    ret = _process_line_re(ret, params, vault, vault_keys, SIMPLE_PARAM_RE)
    ret = _process_line_re(ret, params, vault, vault_keys, DOUBLE_PARANTHESIS_RE)
    ret = _process_line_re(ret, params, vault, vault_keys, PARAM_RE)
    return ret

def _process_line_re(line, params, vault, vault_keys, matcher):
    ret = line
    next_start = 0
    match = matcher.search(line)
    while match is not None:
        param_value = None
        param_name = match.group(1)
        name_arg = None
        for transform in list(VAR_OPERATIONS.keys()):
            if transform in param_name:
                name_arg = param_name.split(transform, 1)
                param_match = name_arg[0]
                param_name = param_match
                name_arg.append(transform)
                break
        if param_name in vault_keys:
            param_value = vault.lookup(param_name)
        elif param_name in params:
            param_value = params[param_name]
        else:
            next_start = match.end()
        if name_arg:
            if param_value and (PARAM_RE.search(param_value) or SIMPLE_PARAM_RE.search(param_value)):
                param_value = None
                next_start = match.end()
            else:
                param_value = VAR_OPERATIONS[name_arg[2]](param_value, name_arg[1])
        if isinstance(param_value, NoneType) or isinstance(param_value, ParamNotAvailable):
            next_start = match.end()
        else:
            if not (ret[:match.start()] + ret[match.end():]).strip():
                return param_value
            else:
                ret = ret[:match.start()] + _to_str(param_value) + ret[match.end():]
        match = matcher.search(ret, next_start)
    return ret


def _var_default(value, arg):
    if value:
        return value
    return arg


def _var_suffix(value, arg):
    if value:
        return re.sub("^" + re.escape(arg[::-1]).replace("\\*", ".*?"), "", value[::-1])[::-1]
    return value


def _var_prefix(value, arg):
    if value:
        return re.sub("^" + re.escape(arg).replace("\\*", ".*?"), "", value)
    return value


def _var_suffix_greedy(value, arg):
    if value:
        return re.sub("^" + re.escape(arg[::-1]).replace("\\*", ".*"), "", value[::-1])[::-1]
    return value


def _var_prefix_greedy(value, arg):
    if value and arg:
        return re.sub("^" + re.escape(arg).replace("\\*", ".*"), "", value)
    return value


def _var_upper(value, arg):
    if value:
        return value.upper()
    return value


def _var_lower(value, arg):
    if value:
        return value.lower()
    return value


def _var_upper_initial(value, arg):
    if value:
        if len(value) > 1:
            return value[0].upper() + value[1:]
        return value[0].upper()
    return value


def _var_lower_initial(value, arg):
    if value:
        if len(value) > 1:
            return value[0].lower() + value[1:]
        return value[0].lower()
    return value


def _var_offset(value, arg):
    if value and arg:
        ind_len = arg.split(":")
        if len(ind_len) == 2:
            start = int(ind_len[0])
            end = start + (int(ind_len[1]))
            return value[start:end]
    return value


def _var_subst(value, arg):
    if value and arg:
        subst_repl = arg.split("/")
        if len(subst_repl) == 2:
            return value.replace(subst_repl[0], subst_repl[1])
    return value


VAR_OPERATIONS = OrderedDict()
VAR_OPERATIONS[":-"] = _var_default
VAR_OPERATIONS["##"] = _var_prefix_greedy
VAR_OPERATIONS["%%"] = _var_suffix_greedy
VAR_OPERATIONS["#"] = _var_prefix
VAR_OPERATIONS["%"] = _var_suffix
VAR_OPERATIONS["^^"] = _var_upper
VAR_OPERATIONS[",,"] = _var_lower
VAR_OPERATIONS["^"] = _var_upper_initial
VAR_OPERATIONS[","] = _var_lower_initial
VAR_OPERATIONS[":"] = _var_offset
VAR_OPERATIONS["/"] = _var_subst


def has_output_selector(stack, outputname, mapper):
    if 'Outputs' not in stack:
        return False
    for output in stack['Outputs']:
        if output['OutputKey'] == outputname:
            return mapper(stack)
    return False


def select_stacks(selector):
    ret = []
    paginator = cloudformation().get_paginator('describe_stacks')
    for page in paginator.paginate():
        for stack in page.get('Stacks'):
            selected = selector(stack)
            if selected:
                ret.append(selected)
    return ret

def read_if_readable(filename):
    try:
        if os.path.isfile(filename):
            with open(filename) as read_file:
                return read_file.read()
        else:
            return ""
    except:
        return ""

def session_token(duration_minutes=60, token_arn=None, token_value=None):
    if "AWS_SESSION_TOKEN" in os.environ:
        return None
    args = {"DurationSeconds": 3600}

    if duration_minutes:
        args["DurationSeconds"] = duration_minutes * 60
    if token_arn and  token_value:
        args["SerialNumber"] = token_arn
        args["TokenCode"] = token_value

    ret = sts().get_session_token(**args)
    if "Credentials" not in ret:
        return None
    else:
        return ret["Credentials"]
