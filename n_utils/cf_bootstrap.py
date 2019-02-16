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

""" Utilities to bootsrap AWS accounts into use with nameless-deploy-tools
"""
from __future__ import print_function

from builtins import zip
from builtins import input
from builtins import str
from builtins import object
import os
import random
import re
import shutil
import subprocess
import stat
import sys
from copy import deepcopy
from collections import OrderedDict
from subprocess import Popen, PIPE

import argparse
import argcomplete
from argcomplete.completers import ChoicesCompleter

import boto3
import ipaddr
from awscli.customizations.configure.writer import ConfigFileWriter
from n_utils.ndt import find_include, find_all_includes
from n_utils.aws_infra_util import yaml_load, yaml_save
from n_utils.cf_utils import has_output_selector, select_stacks


def enum(**enums):
    return type('Enum', (), enums)


BRANCH_MODES = enum(SINGLE_STACK='single', MULTI_STACK='multi')


def _add_default_params(parser):
    parser.add_argument("template", nargs="?").completer = ChoicesCompleter(list_templates())
    parser.add_argument("-y", "--yes", action='store_true',
                        help='Answer yes or use default to all questions')


def create_stack():
    """ Create a stack from a template
    """
    parser = argparse.ArgumentParser(description=create_stack.__doc__, add_help=False)
    _add_default_params(parser)
    parser.add_argument("-h", "--help", action='store_true')
    if "_ARGCOMPLETE" in os.environ:
        ac_args = argcomplete.split_line(os.environ['COMP_LINE'],
                                         os.environ['COMP_POINT'])[3]
        if len(ac_args) >= 2:
            template = ac_args[1]
            template_yaml = load_template(template)
            if template_yaml and "ContextClass" in template_yaml:
                context = load_class(template_yaml["ContextClass"])()
                context.add_context_arguments(parser)
    argcomplete.autocomplete(parser)
    args, _ = parser.parse_known_args()
    if args.template:
        template_yaml = load_template(args.template)
        if "ContextClass" in template_yaml:
            context = load_class(template_yaml["ContextClass"])()
            template_yaml.pop("ContextClass", None)
            parser = argparse.ArgumentParser(description=context.__doc__)
            _add_default_params(parser)
            context.add_context_arguments(parser)
        else:
            parser = argparse.ArgumentParser(description=create_stack.__doc__)
            _add_default_params(parser)
    else:
        parser = argparse.ArgumentParser(description=create_stack.__doc__)
        _add_default_params(parser)
    args = parser.parse_args()
    context.resolve_parameters(args)
    context.set_template(template_yaml)
    if context.write(yes=args.yes):
        subprocess.check_call(["ndt", "print-create-instructions",
                               context.component_name, context.stack_name])
    return


def load_template(template):
    file_name = find_include("creatable-templates/" + template + ".yaml")
    if file_name:
        return yaml_load(open(file_name))
    else:
        return None


def load_class(name):
    components = name.split('.')
    mod = __import__(components[0])
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod


def list_templates():
    ret = []
    files = find_all_includes("creatable-templates/*.yaml")
    for next_file in files:
        next_name = os.path.basename(next_file)[:-5]
        if next_name not in ret:
            ret.append(next_name)
    return ret


def has_entry(prefix, name, file_name):
    if not os.path.isfile(file_name):
        return False
    with open(file_name, "r") as config:
        for line in config.readlines():
            if "[" + prefix + name + "]" == line.strip():
                return True
    return False


def setup_cli(name=None, key_id=None, secret=None, region=None):
    if name is None:
        name = eval(input("Profile name: "))
    home_dir = os.path.expanduser("~")
    config_file = os.path.join(home_dir, ".aws", "config")
    credentials_file = os.path.join(home_dir, ".aws", "credentials")
    if has_entry("profile ", name, config_file) or \
       has_entry("", name, credentials_file):
        print("Profile " + name + " already exists. Not overwriting.")
        return
    if key_id is None:
        key_id = eval(input("Key ID: "))
    if secret is None:
        secret = eval(input("Key secret: "))
    if region is None:
        region = eval(input("Default region: "))
    writer = ConfigFileWriter()
    config_values = {
        "__section__": "profile " + name,
        "output": "json",
        "region": region
    }
    credentials_values = {
        "__section__": name,
        "aws_access_key_id": key_id,
        "aws_secret_access_key": secret
    }
    writer.update_config(config_values, config_file)
    writer.update_config(credentials_values, credentials_file)
    home_bin = credentials_file = os.path.join(home_dir, "bin")
    if not os.path.isdir(home_bin):
        os.makedirs(home_bin)
    source_file = os.path.join(home_bin, name)
    with open(source_file, "w") as source_script:
        source_script.write('#!/bin/bash\n\n')
        source_script.write('export AWS_DEFAULT_REGION=')
        source_script.write(region + ' AWS_PROFILE=' + name)
        source_script.write(' AWS_DEFAULT_PROFILE=' + name + "\n")
    os.chmod(source_file, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)
    os.environ['AWS_PROFILE'] = name
    os.environ['AWS_DEFAULT_PROFILE'] = name
    os.environ['AWS_DEFAULT_REGION'] = region


def _append_cidr_param(public, letter, cidr, params):
    if public:
        cidr_param = "paramPub" + letter + "Cidr"
        description = "Public Subnet " + letter + " CIDR block"
    else:
        cidr_param = "paramPriv" + letter + "Cidr"
        description = "Private Subnet " + letter + " CIDR block"
    params.update(OrderedDict([(cidr_param, OrderedDict([
        ("Description", description),
        ("Type", "String"),
        ("Default", _nts(cidr))]))]))


def _append_network_resources(public, letter, resources, availability_zone):
    if public:
        subnet_resource = "resourcePubSubnetA"
        route_table_assoc = "resourcePubSubnetRouteTableAssocA"
        cidr_param = "paramPub" + letter + "Cidr"
        db_subnet = "resourcePubSubnetGroup"
    else:
        subnet_resource = "resourcePrivSubnetA"
        route_table_assoc = "resourcePrivSubnetRouteTableAssocA"
        cidr_param = "paramPriv" + letter + "Cidr"
        route_table = "resourcePrivRouteTableA"
        db_subnet = "resourcePrivSubnetGroup"

    subnet_to_create = subnet_resource[:-1] + letter

    subnet_res_dict = deepcopy(resources[subnet_resource])
    subnet_res_dict['Properties']['CidrBlock']['Ref'] = cidr_param
    subnet_res_dict['Properties']['AvailabilityZone'] = availability_zone
    subnet_res_dict['Properties']['Tags'][0]['Value']['Fn::Join'][1][1] += \
        availability_zone
    resources.update({subnet_to_create: subnet_res_dict})
    if not public:
        route_table_dict = deepcopy(resources[route_table])
        route_table_dict['Properties']['Tags'][0]['Value']['Fn::Join'][1][1] = \
            " private route table " + letter
        resources.update(OrderedDict([(route_table[:-1] + letter, route_table_dict)]))
    route_table_assoc_dict = deepcopy(resources[route_table_assoc])
    if not public:
        route_table_assoc_dict['Properties']['RouteTableId']['Ref'] = \
            route_table[:-1] + letter
    route_table_assoc_dict['Properties']['SubnetId']['Ref'] = \
        subnet_to_create
    resources.update(OrderedDict([(route_table_assoc[:-1] + letter, route_table_assoc_dict)]))

    resources[db_subnet]['Properties']['SubnetIds'].append(OrderedDict([("Ref", subnet_to_create)]))


def _nts(net):
    return str(net).lower()

def _get_network_yaml(network, vpc_cidr, subnet_prefixlen, subnet_base, network_yaml, common_yaml):
    subnet_bits = 32 - int(subnet_prefixlen)
    subnet_size = 2 ** subnet_bits
    last_subnet = subnet_base - subnet_size
    ec2 = boto3.client("ec2")
    az_response = ec2.describe_availability_zones()
    az_names = sorted([az_data['ZoneName'] for az_data in
                       az_response['AvailabilityZones']])
    network_yaml['Parameters']['paramVPCCidr']['Default'] = _nts(vpc_cidr)
    for az_name in az_names:
        zone_letter = az_name[-1:]
        zone_upper_letter = zone_letter.upper()
        last_subnet += subnet_size
        private_subnet_addr = last_subnet + (len(az_names) * subnet_size)
        subnet = ipaddr.IPv4Network(str(last_subnet) + "/" + str(subnet_prefixlen))
        private_subnet = ipaddr.IPv4Network(str(private_subnet_addr) + "/" +
                                            str(subnet_prefixlen))
        if zone_letter == 'a':
            network_yaml['Parameters']['paramPubACidr']['Default'] = _nts(subnet)
            network_yaml['Parameters']['paramPrivACidr']['Default'] = _nts(private_subnet)
            network_yaml['Resources']['resourcePubSubnetA']['Properties']['AvailabilityZone'] = az_name
            network_yaml['Resources']['resourcePrivSubnetA']['Properties']['AvailabilityZone'] = az_name
            common_yaml['paramNetwork']['Default'] = _nts(network)
        else:
            _append_cidr_param(True, zone_upper_letter, _nts(subnet),
                               network_yaml['Parameters'])
            _append_cidr_param(False, zone_upper_letter, _nts(private_subnet),
                               network_yaml['Parameters'])
            _append_network_resources(True, zone_upper_letter,
                                      network_yaml['Resources'], az_name)
            _append_network_resources(False, zone_upper_letter,
                                      network_yaml['Resources'], az_name)
            network_yaml['Outputs']['subnet' + zone_upper_letter] = {
                "Description": "Public Subnet " + zone_upper_letter,
                "Value": {"Ref": "resourcePubSubnet" + zone_upper_letter},
                "Export": {"Name": {"Fn::Join": [":", [{"Ref": "AWS::StackName"},
                                                       "publicSubnet" + zone_upper_letter]]}}
            }
            network_yaml['Outputs']['subnetPriv' + zone_upper_letter] = {
                "Description": "Private Subnet " + zone_upper_letter,
                "Value": {"Ref": "resourcePrivSubnet" + zone_upper_letter},
                "Export": {"Name": {"Fn::Join": [":", [{"Ref": "AWS::StackName"},
                                                       "privateSubnet" + zone_upper_letter]]}}
            }
            pub_net = deepcopy(common_yaml['paramSubnetA'])
            pub_net['Description'] = pub_net['Description'][:-1] + zone_upper_letter
            pub_net['Default']['StackRef']['paramName'] = \
                pub_net['Default']['StackRef']['paramName'][:-1] + zone_upper_letter
            common_yaml['paramSubnet' + zone_upper_letter] = pub_net
            priv_net = deepcopy(common_yaml['paramSubnetPrivA'])
            priv_net['Description'] = pub_net['Description'][:-1] + zone_upper_letter
            priv_net['Default']['StackRef']['paramName'] = \
                priv_net['Default']['StackRef']['paramName'][:-1] + zone_upper_letter
            common_yaml['paramSubnetPriv' + zone_upper_letter] = priv_net
    return network_yaml, common_yaml


def _set_first_parameter(root, name, value):
    if name in root:
        root[name]["Default"] = value
        return True
    for k, v in list(root.items()):
        if isinstance(v, dict) or isinstance(v, OrderedDict):
            return _set_first_parameter(v, name, value)
        elif isinstance(v, list):
            for next in v:
                if _set_first_parameter(next, name, value):
                    return True


def _map_ssh_key(context, param, value):
    key_name = None
    default_name = "ndt-" + context.__class__.__name__.lower() + "-instance"
    if value == "1":
        key_name = eval(input("Name for new key pair (" + default_name + "): "))
        if not key_name:
            key_name = default_name
        ec2 = boto3.client("ec2")
        key_res = ec2.create_key_pair(KeyName=key_name)
        if key_res and "KeyMaterial" in key_res:
            proc = Popen(["store-secret.sh", key_name + ".pem"],
                         stdout=PIPE, stdin=PIPE, stderr=PIPE)
            proc.communicate(input=key_res["KeyMaterial"])
    else:
        try:
            index = int(value) - 2
            key_name = context.ssh_keys[index]
        except (ValueError, IndexError):
            print("Invalid ssh key selection " + value)
            sys.exit(1)
    return key_name


def _map_elastic_ip(context, param, value):
    eip = None
    if value == "1":
        ec2 = boto3.client("ec2")
        eip_res = ec2.allocate_address(Domain='vpc')
        if eip_res and "PublicIp" in eip_res:
            eip = eip_res["PublicIp"]
        ec2.create_tags(Resources=[eip_res['AllocationId']],
                        Tags=[{
                            "Key": "Name",
                            "Value": context.__class__.__name__.lower()
                        }])
    else:
        try:
            index = int(value) - 2
            eip = context.elastic_ips[index]
        except (ValueError, IndexError):
            print("Invalid elastic ip selection " + value)
            sys.exit(1)
    return eip


def _map_list(context, param, value):
    select_list = getattr(context, param + "s")
    try:
        index = int(value) - 1
        return select_list[index]
    except (ValueError, IndexError):
        print("Invalid " + param + " selection " + value)
        sys.exit(1)


class ContextClassBase(object):
    """ Base class for template contexts. Can be directly used for
    bootstrap stacks with no parameters to ask can use it directly
    """
    ask_fields = []
    component_name = "bootstrap"
    stack_name = "Stack name ({0}): "
    branch_mode = BRANCH_MODES.SINGLE_STACK
    template = None
    value_mappers = {}
    template_transformers = []

    def __init__(self, ask_fields):
        if not ask_fields:
            ask_fields = ["stack_name"]
        elif "stack_name" not in ask_fields:
            if ask_fields[0] == "component_name":
                ask_fields.insert(1, "stack_name")
            else:
                ask_fields.insert(0, "stack_name")
        self.ask_fields = ask_fields

    def stack_name_default(self):
        return "default"

    def set_template(self, template):
        self.template = template
        for transformer in self.template_transformers:
            transformer(self)

    def format_prompt(self, parameter, default=None):
        prompt = getattr(self, parameter)
        if not default:
            default = getattr(self, parameter + "_default")()
        return prompt.format(default)

    def getattr(self, parameter):
        return getattr(self, parameter)

    def setattr(self, parameter, value):
        return setattr(self, parameter, value)

    def add_context_arguments(self, parser):
        parameters = self.getattr("ask_fields")
        shorts = ['h']
        for param in parameters:
            if not param[0] in shorts:
                shorts.append(param[0])
            else:
                attempt = [x[0] for x in re.split("[\b_]", param)]
                if len(attempt) > 1 and not attempt[1] in shorts:
                    shorts.append(attempt[1])
                else:
                    attempt = param[1]
                    if attempt not in shorts:
                        shorts.append(attempt)
                    else:
                        shorts.append("")
        shorts.pop(0)
        for short_arg, long_arg in zip(shorts, parameters):
            if short_arg:
                parser.add_argument("-" + short_arg, "--" + long_arg,
                                    help=self.format_prompt(long_arg))
            else:
                parser.add_argument("--" + long_arg, help=self.format_prompt(long_arg))

    def resolve_parameters(self, args):
        for param in self.ask_fields:
            if getattr(args, param):
                setattr(self, param, getattr(args, param))
            elif args.yes:
                setattr(self, param, getattr(args, param + "_default")())
            else:
                default = self.getattr(param + "_default")()
                setval = eval(input(self.format_prompt(param, default=default)))
                if not setval:
                    setval = default
                if param in self.value_mappers:
                    setval = self.value_mappers[param](self, param, setval)
                self.setattr(param, setval)

    def _ask_ssh_key(self):
        self.ssh_key = "Ssh key ({0}):\n1: create new\n"
        self.ssh_keys = []
        self.ssh_key_default = lambda: "1"
        if "ssh_key" not in self.ask_fields:
            self.ask_fields.append("ssh_key")
        index = 2
        ec2 = boto3.client("ec2")
        keys = ec2.describe_key_pairs()
        if keys and "KeyPairs" in keys:
            for key in keys["KeyPairs"]:
                self.ssh_keys.append(key["KeyName"])
                self.ssh_key = self.ssh_key + str(index) \
                    + ": " + key["KeyName"] + "\n"
                index = index + 1
        self.value_mappers["ssh_key"] = _map_ssh_key
        self.template_transformers.append(lambda myself: _set_first_parameter(myself.template,
                                                                              "paramSshKeyName",
                                                                              myself.ssh_key))

    def _ask_elastic_ip(self):
        self.elastic_ip = "Elastic ip ({0}):\n1: allocate new\n"
        self.elastic_ips = []
        self.elastic_ip_default = lambda: "1"
        if "elastic_ip" not in self.ask_fields:
            self.ask_fields.append("elastic_ip")
        index = 2
        ec2 = boto3.client("ec2")
        eips = ec2.describe_addresses()
        if eips and "Addresses" in eips:
            for address in eips["Addresses"]:
                if "InstanceId" not in address:
                    self.elastic_ips.append(address['PublicIp'])
                    self.elastic_ip = self.elastic_ip + str(index) \
                        + ": " + address['PublicIp'] + "\n"
                    index = index + 1
        self.value_mappers["elastic_ip"] = _map_elastic_ip
        self.template_transformers.append(lambda myself: _set_first_parameter(myself.template,
                                                                              "paramEip",
                                                                              myself.elastic_ip))

    def write(self, yes=False):
        if "Files" in self.template:
            for entry in self.template["Files"]:
                for source, dest in list(entry.items()):
                    dest = self.component_name + os.sep + dest % self.__dict__
                    dest = os.path.normpath(dest)
                    dest_dir = os.path.normpath(os.path.dirname(dest))
                    if not os.path.exists(dest_dir):
                        os.makedirs(dest_dir)
                    source_file = find_include(source)
                    shutil.copy2(source_file, dest)
            self.template.pop("Files", None)
        stack_dir = os.path.join(".", self.component_name, "stack-" + self.stack_name)
        if not os.path.exists(stack_dir):
            os.makedirs(stack_dir)
        if self.branch_mode == BRANCH_MODES.SINGLE_STACK:
            file_name = "infra.properties"
            stack_props = os.path.join(stack_dir, file_name)
            if not os.path.exists(stack_props):
                with open(stack_props, 'w') as stack_props_file:
                    stack_props_file.write("STACK_NAME=$ORIG_STACK_NAME\n")
        stack_template = os.path.join(stack_dir, "template.yaml")
        if os.path.exists(stack_template) and not yes:
            answer = eval(input("Overwrite " + self.stack_name + " stack? (n): "))
            if not answer or not answer.lower() == "y":
                return False
        with open(stack_template, "w") as stack_file:
            stack_file.write(yaml_save(self.template))
        return True


class Network(ContextClassBase):
    """ Creates a public and private subnet for every availability zone
    in the selected region and a shared common yaml (common/network.yaml)
    for easy access to parameters.
    """
    stack_name = "Network stack name ({0}): "
    vpc_cidr = "VPC CIDR ({0}) "
    subnet_prefixlen = "Subnet prefix length ({0}) "
    subnet_base = "Subnet base ({0}) "
    last_vpc_cidr = None
    common_yaml = None

    def __init__(self):
        ContextClassBase.__init__(self, ['vpc_cidr', 'subnet_prefixlen', 'subnet_base'])

    def stack_name_default(self):
        return "network"

    def vpc_cidr_default(self):
        self.last_vpc_cidr = "10." + str(random.randint(0, 255)) + ".0.0/16"
        return self.last_vpc_cidr

    def subnet_prefixlen_default(self):
        try:
            nw = ipaddr.IPv4Network(self.vpc_cidr)
            return nw.prefixlen + 4
        except BaseException:
            try:
                nw = ipaddr.IPv4Network(self.last_vpc_cidr)
                return nw.prefixlen + 4
            except BaseException:
                return 20

    def subnet_base_default(self):
        try:
            nw = ipaddr.IPv4Network(self.vpc_cidr)
            return nw.network
        except BaseException:
            try:
                nw = ipaddr.IPv4Network(self.last_vpc_cidr)
                return nw.network
            except BaseException:
                return "10." + str(random.randint(0, 255)) + ".0.0"

    def set_template(self, template):
        common_yaml = yaml_load(open(find_include("creatable-templates/network/common.yaml")))
        self.template, self.common_yaml = \
            _get_network_yaml(self.stack_name, self.vpc_cidr, self.subnet_prefixlen,
                              self.subnet_base, template, common_yaml)

    def write(self, yes=False):
        ContextClassBase.write(self, yes=yes)
        if not os.path.exists("common"):
            os.makedirs("common")
        common_out = os.path.join("common", "network.yaml")
        with open(common_out, 'w') as c_out:
            c_out.write(yaml_save(self.common_yaml))
        return True


class BakeryRoles(ContextClassBase):
    """ Creates roles necessary for baking images and deploying stacks
    """

    def __init__(self):
        ContextClassBase.__init__(self, ['network_stack', 'vault_stack'])
        self._ask_network_stack()
        self._ask_vault_stack()

    def _ask_network_stack(self):
        self.network_stack = "Network stack ({0}):\n"

        def network_sel(stack): return has_output_selector(stack, "VPC",
                                                           lambda stack: stack['StackName'])
        self.network_stacks = select_stacks(network_sel)
        if self.network_stacks:
            index = 1
            for stack_name in self.network_stacks:
                self.network_stack = self.network_stack + str(index) + ": " + \
                    stack_name + "\n"
                index = index + 1
        self.value_mappers["network_stack"] = _map_list
        self.template_transformers.append(lambda myself: _set_first_parameter(myself.template,
                                                                              "paramNetworkStack",
                                                                              myself.network_stack))

    def _ask_vault_stack(self):
        self.vault_stack = "Vault stack ({0}):\n"

        def vault_sel(stack): return has_output_selector(stack, "decryptPolicy",
                                                         lambda stack: stack['StackName'])
        self.vault_stacks = select_stacks(vault_sel)
        if self.vault_stacks:
            index = 1
            for stack_name in self.vault_stacks:
                self.vault_stack = self.vault_stack + str(index) + ": " + \
                    stack_name + "\n"
                index = index + 1
        self.value_mappers["vault_stack"] = _map_list
        self.template_transformers.append(lambda myself: _set_first_parameter(myself.template,
                                                                              "paramVaultStack",
                                                                              myself.vault_stack))

    def stack_name_default(self):
        return "bakery-roles"

    def network_stack_default(self):
        return "1"

    def vault_stack_default(self):
        return "1"


class Route53(ContextClassBase):
    """ Creates a common shared yaml (common/route53.yaml) for
    easy access to route53 parameters
    """

    def __init__(self):
        ContextClassBase.__init__(self, ['hosted_zone'])
        self.ask_fields.pop(0)
        self._ask_hosted_zone()

    def _ask_hosted_zone(self):
        self.hosted_zone = "Hosted zone ({0}):\n"
        self.hosted_zones = boto3.client('route53').list_hosted_zones()['HostedZones']
        self.hosted_zone_default = lambda: "1"
        if self.hosted_zones:
            index = 1
            for zone in self.hosted_zones:
                priv = "Private"
                if zone['Config']['PrivateZone']:
                    priv = "Public"
                self.hosted_zone = self.hosted_zone + str(index) + ": " + \
                    zone['Name'] + " (" + \
                    zone['Id'].split("/")[-1:][0] + ") - " \
                    + priv + "\n"
                index = index + 1
        self.value_mappers["hosted_zone"] = _map_list

    def write(self, yes=False):
        if not os.path.exists("common"):
            os.makedirs("common")
        common_out = os.path.join("common", "route53.yaml")
        common_yaml = {
            "paramHostedZoneName": {
                "Type": "String",
                "Description": "Name of hosted zone to use",
                "Default": self.hosted_zone['Name']
            },
            "paramHostedZoneDomain": {
                "Type": "String",
                "Description": "Name of hosted zone to use",
                "Default": self.hosted_zone['Name'][:-1]
            },
            "paramHostedZoneId": {
                "Type": "String",
                "Description": "Id of hosted zone to use",
                "Default": self.hosted_zone['Id'].split("/")[-1:][0]
            }
        }
        with open(common_out, 'w') as c_out:
            c_out.write(yaml_save(common_yaml))
        return False


class Jenkins(ContextClassBase):
    """ Creates a jenkins stack with the default domain name jenkins.${paramHostedZoneDomain}.
    Also a Jenkins Job DSL script is created that can be run in Jenkins to create jobs
    to bake and deploy ndt infrastructure defined in this repository.
    """
    elastic_ip = "Elastic IP ({0}):\n1: allocate new\n"
    elastic_ips = []

    def __init__(self):
        ContextClassBase.__init__(self, ['component_name', 'elastic_ip', 'ssh_key'])
        self.component_name = "Component name ({0}): "
        self.branch_mode = BRANCH_MODES.MULTI_STACK
        self._ask_elastic_ip()
        self._ask_ssh_key()

    def component_name_default(self):
        return "jenkins"

    def stack_name_default(self):
        return "jenkins"

    def set_template(self, template):
        ContextClassBase.set_template(self, template)
        ec2 = boto3.client("ec2")
        az_response = ec2.describe_availability_zones()
        az_names = sorted([az_data['ZoneName'] for az_data in
                           az_response['AvailabilityZones']])
        for az_name in az_names:
            self.template["Resources"]["Fn::Merge"][0]["resourceAsg"]["Properties"]["AvailabilityZones"].append(az_name)
            self.template["Resources"]["Fn::Merge"][0]["resourceAsg"]["Properties"]["VPCZoneIdentifier"].append(
                "paramSubnet" + az_name[-1:].upper())
