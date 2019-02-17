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

from builtins import object
from builtins import str
import collections
import hashlib
import locale
import os
import re
import sys
import time
import six
from datetime import datetime
import boto3

from botocore.exceptions import ClientError
from pygments import highlight, lexers, formatters
from pygments.styles import get_style_by_name
from termcolor import colored

from n_utils import aws_infra_util
from n_utils.cf_utils import get_images
from n_utils.log_events import CloudWatchLogsThread, CloudFormationEvents, fmttime

REDIRECTED = False


def log_data(data, output_format="yaml"):
    if output_format == "yaml":
        formatted = aws_infra_util.yaml_save(data)
    else:
        formatted = aws_infra_util.json_save(data)
    lexer = lexers.get_lexer_by_name(output_format)
    formatter = formatters.get_formatter_by_name("256")
    formatter.__init__(style=get_style_by_name('emacs'))
    if not isinstance(formatted, six.string_types):
        formatted = str(formatted, 'UTF-8')
    colored_yaml = os.linesep + highlight(formatted, lexer, formatter)
    log(colored_yaml)

def log(message):
    os.write(1, (colored(fmttime(datetime.now()), 'yellow') + " "
                 + message + os.linesep).encode(locale.getpreferredencoding()))


def update_stack(stack_name, template, params, dry_run=False, session=None, tags=None):
    if session:
        clf = session.client('cloudformation')
    else:
        clf = boto3.client('cloudformation')
    chset_name = stack_name + "-" + time.strftime("%Y%m%d%H%M%S",
                                                  time.gmtime())
    params = get_template_arguments(stack_name, template, params)
    params['ChangeSetName'] = chset_name
    if tags:
        params["Tags"] = tags
    chset_id = clf.create_change_set(**params)['Id']
    chset_data = clf.describe_change_set(ChangeSetName=chset_id)
    status = chset_data['Status']
    while "_COMPLETE" not in status and status != "FAILED":
        time.sleep(5)
        chset_data = clf.describe_change_set(ChangeSetName=chset_id)
        status = chset_data['Status']
    if status == "FAILED":
        clf.delete_change_set(ChangeSetName=chset_id)
        if 'StatusReason' in chset_data \
                and "The submitted information didn't contain changes" in chset_data['StatusReason']:
            failed_for_real = False
        else:
            failed_for_real = True
        if 'StatusReason' in chset_data:
            if failed_for_real:
                log_str = "\033[31;1mFAILED: " + chset_data['StatusReason'] + "\033[m"
            else:
                log_str = chset_data['StatusReason']
            log(log_str)
        if failed_for_real:
            raise Exception("Creating changeset failed")
    else:
        chset_data['CreationTime'] = time.strftime("%a, %d %b %Y %H:%M:%S +0000",
                                                   chset_data['CreationTime'].timetuple())
        log("\033[32;1m*** Changeset ***:\033[m")
        log_data(chset_data)
        if not dry_run:
            clf.execute_change_set(ChangeSetName=chset_id)
        else:
            clf.delete_change_set(ChangeSetName=chset_id)
    return


def create_stack(stack_name, template, params, session=None, tags=None):
    if session:
        clf = session.client('cloudformation')
    else:
        clf = boto3.client('cloudformation')
    params = get_template_arguments(stack_name, template, params)
    if tags:
        params["Tags"] = tags
    clf.create_stack(**params)
    return


def get_stack_operation(stack_name, session=None):
    if session:
        clf = session.client('cloudformation')
    else:
        clf = boto3.client('cloudformation')
    stack_oper = "create_stack"
    try:
        stack_data = clf.describe_stacks(StackName=stack_name)
        # Dump original status, for the record
        status = stack_data['Stacks'][0]['StackStatus']
        log("Status: \033[32;1m" + status + "\033[m")
        stack_oper = "update_stack"
    except ClientError as err:
        if err.response['Error']['Code'] == 'ValidationError' and \
           err.response['Error']['Message'].endswith('does not exist'):
            log("Status: \033[32;1mNEW_STACK\033[m")
        else:
            raise
    return globals()[stack_oper]


def get_end_status(stack_name, session=None):
    logs = CloudWatchLogsThread(log_group_name=stack_name)
    logs.start()
    cf_events = CloudFormationEvents(log_group_name=stack_name)
    cf_events.start()
    log("Waiting for stack operation to complete:")
    if session:
        clf = session.client('cloudformation')
    else:
        clf = boto3.client('cloudformation')
    status = "_IN_PROGRESS"
    while True:
        stack_info = clf.describe_stacks(StackName=stack_name)
        status = stack_info['Stacks'][0]['StackStatus']
        if "ROLLBACK" in status:
            color = "\033[31;1m"
        else:
            color = "\033[32;1m"
        log(color + "Status: " + status + "\033[m")
        if not status.endswith("_IN_PROGRESS"):
            logs.stop()
            cf_events.stop()
            break
        time.sleep(5)
    return status


def create_or_update_stack(stack_name, json_small, params_doc, session=None, tags=None):
    stack_func = get_stack_operation(stack_name, session=session)
    stack_func(stack_name, json_small, params_doc, session=session, tags=tags)
    return get_end_status(stack_name, session=session)


def get_template_arguments(stack_name, template, params, session=None):
    params = {"StackName": stack_name,
              "Parameters": params, "Capabilities": ["CAPABILITY_IAM", "CAPABILITY_NAMED_IAM"]}
    if 'CF_BUCKET' in os.environ and os.environ['CF_BUCKET']:
        bucket = os.environ['CF_BUCKET']
        if session:
            s3cli = session.client('s3')
        else:
            s3cli = boto3.client('s3')
        template_hash = hashlib.md5()
        template_hash.update(template)
        template_hash.update(aws_infra_util.json_save_small(params))
        key = stack_name + '-' + template_hash.hexdigest()
        s3cli.put_object(Body=template, Bucket=bucket, Key=key)
        params['TemplateURL'] = "https://s3.amazonaws.com/" + bucket + "/" + key
    else:
        params["TemplateBody"] = template
    return params


def delete(stack_name, regn, session=None):
    os.environ['AWS_DEFAULT_REGION'] = regn
    log("**** Deleting stack '" + stack_name + "'")
    if session:
        clf = session.client('cloudformation')
    else:
        clf = boto3.client('cloudformation')
    cf_events = CloudFormationEvents(log_group_name=stack_name)
    cf_events.start()
    clf.delete_stack(StackName=stack_name)
    while True:
        try:
            stack_info = clf.describe_stacks(StackName=stack_name)
            status = stack_info['Stacks'][0]['StackStatus']
            if not status.endswith("_IN_PROGRESS") and not status.endswith("_COMPLETE"):
                raise Exception("Delete stack failed: end state " + status)
            log("Status: \033[32;1m" + status + "\033[m")
            time.sleep(5)
        except ClientError as err:
            cf_events.stop()
            if err.response['Error']['Code'] == 'ValidationError' and \
               err.response['Error']['Message'].endswith('does not exist'):
                log("Status: \033[32;1mDELETE_COMPLETE\033[m")
                break
            else:
                raise


def resolve_ami(template_doc, session=None):
    ami_id = ""
    ami_name = ""
    ami_created = ""
    if 'AMI_ID' in os.environ and os.environ['AMI_ID']:
        ami_id = os.environ['AMI_ID']

    if not ami_id and 'Parameters' in template_doc and \
        'paramAmi' in template_doc['Parameters'] and \
            'IMAGE_JOB' in os.environ:
        image_job = re.sub(r'\W', '_', os.environ['IMAGE_JOB'].lower())
        log("Looking for ami with name prefix " + image_job)
        sorted_images = get_images(image_job)
        if sorted_images:
            image = sorted_images[0]
            ami_id = image['ImageId']
            ami_name = image['Name']
            ami_created = image['CreationDate']
    elif ami_id and 'Parameters' in template_doc and \
            'paramAmi'in template_doc['Parameters']:
        log("Looking for ami metadata with id " + ami_id)
        if session:
            ec2 = session.client('ec2')
        else:
            ec2 = boto3.client('ec2')
        ami_meta = ec2.describe_images(ImageIds=[ami_id])
        log("Result: " + aws_infra_util.json_save(ami_meta))
        image = ami_meta['Images'][0]
        ami_name = image['Name']
        ami_created = image['CreationDate']
    return ami_id, ami_name, ami_created


def deploy(stack_name, yaml_template, regn, dry_run=False, session=None):
    os.environ['AWS_DEFAULT_REGION'] = regn
    os.environ['REGION'] = regn
    global REDIRECTED
    if not REDIRECTED:
        # Disable buffering, from http://stackoverflow.com/questions/107705/disable-output-buffering
        sys.stdout = Unbuffered(sys.__stdout__)
        REDIRECTED = True
    template_doc = aws_infra_util.yaml_to_dict(yaml_template)
    ami_id, ami_name, ami_created = resolve_ami(template_doc, session=session)

    log("**** Deploying stack '" + stack_name + "' with template '" +
        yaml_template + "' and ami_id '" + str(ami_id) + "'")

    if "Parameters" not in template_doc:
        template_doc['Parameters'] = {}

    template_parameters = template_doc['Parameters']
    tags = []
    if "Tags" in template_doc:
        tags = template_doc["Tags"]
        del template_doc["Tags"]
    if ami_id:
        with open("ami.properties", 'w') as ami_props:
            ami_props.write("AMI_ID=" + ami_id + "\nNAME=" + ami_name + "\n")
        os.environ["paramAmi"] = ami_id
        os.environ["paramAmiName"] = ami_name
        os.environ["paramAmiCreated"] = ami_created
        if "paramAmiName" not in template_parameters:
            template_parameters['paramAmiName'] = \
                collections.OrderedDict([("Description", "AMI Name"),
                                         ("Type", "String"), ("Default", "")])
        if "paramAmiCreated" not in template_parameters:
            template_parameters['paramAmiCreated'] = \
                collections.OrderedDict([("Description", "AMI Creation Date"),
                                         ("Type", "String"), ("Default", "")])
    else:
        with open("ami.properties", 'w') as ami_props:
            ami_props.write("AMI_ID=\nNAME=\n")
    json_small = aws_infra_util.json_save_small(template_doc)

    log("**** Final template ****")
    log_data(template_doc, output_format="json")

    # Create/update stack
    params_doc = []
    for key in list(template_parameters.keys()):
        if key in os.environ:
            val = os.environ[key]
            log("Parameter " + key + ": using \033[32;1mCUSTOM value " +
                val + "\033[m")
            params_doc.append({'ParameterKey': key, 'ParameterValue': val})
        else:
            val = template_parameters[key]['Default']
            log("Parameter " + key + ": using default value " + str(val))

    if not dry_run:
        status = create_or_update_stack(stack_name, json_small, params_doc, session=session, tags=tags)
        if not (status == "CREATE_COMPLETE" or status == "UPDATE_COMPLETE"):
            sys.exit("Stack operation failed: end state " + status)
    elif get_stack_operation(stack_name).__name__ == "update_stack":
        update_stack(stack_name, json_small, params_doc, dry_run=True, session=session, tags=tags)
    log("Done!")


class Unbuffered(object):
    def __init__(self, stream):
        self.stream = stream
        self.SYS_ENCODING = locale.getpreferredencoding(False)
        if self.SYS_ENCODING == "ascii" or self.SYS_ENCODING == "US-ASCII":
            self.SYS_ENCODING = "ISO8859-15"

    def write(self, data):
        if isinstance(data, six.string_types):
            self.stream.write(data)
        elif isinstance(data, bytes):
            self.stream.write(data.decode(self.SYS_ENCODING))
        else:
            self.stream.write(str(data))
        self.stream.flush()

    def writelines(self, datas):
        self.stream.writelines(datas)
        self.stream.flush()

    def __getattr__(self, attr):
        return getattr(self.stream, attr)
