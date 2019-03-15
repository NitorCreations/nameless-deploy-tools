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
from __future__ import print_function

from builtins import str
from builtins import range
from builtins import object
import io
import json
import os
import random
import re
import shutil
import stat
import string
import sys
import tempfile
import time
import tempfile
import six
from copy import deepcopy
from collections import deque, OrderedDict
from os.path import expanduser
from threading import Event, Lock, Thread
from operator import itemgetter

import boto3
from botocore.exceptions import ClientError, EndpointConnectionError
import requests
from requests.exceptions import ConnectionError
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from n_vault import Vault
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

def get_retry(url, retries=5, backoff_factor=0.3,
              status_forcelist=(500, 502, 504), session=None, timeout=5):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session.get(url, timeout=5)


def wait_net_service(server, port, timeout=None):
    """ Wait for network service to appear
        @param timeout: in seconds, if None or 0 wait forever
        @return: True of False, if timeout is None may return only True or
                 throw unhandled network exception
    """
    import socket
    import errno
    s = socket.socket()
    if sys.version < "3":
        # Just make this something that will not be throwns since python 2
        # just has socket.error
        ConnectionRefusedError = EndpointConnectionError
    if timeout:
        from time import time as now
        # time module is needed to calc timeout shared between two exceptions
        end = now() + timeout
    while True:
        try:
            if timeout:
                next_timeout = end - now()
                if next_timeout < 0:
                    return False
                else:
                    s.settimeout(next_timeout)
            s.connect((server, port))
        except socket.timeout as err:
            # this exception occurs only if timeout is set
            if timeout:
                return False
        except ConnectionRefusedError:
            s.close()
            return False
        except socket.error as err:
            # catch timeout exception from underlying network library
            # this one is different from socket.timeout
            if not isinstance(err.args, tuple) or err[0] != errno.ETIMEDOUT or err[0] != errno.ECONNREFUSED:
                raise
            elif err[0] == errno.ECONNREFUSED:
                s.close()
                return False
        else:
            s.close()
            return True


class InstanceInfo(object):
    """ A class to get the relevant metadata for an instance running in EC2
        firstly from the metadata service and then from EC2 tags and then
        from the CloudFormation template that created this instance

        The info is then cached in /opt/nameless/instance-data.json on linux and
        in  C:\\nameless\\instance-data.json on windows.
    """
    _info = {}

    def stack_name(self):
        if 'stack_name' in self._info:
            return self._info['stack_name']
        else:
            return None

    def stack_id(self):
        if 'stack_id' in self._info:
            return self._info['stack_id']
        else:
            return None

    def instance_id(self):
        if 'instanceId' in self._info:
            return self._info['instanceId']
        else:
            return None

    def region(self):
        if 'region' in self._info:
            return self._info['region']
        else:
            return None

    def initial_status(self):
        if 'initial_status' in self._info:
            return self._info['initial_status']
        else:
            return None

    def logical_id(self):
        if 'logical_id' in self._info:
            return self._info['logical_id']
        else:
            return None

    def availability_zone(self):
        if 'availabilityZone' in self._info:
            return self._info['availabilityZone']
        else:
            return None

    def private_ip(self):
        if 'privateIp' in self._info:
            return self._info['privateIp']
        else:
            return None

    def tag(self, name):
        if 'Tags' in self._info and name in self._info['Tags']:
            return self._info['Tags'][name]
        else:
            return None

    def clear_cache(self):
        if os.path.isfile(INSTANCE_DATA_LINUX):
            os.remove(INSTANCE_DATA_LINUX)
        if os.path.isfile(INSTANCE_DATA_WIN):
            os.remove(INSTANCE_DATA_WIN)
        self._info = None
        self.__init__()

    def __init__(self):
        if os.path.isfile(INSTANCE_DATA_LINUX) and \
           time.time() - os.path.getmtime(INSTANCE_DATA_LINUX) < 900:
            try:
                self._info = json.load(open(INSTANCE_DATA_LINUX))
            except BaseException:
                pass
        if os.path.isfile(INSTANCE_DATA_WIN) and \
           time.time() - os.path.getmtime(INSTANCE_DATA_WIN) < 900:
            try:
                self._info = json.load(open(INSTANCE_DATA_WIN))
            except BaseException:
                pass
        if not self._info and is_ec2():
            try:
                if not wait_net_service("169.254.169.254", 80, 120):
                    raise Exception("Failed to connect to instance identity service")
                response = get_retry(INSTANCE_IDENTITY_URL)
                self._info = json.loads(response.text)
                os.environ['AWS_DEFAULT_REGION'] = self.region()
                ec2 = boto3.client('ec2')
                tags = {}
                tag_response = None
                retry = 0
                while not tag_response and retry < 20:
                    try:
                        tag_response = ec2.describe_tags(Filters=[{'Name': 'resource-id',
                                                                   'Values': [self.instance_id()]}])
                    except (ConnectionError, EndpointConnectionError):
                        retry = retry + 1
                        time.sleep(1)
                        continue
                    except ClientError:
                        tag_response = { 'Tags': [] }
                for tag in tag_response['Tags']:
                    tags[tag['Key']] = tag['Value']
                self._info['Tags'] = tags
                if 'aws:cloudformation:stack-name' in self._info['Tags']:
                    self._info['stack_name'] = tags['aws:cloudformation:stack-name']
                if 'aws:cloudformation:stack-id' in self._info['Tags']:
                    self._info['stack_id'] = tags['aws:cloudformation:stack-id']
                if self.stack_name():
                    stack_parameters, stack = stack_params_and_outputs_and_stack(region(), self.stack_name())
                    self._info['StackData'] = stack_parameters
                    self._info['FullStackData'] = stack
            except ConnectionError:
                self._info = {}
            info_file = None
            info_file_dir = None
            info_file_parent = None
            if os.path.isdir('C:/'):
                info_file_parent = 'C:/'
                info_file_dir = 'C:/nameless'
            else:
                info_file_parent = '/opt'
                info_file_dir = '/opt/nameless'
            if not os.path.isdir(info_file_dir) and os.access(info_file_parent, os.W_OK):
                os.makedirs(info_file_dir)
            if not os.access(info_file_dir, os.W_OK):
                home = expanduser("~")
                info_file_dir = home + "/.ndt"
            if not os.path.isdir(info_file_dir) and os.access(info_file_parent, os.W_OK):
                os.makedirs(info_file_dir)
            if os.access(info_file_dir, os.W_OK):
                info_file = info_file_dir + '/instance-data.json'
                with open(info_file, 'w') as outf:
                    outf.write(json.dumps(self._info, skipkeys=True, indent=2, default=dthandler))
                try:
                    os.chmod(info_file, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP |
                             stat.S_IWGRP | stat.S_IROTH | stat.S_IWOTH)
                    os.chmod(info_file_dir, stat.S_IRUSR | stat.S_IWUSR |
                             stat.S_IXUSR | stat.S_IRGRP | stat.S_IWGRP |
                             stat.S_IXGRP | stat.S_IROTH | stat.S_IWOTH |
                             stat.S_IXOTH)
                except BaseException:
                    pass
        if self.region():
            os.environ['AWS_DEFAULT_REGION'] = self.region()
        if 'FullStackData' in self._info and 'StackStatus' in self._info['FullStackData']:
            self._info['initial_status'] = self._info['FullStackData']['StackStatus']
        if 'Tags' in self._info:
            tags = self._info['Tags']
            if 'aws:cloudformation:stack-name' in tags:
                self._info['stack_name'] = tags['aws:cloudformation:stack-name']
            if 'aws:cloudformation:stack-id' in tags:
                self._info['stack_id'] = tags['aws:cloudformation:stack-id']
            if 'aws:cloudformation:logical-id' in tags:
                self._info['logical_id'] = tags['aws:cloudformation:logical-id']

    def stack_data_dict(self):
        if 'StackData' in self._info:
            return self._info['StackData']

    def stack_data(self, name):
        if 'StackData' in self._info:
            if name in self._info['StackData']:
                return self._info['StackData'][name]
        return ''

    def __str__(self):
        return json.dumps(self._info, skipkeys=True)


class IntervalThread(Thread):
    def __init__(self, event, interval, call_function):
        Thread.__init__(self)
        self._stopped = event
        self._interval = interval
        self._call_function = call_function

    def run(self):
        while not self._stopped.wait(self._interval):
            self._call_function()


class LogSender(object):
    def __init__(self, file_name):
        info = InstanceInfo()
        self._lock = Lock()
        self._send_lock = Lock()
        self._logs = boto3.client('logs')
        self.group_name = info.stack_name()
        self._messages = deque()
        self.stream_name = info.instance_id() + "|" + \
            file_name.replace(':', '_').replace('*', '_')
        try:
            self._logs.create_log_group(logGroupName=self.group_name)
        except BaseException:
            pass
        try:
            self._logs.create_log_stream(logGroupName=self.group_name,
                                         logStreamName=self.stream_name)
        except BaseException:
            pass
        self.token = None
        self.send(str(info))
        self._do_send()
        self._stop_flag = Event()
        self._thread = IntervalThread(self._stop_flag, 2, self._do_send)
        self._thread.start()

    def send(self, line):
        try:
            self._lock.acquire()
            if isinstance(line, bytes):
                line = line.decode('utf-8', 'replace')
            self._messages.append(line.rstrip())
            if 'CLOUDWATCH_LOG_DEBUG' in os.environ:
                print("Queued message")
        finally:
            self._lock.release()

    def _do_send(self):
        events = []
        try:
            self._lock.acquire()
            if len(self._messages) == 0:
                return
            counter = 0
            while len(self._messages) > 0 and counter < 1048576 and \
                    len(events) < 10000:
                message = self._messages.popleft()
                counter = counter + len(message.encode('utf-8', 'replace')) + 26
                if counter > 1048576:
                    self._messages.appendleft(message)
                elif message:
                    event = {}
                    event['timestamp'] = int(time.time() * 1000)
                    event['message'] = message
                    events.append(event)
        finally:
            self._lock.release()
        if len(events) == 0:
            return
        try:
            self._send_lock.acquire()
            if not self.token:
                stream_desc = self._logs.describe_log_streams(logGroupName=self.group_name,
                                                              logStreamNamePrefix=self.stream_name)
                if 'uploadSequenceToken' in stream_desc['logStreams'][0]:
                    self.token = stream_desc['logStreams'][0]['uploadSequenceToken']
            if self.token:
                log_response = self._logs.put_log_events(logGroupName=self.group_name,
                                                         logStreamName=self.stream_name,
                                                         logEvents=events,
                                                         sequenceToken=self.token)
            else:
                log_response = self._logs.put_log_events(logGroupName=self.group_name,
                                                         logStreamName=self.stream_name,
                                                         logEvents=events)
            if 'CLOUDWATCH_LOG_DEBUG' in os.environ:
                print("Sent " + str(len(events)) + " messages to " + self.stream_name)
            self.token = log_response['nextSequenceToken']
        except ClientError:
            self.token = None
            for event in events:
                self.send(event['message'].encode('utf-8', 'replace'))
        finally:
            self._send_lock.release()


def send_logs_to_cloudwatch(file_name):
    info = InstanceInfo()
    stack_name = info.stack_name()
    while not stack_name:
        time.sleep(1)
        info.clear_cache()
        stack_name = info.stack_name()
    log_sender = LogSender(file_name)
    read_and_follow(file_name, log_sender.send)


def read_and_follow(file_name, line_function, wait=1):
    while not (os.path.isfile(file_name) and os.path.exists(file_name)):
        time.sleep(wait)
    with open(file_name) as file_:
        end_seen = False
        while True:
            curr_position = file_.tell()
            line = file_.readline()
            if not line:
                file_.seek(curr_position)
                end_seen = True
            else:
                line_function(line)
                end_seen = False
            if end_seen:
                time.sleep(wait)


def signal_status(status, resource_name=None):
    info = InstanceInfo()
    clf = boto3.client('cloudformation')
    if not resource_name:
        resource_name = info.logical_id()
    print("Signalling " + status + " for " + info.stack_name() + "." + resource_name)
    clf.signal_resource(StackName=info.stack_name(),
                        LogicalResourceId=resource_name,
                        UniqueId=info.instance_id(),
                        Status=status)


def associate_eip(eip=None, allocation_id=None, eip_param="paramEip",
                  allocation_id_param="paramEipAllocationId"):
    if not eip_param:
        eip_param = "paramEip"
    if not allocation_id_param:
        allocation_id_param = "paramEipAllocationId"
    info = InstanceInfo()
    if not allocation_id:
        if eip:
            ec2 = boto3.client('ec2')
            address_data = ec2.describe_addresses(PublicIps=[eip])
            if 'Addresses' in address_data and \
               len(address_data['Addresses']) > 0 and \
               'AllocationId' in address_data['Addresses'][0]:
                allocation_id = address_data['Addresses'][0]['AllocationId']
    if not allocation_id:
        allocation_id = info.stack_data(allocation_id_param)
    if not allocation_id:
        eip = info.stack_data(eip_param)
        ec2 = boto3.client('ec2')
        address_data = ec2.describe_addresses(PublicIps=[eip])
        if 'Addresses' in address_data and len(address_data['Addresses']) > 0 \
           and 'AllocationId' in address_data['Addresses'][0]:
            allocation_id = address_data['Addresses'][0]['AllocationId']
    print("Allocating " + allocation_id + " on " + info.instance_id())
    ec2 = boto3.client('ec2')
    ec2.associate_address(InstanceId=info.instance_id(),
                          AllocationId=allocation_id,
                          AllowReassociation=True)


def init():
    info = InstanceInfo()
    return str(info)


def get_userdata(outfile):
    response = get_retry(USER_DATA_URL)
    if outfile == "-":
        print(response.text)
    else:
        with open(outfile, 'w') as outf:
            outf.write(response.text)


def id_generator(size=10, chars=string.ascii_uppercase + string.digits +
                 string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))


def assume_role(role_arn, mfa_token_name=None, duration_minutes=60):
    sts = boto3.client("sts")
    if mfa_token_name:
        token = mfa_read_token(mfa_token_name)
        code = mfa_generate_code(mfa_token_name)
        response = sts.assume_role(RoleArn=role_arn,
                                   RoleSessionName="n-sess-" + id_generator(),
                                   SerialNumber=token['token_arn'],
                                   TokenCode=code,
                                   DurationSeconds=(duration_minutes * 60))
    else:
        response = sts.assume_role(RoleArn=role_arn, RoleSessionName="n-sess-" +
                                   id_generator(),
                                   DurationSeconds=(duration_minutes * 60))
    return response['Credentials']


def resolve_account():
    global ACCOUNT_ID
    if not ACCOUNT_ID:
        try:
            sts = boto3.client("sts")
            ACCOUNT_ID = sts.get_caller_identity()['Account']
        except BaseException:
            pass
    return ACCOUNT_ID

def assumed_role_name():
    global ROLE_NAME
    if not ROLE_NAME:
        try:
            sts = boto3.client("sts")
            roleArn = sts.get_caller_identity()['Arn']
            if ":assumed-role/" in roleArn:
                ROLE_NAME = roleArn.split("/")[1]
        except BaseException:
            pass
    return ROLE_NAME


def is_ec2():
    if sys.platform.startswith("win"):
        import wmi
        systeminfo = wmi.WMI().Win32_ComputerSystem()[0]
        return "EC2" == systeminfo.PrimaryOwnerName
    elif sys.platform.startswith("linux"):
        if read_if_readable("/sys/hypervisor/uuid").startswith("ec2"):
            return True
        elif read_if_readable("/sys/class/dmi/id/product_uuid").startswith("EC2"):
            return True
        elif read_if_readable("/sys/devices/virtual/dmi/id/board_vendor").startswith("Amazon EC2"):
            return True
        elif read_if_readable("/sys/devices/virtual/dmi/id/sys_vendor").startswith("Amazon EC2"):
            return True
        elif read_if_readable("/sys/devices/virtual/dmi/id/sys_vendor").startswith("Amazon EC2"):
            return True
        elif read_if_readable("/sys/devices/virtual/dmi/id/bios_vendor").startswith("Amazon EC2"):
            return True
        elif read_if_readable("/sys/devices/virtual/dmi/id/chassis_vendor").startswith("Amazon EC2"):
            return True
        elif read_if_readable("/sys/devices/virtual/dmi/id/chassis_asset_tag").startswith("Amazon EC2"):
            return True
        elif "AmazonEC2" in read_if_readable("/sys/devices/virtual/dmi/id/modalias"):
            return True 
        elif "AmazonEC2" in read_if_readable("/sys/devices/virtual/dmi/id/uevent"):
            return True
        else:
            return False

def region():
    """ Get default region - the region of the instance if run in an EC2 instance
    """
    # If it is set in the environment variable, use that
    if 'AWS_DEFAULT_REGION' in os.environ:
        return os.environ['AWS_DEFAULT_REGION']
    else:
        # Otherwise it might be configured in AWS credentials
        session = boto3.session.Session()
        if session.region_name:
            return session.region_name
        # If not configured and being called from an ec2 instance, use the
        # region of the instance
        elif is_ec2():
            info = InstanceInfo()
            return info.region()
        # Otherwise default to Ireland
        else:
            return 'eu-west-1'


def regions():
    """Get all region names as a list"""
    ec2 = boto3.client("ec2")
    response = ec2.describe_regions()
    for regn in response['Regions']:
        yield regn['RegionName']


def stacks():
    """Get list of stack names for the currently default region"""
    set_region()
    pages = boto3.client("cloudformation").get_paginator('describe_stacks')
    for page in pages.paginate():
        for stack in page.get('Stacks', []):
            yield stack['StackName']


def stack_params_and_outputs(regn, stack_name):
    """ Get parameters and outputs from a stack as a single dict
    """
    params, _ = stack_params_and_outputs_and_stack(regn, stack_name)
    return params


def stack_params_and_outputs_and_stack(regn, stack_name):
    """ Get parameters and outputs from a stack as a single dict and the full stack
    """
    cloudformation = boto3.client("cloudformation", region_name=regn)
    retry = 0
    stack = {}
    resources = {}
    while not stack and retry < 10:
        try:
            stack = cloudformation.describe_stacks(StackName=stack_name)
            stack = stack['Stacks'][0]
        except (ConnectionError, EndpointConnectionError):
            retry = retry + 1
            time.sleep(1)
            continue
        except ClientError:
            break
    if not stack:
        return {}, {}
    retry = 0
    while not resources and retry < 3:
        try:
            resources = cloudformation.describe_stack_resources(StackName=stack_name)
        except ClientError:
            break
        except (ConnectionError, EndpointConnectionError):
            retry = retry + 1
            time.sleep(1)
            continue
    resp = {}
    if 'CreationTime' in stack:
        stack['CreationTime'] = time.strftime("%a, %d %b %Y %H:%M:%S +0000",
                                              stack['CreationTime'].timetuple())
    if 'LastUpdatedTime' in stack:
        stack['LastUpdatedTime'] = time.strftime("%a, %d %b %Y %H:%M:%S +0000",
                                                 stack['LastUpdatedTime'].timetuple())
    if "StackResources" in resources:
        for resource in resources["StackResources"]:
            resp[resource['LogicalResourceId']] = resource['PhysicalResourceId']
    if 'Parameters' in stack:
        for param in stack['Parameters']:
            resp[param['ParameterKey']] = param['ParameterValue']
    if 'Outputs' in stack:
        for output in stack['Outputs']:
            resp[output['OutputKey']] = output['OutputValue']
    return resp, stack


def set_region():
    """ Sets the environment variable AWS_DEFAULT_REGION if not already set
        to a sensible default
    """
    if 'AWS_DEFAULT_REGION' not in os.environ:
        os.environ['AWS_DEFAULT_REGION'] = region()


def share_to_another_region(ami_id, regn, ami_name, account_ids, timeout_sec=900):
    ec2 = boto3.client('ec2', region_name=regn)
    if not regn == region():
        resp = ec2.copy_image(SourceRegion=region(), SourceImageId=ami_id,
                              Name=ami_name)
        ami_id = resp['ImageId']
    status = "initial"
    start = time.time()
    while status != 'available':
        time.sleep(2)
        if time.time() - start > timeout_sec:
            raise Exception("Failed waiting for status 'available' for " +
                            ami_id + " (timeout: " + str(timeout_sec) + ")")
        images_resp = ec2.describe_images(ImageIds=[ami_id])
        status = images_resp['Images'][0]['State']
    perms = {"Add": []}
    my_acco = resolve_account()
    for acco in account_ids:
        if not acco == my_acco:
            perms['Add'].append({"UserId": acco})
    if len(perms['Add']) > 0:
        ec2.modify_image_attribute(ImageId=ami_id, LaunchPermission=perms)

def _has_job_tag(image, image_name_prefix):
    for tag in image['Tags']:
        if re.match('^' + image_name_prefix + '_\\d{4,14}', tag['Value']):
            return True
    return False

def get_images(image_name_prefix, job_tag_function=_has_job_tag):
    image_name_prefix = re.sub(r'\W', '_', image_name_prefix)
    ec2 = boto3.client('ec2')
    ami_data = ec2.describe_images(Filters=[{'Name': 'tag-value',
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
    set_region()
    build_number = time.strftime("%Y%m%d%H%M%S", time.gmtime())
    if 'BUILD_NUMBER' in os.environ:
        build_number = "%04d" % int(os.environ['BUILD_NUMBER'])
    ec2 = boto3.client('ec2')
    images_resp = ec2.describe_images(ImageIds=[ami_id])
    ami_name = images_resp['Images'][0]['Name']
    with open("ami.properties", 'w') as ami_props:
        ami_props.write("AMI_ID=" + ami_id + "\nNAME=" + ami_name + "\n")
    ec2.create_tags(Resources=[ami_id], Tags=[{'Key': image_name_prefix,
                                               'Value': image_name_prefix +
                                               "_" + build_number}])


def register_private_dns(dns_name, hosted_zone, ttl=None):
    set_region()
    if not ttl:
        ttl=60
    else:
        ttl=int(ttl)
    zone_id = None
    zone_paginator = boto3.client("route53").get_paginator("list_hosted_zones")
    for page in zone_paginator.paginate():
        for zone in page.get("HostedZones", []):
            if zone["Name"] == hosted_zone:
                zone_id = zone['Id']
                break
        if zone_id:
            break
    if not zone_id:
        raise Exception("Failed to get zone id for zone " + hosted_zone)
    info = InstanceInfo()
    route53 = boto3.client("route53")
    route53.change_resource_record_sets(HostedZoneId=zone_id, ChangeBatch={
        "Changes": [
            {
                "Action": "UPSERT",
                "ResourceRecordSet": {
                    "Name": dns_name,
                    "Type": "A",
                    "TTL": ttl,
                    "ResourceRecords": [
                        {
                            "Value": info.private_ip()
                        }
                    ]
                }
            }
        ]})


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
        info = InstanceInfo()
        params.update(info.stack_data_dict())
    elif stack_name and not skip_stack:
        params.update(stack_params_and_outputs(region(), stack_name))
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
        if "Fn::" in [x[:4] for x in list(ret.keys())]:
            return expand_only_double_paranthesis_params(ret, params, vault, vault_keys)
        for key, value in list(line.items()):
            if key.startswith("Fn::"):
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
            ret = ret[:match.start()] + param_value + ret[match.end():]
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
    paginator = boto3.client('cloudformation').get_paginator('describe_stacks')
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
    args = {"DurationSeconds": 3600}

    if duration_minutes:
        args["DurationSeconds"] = duration_minutes * 60
    if token_arn and  token_value:
        args["SerialNumber"] = token_arn
        args["TokenCode"] = token_value

    sts = boto3.client("sts")

    ret = sts.get_session_token(**args)
    if "Credentials" not in ret:
        return None
    else:
        return ret["Credentials"]