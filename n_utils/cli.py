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

""" Command line tools for nameless-deploy-tools
"""
from __future__ import print_function

from builtins import input
from builtins import str
import argparse
import json
import locale
import os
import sys
import time
import re
import inspect
from datetime import datetime, timedelta
from dateutil.parser import parse
from dateutil.tz import tzutc
from inspect import trace, getframeinfo
from subprocess import PIPE, Popen
import argcomplete
import yaml
from argcomplete.completers import ChoicesCompleter, FilesCompleter
from pygments import highlight, lexers, formatters
from pygments.styles import get_style_by_name
from n_utils import aws_infra_util, cf_bootstrap, cf_deploy, cf_utils, \
    volumes, _to_bytes, _to_str
from n_utils.cf_utils import InstanceInfo, is_ec2, region, regions, stacks, \
    stack_params_and_outputs, get_images, promote_image, \
    share_to_another_region, set_region, register_private_dns, interpolate_file, \
    assumed_role_name, session_token
from n_utils.cloudfront_utils import distributions, distribution_comments, \
    upsert_cloudfront_records
from n_utils.ecr_utils import ensure_repo, repo_uri
from n_utils.log_events import CloudWatchLogsGroups, CloudFormationEvents, CloudWatchLogsThread
from n_utils.maven_utils import add_server
from n_utils.mfa_utils import mfa_add_token, mfa_delete_token, mfa_generate_code, \
    mfa_generate_code_with_secret, list_mfa_tokens, mfa_backup_tokens, mfa_decrypt_backup_tokens, \
    mfa_to_qrcode, mfa_read_token
from n_utils.account_utils import list_created_accounts, create_account
from n_utils.aws_infra_util import load_parameters
from n_utils.ndt import find_include, find_all_includes, include_dirs
from n_utils.profile_util import update_profile, print_profile
from n_utils.ndt_project import list_jobs, list_components
from n_utils.git_utils import Git
from n_utils.ndt_project import Project
from n_utils.tf_utils import pull_state, jmespath_var, flat_state

SYS_ENCODING = locale.getpreferredencoding()

NoneType = type(None)

def get_parser(formatter=None):
    func_name = inspect.stack()[1][3]
    caller = sys._getframe().f_back
    func = caller.f_locals.get(
        func_name, caller.f_globals.get(
            func_name
        )
    )
    if formatter:
        return argparse.ArgumentParser(formatter_class=formatter, description=func.__doc__)
    else:
        return argparse.ArgumentParser(description=func.__doc__)


def list_file_to_json():
    """ Convert a file with an entry on each line to a json document with
    a single element (name as argument) containg file rows as  list.
    """
    parser = get_parser()
    parser.add_argument("arrayname", help="The name in the json object given" +
                                          "to the array").completer = \
        ChoicesCompleter(())
    parser.add_argument("file", help="The file to parse").completer = \
        FilesCompleter()
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    if not os.path.isfile(args.file):
        parser.error(args.file + " not found")
    content = [line.rstrip('\n') for line in open(args.file)]
    json.dump({args.arrayname: content}, sys.stdout)


def add_deployer_server():
    """Add a server into a maven configuration file. Password is taken from the
    environment variable 'DEPLOYER_PASSWORD'
    """
    parser = get_parser()
    parser.add_argument("file", help="The file to modify").completer = \
        FilesCompleter()
    parser.add_argument("username",
                        help="The username to access the server.").completer = \
        ChoicesCompleter(())
    parser.add_argument("--id", help="Optional id for the server. Default is" +
                                     " deploy. One server with this id is " +
                                     "added and another with '-release' " +
                                     "appended", default="deploy").completer = \
        ChoicesCompleter(())
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    if not os.path.isfile(args.file):
        parser.error(args.file + " not found")
    add_server(args.file, args.id, args.username)
    add_server(args.file, args.id + "-release", args.username)


def get_userdata():
    """Get userdata defined for an instance into a file
    """
    parser = get_parser()
    parser.add_argument("file", help="File to write userdata into").completer =\
        FilesCompleter()
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    dirname = os.path.dirname(args.file)
    if dirname:
        if os.path.isfile(dirname):
            parser.error(dirname + " exists and is a file")
        elif not os.path.isdir(dirname):
            os.makedirs(dirname)
    cf_utils.get_userdata(args.file)
    return


def get_account_id():
    """Get current account id. Either from instance metadata or current cli
    configuration.
    """
    parser = get_parser()
    parser.parse_args()
    print(cf_utils.resolve_account())


def colorprint(data, output_format="yaml"):
    """ Colorized print for either a yaml or a json document given as argument
    """
    lexer = lexers.get_lexer_by_name(output_format)
    formatter = formatters.get_formatter_by_name("256")
    formatter.__init__(style=get_style_by_name('emacs'))
    colored = highlight(str(data, 'UTF-8'), lexer, formatter)
    sys.stdout.write(colored)


def yaml_to_json():
    """Convert nameless CloudFormation yaml to CloudFormation json with some
    preprosessing
    """
    parser = get_parser()
    parser.add_argument("--colorize", "-c", help="Colorize output", action="store_true")
    parser.add_argument("--merge", "-m", help="Merge other yaml files to the main file", nargs="*")
    parser.add_argument("--small", "-s", help="Compact representration of json", action="store_true")
    parser.add_argument("file", help="File to parse").completer = FilesCompleter()
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    if not os.path.isfile(args.file):
        parser.error(args.file + " not found")
    doc = aws_infra_util.yaml_to_dict(args.file, merge=args.merge)
    if args.small:
        dump = lambda out_doc: json.dumps(out_doc)
    else:
        dump = lambda out_doc: json.dumps(out_doc, indent=2)
    if args.colorize:
        colorprint(dump(doc), output_format="json")
    else:
        print(dump(doc))


def yaml_to_yaml():
    """ Do ndt preprocessing for a yaml file
    """
    parser = get_parser()
    parser.add_argument("--colorize", "-c", help="Colorize output", action="store_true")
    parser.add_argument("file", help="File to parse").completer = FilesCompleter()
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    if not os.path.isfile(args.file):
        parser.error(args.file + " not found")
    doc = aws_infra_util.yaml_to_yaml(args.file)
    if args.colorize:
        colorprint(doc)
    else:
        print(doc)


def json_to_yaml():
    """Convert CloudFormation json to an approximation of a nameless CloudFormation
    yaml with for example scripts externalized
    """
    parser = get_parser()
    parser.add_argument("--colorize", "-c", help="Colorize output",
                        action="store_true")
    parser.add_argument("file", help="File to parse").completer = FilesCompleter()
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    if not os.path.isfile(args.file):
        parser.error(args.file + " not found")
    doc = aws_infra_util.json_to_yaml(args.file)
    if args.colorize:
        colorprint(doc)
    else:
        print(doc)


def read_and_follow():
    """Read and print a file and keep following the end for new data
    """
    parser = get_parser()
    parser.add_argument("file", help="File to follow").completer = FilesCompleter()
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    if not os.path.isfile(args.file):
        parser.error(args.file + " not found")
    cf_utils.read_and_follow(args.file, sys.stdout.write)


def logs_to_cloudwatch():
    """Read a file and send rows to cloudwatch and keep following the end for new data.
    The log group will be the stack name that created instance and the logstream
    will be the instance id and filename.
    """
    parser = get_parser()
    parser.add_argument("file", help="File to follow").completer = FilesCompleter()
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    if not os.path.isfile(args.file):
        parser.error(args.file + " not found")
    cf_utils.send_logs_to_cloudwatch(args.file)


def signal_cf_status():
    """Signal CloudFormation status to a logical resource in CloudFormation
    that is either given on the command line or resolved from CloudFormation
    tags
    """
    parser = get_parser()
    parser.add_argument("status",
                        help="Status to indicate: SUCCESS | FAILURE").completer\
        = ChoicesCompleter(("SUCCESS", "FAILURE"))
    parser.add_argument("-r", "--resource", help="Logical resource name to " +
                                                 "signal. Looked up from " +
                                                 "cloudformation tags by " +
                                                 "default")
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    if args.status != "SUCCESS" and args.status != "FAILURE":
        parser.error("Status needs to be SUCCESS or FAILURE")
    cf_utils.signal_status(args.status, resource_name=args.resource)


def associate_eip():
    """Associate an Elastic IP for the instance that this script runs on
    """
    parser = get_parser()
    parser.add_argument("-i", "--ip", help="Elastic IP to allocate - default" +
                                           " is to get paramEip from the stack" +
                                           " that created this instance")
    parser.add_argument("-a", "--allocationid", help="Elastic IP allocation " +
                                                     "id to allocate - " +
                                                     "default is to get " +
                                                     "paramEipAllocationId " +
                                                     "from the stack " +
                                                     "that created this instance")
    parser.add_argument("-e", "--eipparam", help="Parameter to look up for " +
                                                 "Elastic IP in the stack - " +
                                                 "default is paramEip",
                        default="paramEip")
    parser.add_argument("-p", "--allocationidparam", help="Parameter to look" +
                                                          " up for Elastic " +
                                                          "IP Allocation ID " +
                                                          "in the stack - " +
                                                          "default is " +
                                                          "paramEipAllocatio" +
                                                          "nId",
                        default="paramEipAllocationId")
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    cf_utils.associate_eip(eip=args.ip, allocation_id=args.allocationid,
                           eip_param=args.eipparam,
                           allocation_id_param=args.allocationidparam)


def instance_id():
    """ Get id for instance
    """
    parser = get_parser()
    argcomplete.autocomplete(parser)
    parser.parse_args()
    if is_ec2():
        info = InstanceInfo()
        print(info.instance_id())
    else:
        sys.exit(1)


def ec2_region():
    """ Get default region - the region of the instance if run in an EC2 instance
    """
    parser = get_parser()
    argcomplete.autocomplete(parser)
    parser.parse_args()
    print(region())


def tag():
    """ Get the value of a tag for an ec2 instance
    """
    parser = get_parser()
    parser.add_argument("name", help="The name of the tag to get")
    args = parser.parse_args()
    argcomplete.autocomplete(parser)
    if is_ec2():
        info = InstanceInfo()
        value = info.tag(args.name)
        if value is not None:
            print(value)
        else:
            sys.exit("Tag " + args.name + " not found")
    else:
        parser.error("Only makes sense on an EC2 instance")


def stack_name():
    """ Get name of the stack that created this instance
    """
    parser = get_parser()
    argcomplete.autocomplete(parser)
    parser.parse_args()
    if is_ec2():
        info = InstanceInfo()
        print(info.stack_name())
    else:
        parser.error("Only makes sense on an EC2 instance cretated from a CF stack")


def stack_id():
    """ Get id of the stack the creted this instance
    """
    parser = get_parser()
    argcomplete.autocomplete(parser)
    parser.parse_args()
    if is_ec2():
        info = InstanceInfo()
        print(info.stack_id())
    else:
        parser.error("Only makes sense on an EC2 instance cretated from a CF stack")


def logical_id():
    """ Get the logical id that is expecting a signal from this instance
    """
    parser = get_parser()
    argcomplete.autocomplete(parser)
    parser.parse_args()
    if is_ec2():
        info = InstanceInfo()
        print(info.logical_id())
    else:
        parser.error("Only makes sense on an EC2 instance cretated from a CF stack")


def cf_region():
    """ Get region of the stack that created this instance
    """
    parser = get_parser()
    argcomplete.autocomplete(parser)
    parser.parse_args()
    if is_ec2():
        info = InstanceInfo()
        print(info.stack_id().split(":")[3])
    else:
        parser.error("Only makes sense on an EC2 instance cretated from a CF stack")


def update_stack():
    """ Create or update existing CloudFormation stack
    """
    parser = argparse.ArgumentParser(description="Create or update existing " +
                                                 "CloudFormation stack")
    parser.add_argument("stack_name", help="Name of the stack to create or " +
                        "update")
    parser.add_argument("yaml_template", help="Yaml template to pre-process " +
                                              "and use for creation")
    parser.add_argument("region", help="The region to deploy the stack to")
    parser.add_argument("-d", "--dry-run", action="store_true",
                        help="Do not actually deploy anything, but just " +
                             "assemble the json and associated parameters")
    args = parser.parse_args()
    if not os.path.isfile(args.yaml_template):
        parser.error(args.yaml_template + " not found")
    cf_deploy.deploy(args.stack_name, args.yaml_template, args.region,
                     args.dry_run)
    return


def delete_stack():
    """Delete an existing CloudFormation stack
    """
    parser = get_parser()
    parser.add_argument("stack_name", help="Name of the stack to delete")
    parser.add_argument("region", help="The region to delete the stack from")
    args = parser.parse_args()
    cf_deploy.delete(args.stack_name, args.region)
    return


def tail_stack_logs():
    """Tail logs from the log group of a cloudformation stack
    """
    parser = get_parser()
    parser.add_argument("stack_name", help="Name of the stack to watch logs " +
                                           "for")
    parser.add_argument("-s", "--start", help="Start time in seconds since " +
                                              "epoc")
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    cwlogs = CloudWatchLogsThread(args.stack_name, start_time=args.start)
    cwlogs.start()
    cfevents = CloudFormationEvents(args.stack_name, start_time=args.start)
    cfevents.start()
    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            print('Closing...')
            cwlogs.stop()
            cfevents.stop()
            return


def get_logs():
    """Get logs from multiple CloudWatch log groups and possibly filter them.
    """
    parser = get_parser()
    parser.add_argument("log_group_pattern", help="Regular expression to filter log groups with")
    parser.add_argument("-f", "--filter", help="CloudWatch filter pattern")
    parser.add_argument("-s", "--start", help="Start time (x m|h|d|w ago | now | <seconds since epoc>)", nargs="+")
    parser.add_argument("-e", "--end", help="End time (x m|h|d|w ago | now | <seconds since epoc>)", nargs="+")
    parser.add_argument("-o", "--order", help="Best effort ordering of log entries", action="store_true")
    parser.usage = "ndt logs log_group_pattern [-h] [-f FILTER] [-s START [START ...]] [-e END [END ...]] [-o]"
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    cwlogs_groups = CloudWatchLogsGroups(
        log_group_filter=args.log_group_pattern,
        log_filter=args.filter,
        start_time=' '.join(args.start) if args.start else None,
        end_time=' '.join(args.end) if args.end else None,
        sort=args.order
    )
    cwlogs_groups.get_logs()


def resolve_include():
    """Find a file from the first of the defined include paths
    """
    parser = get_parser()
    parser.add_argument("file", help="The file to find")
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    inc_file = find_include(args.file)
    if not inc_file:
        parser.error("Include " + args.file + " not found on include paths " +
                     str(include_dirs))
    print(inc_file)


def resolve_all_includes():
    """Find a file from the first of the defined include paths
    """
    parser = get_parser()
    parser.add_argument("pattern", help="The file pattern to find")
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    inc_file = find_all_includes(args.pattern)
    if not inc_file:
        parser.error("Include " + args.pattern + " not found on include paths " +
                     str(include_dirs))
    for next_file in inc_file:
        print(next_file)


def assume_role():
    """Assume a defined role. Prints out environment variables
    to be eval'd to current context for use:
    eval $(ndt assume-role 'arn:aws:iam::43243246645:role/DeployRole')
    """
    parser = get_parser()
    parser.add_argument("role_arn", help="The ARN of the role to assume")
    parser.add_argument("-t", "--mfa-token", metavar="TOKEN_NAME",
                        help="Name of MFA token to use", required=False)
    parser.add_argument("-d", "--duration", help="Duration for the session in minutes", 
                        default="60", type=int, required=False)
    parser.add_argument("-p", "--profile", help="Profile to edit in ~/.aws/credentials " + \
                                                "to make role persist in that file for " + \
                                                "the duration of the session.", required=False)
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    creds = cf_utils.assume_role(args.role_arn, mfa_token_name=args.mfa_token,
                                 duration_minutes=args.duration)
    if args.profile:
        update_profile(args.profile, creds)
    else:
        print("AWS_ROLE_ARN=\"" + args.role_arn + "\"")
        print("AWS_ACCESS_KEY_ID=\"" + creds['AccessKeyId'] + "\"")
        print("AWS_SECRET_ACCESS_KEY=\"" + creds['SecretAccessKey'] + "\"")
        print("AWS_SESSION_TOKEN=\"" + creds['SessionToken'] + "\"")
        print("AWS_SESSION_EXPIRATION=\"" + creds['Expiration'].strftime("%a, %d %b %Y %H:%M:%S +0000") + "\"")
        print("export AWS_ROLE_ARN AWS_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY AWS_SESSION_TOKEN AWS_SESSION_EXPIRATION")


def session_to_env():
    """ Export current session as environment variables """
    parser = get_parser()
    parser.add_argument("-t", "--token-name",
                        help="Name of the mfs token to use.").completer = \
        ChoicesCompleter(list_mfa_tokens())
    parser.add_argument("-d", "--duration-minutes", type=int, default=60,
                        help="Duration in minutes for the session token. Default to 60")
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    call_args = {"duration_minutes": args.duration_minutes}
    if args.token_name:
        call_args["token_arn"] = mfa_read_token(args.token_name)["token_arn"]
        call_args["token_value"] = mfa_generate_code(args.token_name)

    creds = session_token(**call_args)
    print("AWS_ACCESS_KEY_ID=\"" + creds['AccessKeyId'] + "\"")
    print("AWS_SECRET_ACCESS_KEY=\"" + creds['SecretAccessKey'] + "\"")
    print("AWS_SESSION_TOKEN=\"" + creds['SessionToken'] + "\"")
    print("AWS_SESSION_EXPIRATION=\"" + creds['Expiration'].strftime("%a, %d %b %Y %H:%M:%S +0000") + "\"")

def get_parameter():
    """Get a parameter value from the stack
    """
    parser = get_parser()
    parser.add_argument("parameter", help="The name of the parameter to print")
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    info = InstanceInfo()
    print(info.stack_data(args.parameter))


def volume_from_snapshot():
    """ Create a volume from an existing snapshot and mount it on the given
    path. The snapshot is identified by a tag key and value. If no tag is
    found, an empty volume is created, attached, formatted and mounted.
    """
    parser = get_parser()
    parser.add_argument("tag_key", help="Key of the tag to find volume with")
    parser.add_argument("tag_value", help="Value of the tag to find volume with")
    parser.add_argument("mount_path", help="Where to mount the volume")
    parser.add_argument("size_gb", nargs="?", help="Size in GB for the volum" +
                                                   "e. If different from sna" +
                                                   "pshot size, volume and " +
                                                   "filesystem are resized",
                        default=None, type=int)
    parser.add_argument("-n", "--no_delete_on_termination",
                        help="Whether to skip deleting the volume on termi" +
                             "nation, defaults to false", action="store_true")
    parser.add_argument("-c", "--copytags", nargs="*", help="Tag to copy to the volume from instance. Multiple values allowed.")
    parser.add_argument("-t", "--tags", nargs="*", help="Tag to add to the volume in the format name=value. Multiple values allowed.")
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    tags = {}
    if args.tags:
        for tag in args.tags:
            try:
                key, value = tag.split('=', 1)
                tags[key] = value
            except ValueError:
                parser.error("Invalid tag/value input: " + tag)
    if is_ec2():
        volumes.volume_from_snapshot(args.tag_key, args.tag_value, args.mount_path,
                                     size_gb=args.size_gb,
                                     del_on_termination=not args.no_delete_on_termination,
                                     copytags=args.copytags, tags=tags)
    else:
        parser.error("Only makes sense on an EC2 instance")


def snapshot_from_volume():
    """ Create a snapshot of a volume identified by it's mount path
    """
    parser = get_parser()
    parser.add_argument("-w", "--wait", help="Wait for the snapshot to finish" +
                        " before returning",
                        action="store_true")
    parser.add_argument("tag_key", help="Key of the tag to find volume with")
    parser.add_argument("tag_value", help="Value of the tag to find volume with")
    parser.add_argument("mount_path", help="Where to mount the volume")
    parser.add_argument("-c", "--copytags", nargs="*", help="Tag to copy to the snapshot from instance. Multiple values allowed.")
    parser.add_argument("-t", "--tags", nargs="*", help="Tag to add to the snapshot in the format name=value. Multiple values allowed.")
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    tags = {}
    if args.tags:
        for tag in args.tags:
            try:
                key, value = tag.split('=', 1)
                tags[key] = value
            except ValueError:
                parser.error("Invalid tag/value input: " + tag)
    if is_ec2():
        print(volumes.create_snapshot(args.tag_key, args.tag_value,
                                      args.mount_path, wait=args.wait, tags=tags, copytags=args.copytags))
    else:
        parser.error("Only makes sense on an EC2 instance")


def detach_volume():
    """ Create a snapshot of a volume identified by it's mount path
    """
    parser = get_parser()
    parser.add_argument("mount_path", help="Where to mount the volume")
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    if is_ec2():
        volumes.detach_volume(args.mount_path)
    else:
        parser.error("Only makes sense on an EC2 instance")


def clean_snapshots():
    """Clean snapshots that are older than a number of days (30 by default) and
    have one of specified tag values
    """
    parser = get_parser()
    parser.add_argument("-r", "--region", help="The region to delete " +
                                               "snapshots from. Can also be " +
                                               "set with env variable " +
                                               "AWS_DEFAULT_REGION or is " +
                                               "gotten from instance " +
                                               "metadata as a last resort")
    parser.add_argument("-d", "--days", help="The number of days that is the" +
                                             "minimum age for snapshots to " +
                                             "be deleted", type=int, default=30)
    parser.add_argument("tags", help="The tag values to select deleted " +
                                     "snapshots", nargs="+")
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    if args.region:
        os.environ['AWS_DEFAULT_REGION'] = args.region
    volumes.clean_snapshots(args.days, args.tags)


def setup_cli():
    """Setup the command line environment to define an aws cli profile with
    the given name and credentials. If an identically named profile exists,
    it will not be overwritten.
    """
    parser = get_parser()
    parser.add_argument("-n", "--name", help="Name for the profile to create")
    parser.add_argument("-k", "--key-id", help="Key id for the profile")
    parser.add_argument("-s", "--secret", help="Secret to set for the profile")
    parser.add_argument("-r", "--region", help="Default region for the profile")
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    cf_bootstrap.setup_cli(**vars(args))


def show_stack_params_and_outputs():
    """ Show stack parameters and outputs as a single json documents
    """
    parser = get_parser()
    parser.add_argument("-r", "--region", help="Region for the stack to show",
                        default=region()).completer = ChoicesCompleter(regions())
    parser.add_argument("-p", "--parameter", help="Name of paremeter if only" +
                                                  " one parameter required")
    parser.add_argument("stack_name", help="The stack name to show").completer = \
        ChoicesCompleter(stacks())
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    resp = stack_params_and_outputs(args.region, args.stack_name)
    if args.parameter:
        if args.parameter in resp:
            print(resp[args.parameter])
        else:
            parser.error("Parameter " + args.parameter + " not found")
    else:
        print(json.dumps(resp, indent=2))

def show_terraform_params():
    """ Show available parameters for a terraform subcomponent """
    parser = get_parser()
    parser.add_argument("component", help="The component containg the terraform subcomponet")
    parser.add_argument("terraform", help="The name of the terraform subcomponent")
    param = parser.add_mutually_exclusive_group(required=False)
    param.add_argument("-j", "--jmespath", help="Show just a matching jmespath value")
    param.add_argument("-p", "--parameter", help="Name of paremeter if only" +
                                                " one parameter required")
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    terraform = pull_state(args.component, args.terraform)
    if args.jmespath:
        print(jmespath_var(terraform, args.jmespath))
    else:
        params = flat_state(terraform)
        if args.parameter:
            if args.parameter in params:
                print(params[args.parameter])
        else:
            print(json.dumps(params, indent=2))
            
def cli_get_images():
    """ Gets a list of images given a bake job name
    """
    parser = get_parser()
    parser.add_argument("job_name", help="The job name to look for")
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    set_region()
    images = get_images(args.job_name)
    for image in images:
        print(image['ImageId'] + ":" + image['Name'])


def cli_promote_image():
    """  Promotes an image for use in another branch
    """
    parser = get_parser()
    parser.add_argument("image_id", help="The image to promote")
    parser.add_argument("target_job", help="The job name to promote the image to")
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    if ":" in args.image_id:
        args.image_id = args.image_id.split(":")[0]
    promote_image(args.image_id, args.target_job)


def cli_share_to_another_region():
    """ Shares an image to another region for potentially another account
    """
    parser = get_parser()
    parser.add_argument("ami_id", help="The ami to share")
    parser.add_argument("to_region", help="The region to share to").completer =\
        ChoicesCompleter(regions())
    parser.add_argument("ami_name", help="The name for the ami")
    parser.add_argument("account_id", nargs="+", help="The account ids to sh" +
                                                      "are ami to")
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    share_to_another_region(args.ami_id, args.to_region, args.ami_name,
                            args.account_id)


def cli_register_private_dns():
    """ Register local private IP in route53 hosted zone usually for internal
    use.
    """
    parser = get_parser()
    parser.add_argument("dns_name", help="The name to update in route 53")
    parser.add_argument("hosted_zone", help="The name of the hosted zone to update")
    parser.add_argument("-t", "--ttl", help="Time to live for the record. 60 by default",
                        default="60")
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    register_private_dns(args.dns_name, args.hosted_zone, ttl=args.ttl)


def cli_interpolate_file():
    """ Replace placeholders in file with parameter values from stack and
    optionally from vault
    """
    parser = get_parser()
    parser.add_argument("-s", "--stack", help="Stack name for values. " +
                                              "Automatically resolved on ec2" +
                                              " instances")
    parser.add_argument("-k", "--skip-stack", help="Skip stack parameters in" +
                                                    " all cases",
                        action="store_true")
    parser.add_argument("-n", "--use-environ", help="Use environment variables" +
                                                    " for interpolation",
                        action="store_true")
    parser.add_argument("-v", "--vault", help="Use vault values as well." +
                                              "Vault resovled from env " +
                                              "variables or default is used",
                        action="store_true")
    parser.add_argument("-o", "--output", help="Output file")
    parser.add_argument("-e", "--encoding", help="Encoding to use for the " +
                        "file. Defaults to utf-8",
                        default='utf-8')
    parser.add_argument("file", help="File to interpolate").completer = \
        FilesCompleter()
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    interpolate_file(args.file, stack_name=args.stack, use_vault=args.vault,
                     destination=args.output, use_environ=args.use_environ,
                     skip_stack=args.skip_stack, encoding=args.encoding)


def cli_ecr_ensure_repo():
    """ Ensure that an ECR repository exists and get the uri and login token for
    it """
    parser = get_parser()
    parser.add_argument("name", help="The name of the ecr repository to verify")
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    ensure_repo(args.name)


def cli_ecr_repo_uri():
    """ Get the repo uri for a named docker """
    parser = get_parser()
    parser.add_argument("name", help="The name of the ecr repository")
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    uri = repo_uri(args.name)
    if not uri:
        parser.error("Did not find uri for repo '" + args.name + "'")
    else:
        print(uri)


def cli_upsert_cloudfront_records():
    """ Upsert Route53 records for all aliases of a CloudFront distribution """
    parser = get_parser()
    stack_select = parser.add_mutually_exclusive_group(required=True)
    stack_select.add_argument("-i", "--distribution_id", help="Id for the " +
                                                              "distribution to " +
                                                              "upsert").completer = \
        ChoicesCompleter(distributions())
    stack_select.add_argument("-c", "--distribution_comment", help="Comment for the" +
                                                                   " distribution " +
                                                                   "to upsert").completer = \
        ChoicesCompleter(distribution_comments())
    parser.add_argument("-w", "--wait", help="Wait for request to sync", action="store_true")
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    upsert_cloudfront_records(args)


def cli_mfa_add_token():
    """ Adds an MFA token to be used with role assumption.
        Tokens will be saved in a .ndt subdirectory in the user's home directory.
        If a token with the same name already exists, it will not be overwritten."""
    parser = get_parser()
    parser.add_argument("token_name",
                        help="Name for the token. Use this to refer to the token later with " +
                        "the assume-role command.")
    parser.add_argument("-i", "--interactive", help="Ask for token details interactively.",
                        action="store_true")
    parser.add_argument("-a", "--token_arn", help="ARN identifier for the token.")
    parser.add_argument("-s", "--token_secret", help="Token secret.")
    parser.add_argument("-f", "--force", help="Force an overwrite if the token already exists.",
                        action="store_true")
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    if args.interactive:
        args.token_secret = _to_bytes(input("Enter token secret: "))
        code_1 = mfa_generate_code_with_secret(args.token_secret)
        print("First sync code: " + code_1)
        print("Waiting to generate second sync code. This could take 30 seconds...")
        code_2 = mfa_generate_code_with_secret(args.token_secret)
        while code_1 == code_2:
            time.sleep(5)
            code_2 = mfa_generate_code_with_secret(args.token_secret)
        print("Second sync code: " + code_2)
        args.token_arn = _to_str(input("Enter token ARN: "))
    elif not args.token_secret:
        parser.error("Token secret is required.")
    try:
        mfa_add_token(args)
    except ValueError as error:
        parser.error(error)


def cli_mfa_delete_token():
    """ Deletes an MFA token file from the .ndt subdirectory in the user's
        home directory """
    parser = get_parser()
    parser.add_argument("token_name",
                        help="Name of the token to delete.").completer = \
        ChoicesCompleter(list_mfa_tokens())
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    mfa_delete_token(args.token_name)


def cli_mfa_code():
    """ Generates a TOTP code using an MFA token. """
    parser = get_parser()
    parser.add_argument("token_name",
                        help="Name of the token to use.").completer = \
        ChoicesCompleter(list_mfa_tokens())
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    print(mfa_generate_code(args.token_name))


def cli_mfa_to_qrcode():
    """ Generates a QR code to import a token to other devices. """
    parser = get_parser()
    parser.add_argument("token_name",
                        help="Name of the token to use.").completer = \
        ChoicesCompleter(list_mfa_tokens())
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    mfa_to_qrcode(args.token_name)


def cli_mfa_backup_tokens():
    """ Encrypt or decrypt a backup JSON structure of tokens.

        To output an encrypted backup, provide an encryption secret.

        To decrypt an existing backup, use --decrypt <file>.
    """
    parser = get_parser()
    parser.add_argument("backup_secret",
                        help="Secret to use for encrypting or decrypts the backup.")
    parser.add_argument("-d",
                        "--decrypt",
                        help="Outputs a decrypted token backup read from given file.",
                        nargs=1,
                        metavar="FILE")
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    if args.decrypt:
        print(mfa_decrypt_backup_tokens(args.backup_secret, args.decrypt[0]))
    else:
        print(mfa_backup_tokens(args.backup_secret))


def cli_create_account():
    """ Creates a subaccount. """
    parser = get_parser()
    parser.add_argument("email", help="Email for account root")
    parser.add_argument("account_name", help="Organization unique account name")
    parser.add_argument("-d", "--deny-billing-access", action="store_true")
    parser.add_argument("-o", "--organization-role-name", help="Role name for " +
                                                               "admin access from" +
                                                               " parent account",
                        default="OrganizationAccountAccessRole")
    parser.add_argument("-r", "--trust-role-name", help="Role name for admin " +
                        "access from parent account",
                        default="TrustedAccountAccessRole")
    parser.add_argument("-a", "--trusted-accounts", nargs="*",
                        help="Account to trust with user management").completer = \
        ChoicesCompleter(list_created_accounts())
    parser.add_argument("-t", "--mfa-token", metavar="TOKEN_NAME",
                        help="Name of MFA token to use", required=False)
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    create_account(args.email, args.account_name, role_name=args.organization_role_name,
                   trust_role=args.trust_role_name, access_to_billing=not args.deny_billing_access,
                   trusted_accounts=args.trusted_accounts, mfa_token=args.mfa_token)


def cli_load_parameters():
    """ Load parameters from infra*.properties files in the order:
    infra.properties,
    infra-[branch].properties,
    [component]/infra.properties,
    [component]/infra-[branch].properties,
    [component]/[subcomponent-type]-[subcomponent]/infra.properties,
    [component]/[subcomponent-type]-[subcomponent]/infra-[branch].properties

    Last parameter defined overwrites ones defined before in the files. Supports parameter expansion
    and bash -like transformations. Namely:

    ${PARAM##prefix} # strip prefix greedy
    ${PARAM%%suffix} # strip suffix greedy
    ${PARAM#prefix} # strip prefix not greedy
    ${PARAM%suffix} # strip suffix not greedy
    ${PARAM:-default} # default if empty
    ${PARAM:4:2} # start:len
    ${PARAM/substr/replace}
    ${PARAM^} # upper initial
    ${PARAM,} # lower initial
    ${PARAM^^} # upper
    ${PARAM,,} # lower

    Comment lines start with '#'
    Lines can be continued by adding '\' at the end

    See https://www.tldp.org/LDP/Bash-Beginners-Guide/html/sect_10_03.html
    (arrays not supported)
    """
    parser = get_parser(formatter=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("component", nargs="?", help="Compenent to descend into").completer = \
        ChoicesCompleter([c.name for c in Project().get_components()])
    parser.add_argument("--branch", "-b", help="Branch to get active parameters for").completer = \
        ChoicesCompleter(Git().get_branches())
    parser.add_argument("--resolve-images", "-r", action="store_true", help="Also resolve subcomponent AMI IDs and docker repo urls")
    subcomponent_group = parser.add_mutually_exclusive_group()
    subcomponent_group.add_argument("--stack", "-s", help="CloudFormation subcomponent to descent into").completer = \
        lambda prefix, parsed_args, **kwargs: component_typed_subcomponents("stack", prefix, parsed_args, **kwargs)
    subcomponent_group.add_argument("--serverless", "-l", help="Serverless subcomponent to descent into").completer = \
        lambda prefix, parsed_args, **kwargs: component_typed_subcomponents("serverless", prefix, parsed_args, **kwargs)
    subcomponent_group.add_argument("--docker", "-d", help="Docker image subcomponent to descent into").completer = \
        lambda prefix, parsed_args, **kwargs: component_typed_subcomponents("docker", prefix, parsed_args, **kwargs)
    subcomponent_group.add_argument("--image", "-i", const="", nargs="?", help="AMI image subcomponent to descent into").completer = \
        lambda prefix, parsed_args, **kwargs: component_typed_subcomponents("image", prefix, parsed_args, **kwargs)
    subcomponent_group.add_argument("--cdk", "-c", help="CDK subcomponent to descent into").completer = \
        lambda prefix, parsed_args, **kwargs: component_typed_subcomponents("cdk", prefix, parsed_args, **kwargs)
    subcomponent_group.add_argument("--terraform", "-t", help="Terraform subcomponent to descent into").completer = \
        lambda prefix, parsed_args, **kwargs: component_typed_subcomponents("terraform", prefix, parsed_args, **kwargs)
    format_group = parser.add_mutually_exclusive_group()
    format_group.add_argument("--json", "-j", action="store_true", help="JSON format output (default)")
    format_group.add_argument("--yaml", "-y", action="store_true", help="YAML format output")
    format_group.add_argument("--properties", "-p", action="store_true", help="properties file format output")
    format_group.add_argument("--export-statements", "-e", action="store_true",
                              help="Output as eval-able export statements")

    argcomplete.autocomplete(parser)
    args = parser.parse_args()

    transform = json.dumps
    if args.export_statements:
        transform = map_to_exports
    if args.properties:
        transform = map_to_properties
    if args.yaml:
        transform = yaml.dump
    del args.export_statements
    del args.yaml
    del args.json
    del args.properties
    if (args.stack or args.serverless or args.docker or not isinstance(args.image, NoneType)) \
       and not args.component:
        parser.error("image, stack, doker or serverless do not make sense without component")
    print(transform(load_parameters(**vars(args))), end="")

def component_typed_subcomponents(sc_type, prefix, parsed_args, **kwargs):
    p_args = {}
    if parsed_args.branch:
        p_args["branch"] = parsed_args.branch
    if parsed_args.component:
        return [sc.name for sc in Project(**p_args).get_component(parsed_args.component).get_subcomponents() if sc.type == sc_type and sc.name.startswith(prefix)]
    else:
        return [sc.name for sc in Project(**p_args).get_all_subcomponents() if sc.type == sc_type]
    return None

def map_to_exports(map):
    """ Prints the map as eval-able set of environment variables. Keys
    will be cleaned of all non-word letters and values will be escaped so
    that they will be exported as literal values."""
    ret = ""
    keys = []
    for key, val in list(map.items()):
        key = re.sub("[^a-zA-Z0-9_]", "", key)
        ret += key + "='" + val.replace("'", "'\"'\"'") + "'" + os.linesep
        keys.append(key)
    ret += "export " + " ".join(keys) + os.linesep
    return ret


def map_to_properties(map):
    """ Prints the map as loadable set of java properties. Keys
    will be cleaned of all non-word letters."""
    ret = ""
    for key, val in list(map.items()):
        key = re.sub("[^a-zA-Z0-9_]", "", key)
        ret += key + "=" + val + os.linesep
    return ret

def wait_for_metadata():
    """ Waits for metadata service to be available. All errors are ignored until
    time expires or a socket can be established to the metadata service """
    parser = get_parser()
    parser.add_argument('--timeout', '-t', type=int, help="Maximum time to wait in seconds for the metadata service to be available", default=300)
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    start = datetime.utcnow().replace(tzinfo=tzutc())
    cutoff = start + timedelta(seconds=args.timeout)
    timeout = args.timeout
    connected = False
    while not connected:
        try:
            connected = cf_utils.wait_net_service("169.254.169.254", 80, timeout)
        except:
            pass
        if datetime.utcnow().replace(tzinfo=tzutc()) >= cutoff:
            print("Timed out waiting for metadata service")
            sys.exit(1)
        time.sleep(1)
        timeout = max(1, args.timeout - (datetime.utcnow().replace(tzinfo=tzutc()) - start).total_seconds())

def cli_assumed_role_name():
    """ Read the name of the assumed role if currently defined """
    parser = get_parser()
    argcomplete.autocomplete(parser)
    _ = parser.parse_args()
    print(assumed_role_name())

def cli_list_jobs():
    """ Prints a line for every runnable job in this git repository, in all branches and
    optionally exports the properties for each under '$root/job-properties/"""
    parser = get_parser()
    parser.add_argument("-e", "--export-job-properties", action="store_true",
                        help="Set if you want the properties of all jobs into files under job-properties/")
    parser.add_argument("-j", "--json", action="store_true", help="Print in json format. Optionally " \
                                                                  "exported parameters will be in the json document")
    parser.add_argument("-b", "--branch", help="The branch to process. Default is to process all branches").completer = \
        ChoicesCompleter(Git().get_branches())
    parser.add_argument("-c", "--component", help="Component to process. Default is to process all components").completer = \
        branch_components
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    ret = list_jobs(**vars(args))
    if args.json:
        print(json.dumps(ret, indent=2))
    else:
        print("\n".join(ret))

def branch_components(prefix, parsed_args, **kwargs):
    if parsed_args.branch:
        return [c.name for c in Project(branch=parsed_args.branch).get_components()]
    else:
        return [c.name for c in Project().get_components()]

def cli_list_components():
    """ Prints the components in a branch, by default the current branch """
    parser = get_parser()
    parser.add_argument("-j", "--json", action="store_true", help="Print in json format.")
    parser.add_argument("-b", "--branch", help="The branch to get components from. Default is to process current branch").completer = \
        ChoicesCompleter(Git().get_branches())
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    ret = list_components(**vars(args))
    if args.json:
        print(json.dumps(ret, indent=2))
    else:
        print("\n".join(ret))