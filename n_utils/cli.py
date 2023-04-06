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

import argparse
import inspect
import json
import locale
import os
import re
import sys
import time
from subprocess import PIPE, Popen

import argcomplete
import yaml
from argcomplete.completers import ChoicesCompleter, FilesCompleter
from ec2_utils import ebs, interface
from ec2_utils.instance_info import dthandler, stack_params_and_outputs_and_stack
from ec2_utils.logs import CloudWatchLogsThread
from ec2_utils.utils import best_effort_stacks
from pygments import formatters, highlight, lexers
from pygments.styles import get_style_by_name
from threadlocal_aws import region, regions
from threadlocal_aws.clients import sso

from n_utils import _to_bytes, _to_str, aws_infra_util, cf_bootstrap, cf_deploy, connect, utils
from n_utils.account_utils import create_account, list_created_accounts
from n_utils.aws_infra_util import json_load, json_save_small, load_parameters, yaml_to_dict
from n_utils.az_util import ensure_group, ensure_management_group, fetch_properties
from n_utils.cloudfront_utils import distribution_comments, distributions, upsert_cloudfront_records
from n_utils.ecr_utils import ensure_repo, repo_uri
from n_utils.git_utils import Git
from n_utils.log_events import CloudFormationEvents
from n_utils.maven_utils import add_server
from n_utils.mfa_utils import (
    list_mfa_tokens,
    mfa_add_token,
    mfa_backup_tokens,
    mfa_decrypt_backup_tokens,
    mfa_delete_token,
    mfa_generate_code,
    mfa_generate_code_with_secret,
    mfa_read_token,
    mfa_to_qrcode,
)
from n_utils.ndt import find_all_includes, find_include, include_dirs
from n_utils.ndt_project import Project, list_components, list_jobs, upsert_codebuild_projects
from n_utils.profile_util import _epoc_to_str, get_profile, read_sso_profile, resolve_profile_type, update_profile
from n_utils.route53_util import upsert_record
from n_utils.tf_utils import flat_state, jmespath_var, pull_state
from n_utils.utils import (
    assumed_role_name,
    get_images,
    interpolate_file,
    promote_image,
    session_token,
    share_to_another_region,
)

SYS_ENCODING = locale.getpreferredencoding()

NoneType = type(None)


def get_parser(formatter=None):
    func_name = inspect.stack()[1][3]
    caller = sys._getframe().f_back
    func = caller.f_locals.get(func_name, caller.f_globals.get(func_name))
    if formatter:
        return argparse.ArgumentParser(formatter_class=formatter, description=func.__doc__)
    else:
        return argparse.ArgumentParser(description=func.__doc__)


def list_file_to_json():
    """Convert a file with an entry on each line to a json document with
    a single element (name as argument) containg file rows as  list.
    """
    parser = get_parser()
    parser.add_argument(
        "arrayname", help="The name in the json object given" + "to the array"
    ).completer = ChoicesCompleter(())
    parser.add_argument("file", help="The file to parse").completer = FilesCompleter()
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    if not os.path.isfile(args.file):
        parser.error(args.file + " not found")
    content = [line.rstrip("\n") for line in open(args.file)]
    json.dump({args.arrayname: content}, sys.stdout)


def add_deployer_server():
    """Add a server into a maven configuration file. Password is taken from the
    environment variable 'DEPLOYER_PASSWORD'
    """
    parser = get_parser()
    parser.add_argument("file", help="The file to modify").completer = FilesCompleter()
    parser.add_argument("username", help="The username to access the server.").completer = ChoicesCompleter(())
    parser.add_argument(
        "--id",
        help="Optional id for the server. Default is"
        + " deploy. One server with this id is "
        + "added and another with '-release' "
        + "appended",
        default="deploy",
    ).completer = ChoicesCompleter(())
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    if not os.path.isfile(args.file):
        parser.error(args.file + " not found")
    add_server(args.file, args.id, args.username)
    add_server(args.file, args.id + "-release", args.username)


def colorprint(data, output_format="yaml"):
    """Colorized print for either a yaml or a json document given as argument"""
    lexer = lexers.get_lexer_by_name(output_format)
    formatter = formatters.get_formatter_by_name("256")
    formatter.__init__(style=get_style_by_name("emacs"))
    colored = highlight(_to_str(data), lexer, formatter)
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

        def dump(out_doc):
            return json.dumps(out_doc)

    else:

        def dump(out_doc):
            return json.dumps(out_doc, indent=2, default=dthandler)

    if args.colorize:
        colorprint(dump(doc), output_format="json")
    else:
        print(dump(doc))


def yaml_to_yaml():
    """Do ndt preprocessing for a yaml file"""
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
    parser.add_argument("--colorize", "-c", help="Colorize output", action="store_true")
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


def associate_eip():
    """Associate an Elastic IP for the instance that this script runs on"""
    parser = get_parser()
    parser.add_argument(
        "-i",
        "--ip",
        help="Elastic IP to allocate - default" + " is to get paramEip from the stack" + " that created this instance",
    )
    parser.add_argument(
        "-a",
        "--allocationid",
        help="Elastic IP allocation "
        + "id to allocate - "
        + "default is to get "
        + "paramEipAllocationId "
        + "from the stack "
        + "that created this instance",
    )
    parser.add_argument(
        "-e",
        "--eipparam",
        help="Parameter to look up for " + "Elastic IP in the stack - " + "default is paramEip",
        default="paramEip",
    )
    parser.add_argument(
        "-p",
        "--allocationidparam",
        help="Parameter to look"
        + " up for Elastic "
        + "IP Allocation ID "
        + "in the stack - "
        + "default is "
        + "paramEipAllocatio"
        + "nId",
        default="paramEipAllocationId",
    )
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    interface.associate_eip(
        eip=args.ip,
        allocation_id=args.allocationid,
        eip_param=args.eipparam,
        allocation_id_param=args.allocationidparam,
    )


def update_stack():
    """Create or update existing CloudFormation stack"""
    parser = argparse.ArgumentParser(description="Create or update existing " + "CloudFormation stack")
    parser.add_argument("stack_name", help="Name of the stack to create or " + "update")
    parser.add_argument("yaml_template", help="Yaml template to pre-process " + "and use for creation")
    parser.add_argument("region", help="The region to deploy the stack to")
    parser.add_argument(
        "-d",
        "--dry-run",
        action="store_true",
        help="Do not actually deploy anything, but just " + "assemble the json and associated parameters",
    )
    parser.add_argument(
        "-r",
        "--disable-rollback",
        action="store_true",
        help="Disable stack rollback on failure",
    )
    args = parser.parse_args()
    if not os.path.isfile(args.yaml_template):
        parser.error(args.yaml_template + " not found")
    cf_deploy.deploy(
        args.stack_name,
        args.yaml_template,
        args.region,
        args.dry_run,
        disable_rollback=args.disable_rollback,
    )
    return


def delete_stack():
    """Delete an existing CloudFormation stack"""
    parser = get_parser()
    parser.add_argument("stack_name", help="Name of the stack to delete")
    parser.add_argument("region", help="The region to delete the stack from")
    args = parser.parse_args()
    cf_deploy.delete(args.stack_name, args.region)
    return


def tail_stack_logs():
    """Tail logs from the log group of a cloudformation stack"""
    parser = get_parser()
    parser.add_argument("stack_name", help="Name of the stack to watch logs " + "for")
    parser.add_argument("-s", "--start", help="Start time in seconds since " + "epoc")
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
            print("Closing...")
            cwlogs.stop()
            cfevents.stop()
            return


def resolve_include():
    """Find a file from the first of the defined include paths"""
    parser = get_parser()
    parser.add_argument("file", help="The file to find")
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    inc_file = find_include(args.file)
    if not inc_file:
        parser.error("Include " + args.file + " not found on include paths " + str(include_dirs))
    print(inc_file)


def resolve_all_includes():
    """Find a file from the first of the defined include paths"""
    parser = get_parser()
    parser.add_argument("pattern", help="The file pattern to find")
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    inc_file = find_all_includes(args.pattern)
    if not inc_file:
        parser.error("Include " + args.pattern + " not found on include paths " + str(include_dirs))
    for next_file in inc_file:
        print(next_file)


def assume_role():
    """Assume a defined role. Prints out environment variables
    to be eval'd to current context for use:
    eval $(ndt assume-role 'arn:aws:iam::43243246645:role/DeployRole')
    """
    parser = get_parser()
    parser.add_argument("role_arn", help="The ARN of the role to assume")
    parser.add_argument(
        "-t",
        "--mfa-token",
        metavar="TOKEN_NAME",
        help="Name of MFA token to use",
        required=False,
    )
    parser.add_argument(
        "-d",
        "--duration",
        help="Duration for the session in minutes",
        default="60",
        type=int,
        required=False,
    )
    parser.add_argument(
        "-p",
        "--profile",
        help="Profile to edit in ~/.aws/credentials "
        + "to make role persist in that file for "
        + "the duration of the session.",
        required=False,
    )
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    creds = utils.assume_role(args.role_arn, mfa_token_name=args.mfa_token, duration_minutes=args.duration)
    if args.profile:
        update_profile(args.profile, creds)
    else:
        print('AWS_ROLE_ARN="' + args.role_arn + '"')
        print('AWS_ACCESS_KEY_ID="' + creds["AccessKeyId"] + '"')
        print('AWS_SECRET_ACCESS_KEY="' + creds["SecretAccessKey"] + '"')
        print('AWS_SESSION_TOKEN="' + creds["SessionToken"] + '"')
        print('AWS_SESSION_EXPIRATION="' + creds["Expiration"].strftime("%a, %d %b %Y %H:%M:%S +0000") + '"')
        print("export AWS_ROLE_ARN AWS_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY AWS_SESSION_TOKEN AWS_SESSION_EXPIRATION")


def session_to_env():
    """Export current session as environment variables"""
    parser = get_parser()
    parser.add_argument("-t", "--token-name", help="Name of the mfs token to use.").completer = ChoicesCompleter(
        list_mfa_tokens()
    )
    parser.add_argument(
        "-d",
        "--duration-minutes",
        type=int,
        default=60,
        help="Duration in minutes for the session token. Default to 60",
    )
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    call_args = {"duration_minutes": args.duration_minutes}
    if args.token_name:
        call_args["token_arn"] = mfa_read_token(args.token_name)["token_arn"]
        call_args["token_value"] = mfa_generate_code(args.token_name)

    profile_type = None
    if "AWS_PROFILE" in os.environ:
        profile_type = resolve_profile_type(os.environ["AWS_PROFILE"])
    if profile_type == "sso":
        profile = get_profile(os.environ["AWS_PROFILE"])
        cache_json = read_sso_profile(os.environ["AWS_PROFILE"])
        if "accessToken" in cache_json and cache_json["accessToken"]:
            access_token = cache_json["accessToken"]
            creds = sso(region=profile["sso_region"]).get_role_credentials(
                roleName=profile["sso_role_name"], accountId=profile["sso_account_id"], accessToken=access_token
            )
            role_creds = creds["roleCredentials"]
            print(f"AWS_ACCESS_KEY_ID='{role_creds['accessKeyId']}'")
            print(f"AWS_SECRET_ACCESS_KEY='{role_creds['secretAccessKey']}'")
            print(f"AWS_SESSION_TOKEN='{role_creds['sessionToken']}'")
            print('AWS_SESSION_EXPIRATION="' + _epoc_to_str(role_creds["expiration"] / 1000) + '"')
            print("export AWS_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY AWS_SESSION_TOKEN AWS_SESSION_EXPIRATION")
    elif profile_type in ["azure", "adfs", "lastpass"]:
        profile = get_profile(os.environ["AWS_PROFILE"], include_creds=True)
        print(f"AWS_ACCESS_KEY_ID='{profile['aws_access_key_id']}'")
        print(f"AWS_SECRET_ACCESS_KEY='{profile['aws_secret_access_key']}'")
        print(f"AWS_SESSION_TOKEN='{profile['aws_session_token']}'")
        print(f"AWS_SESSION_EXPIRATION='{profile['aws_session_expiration']}'")
        print("export AWS_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY AWS_SESSION_TOKEN AWS_SESSION_EXPIRATION")
    else:
        creds = session_token(**call_args)
        if creds:
            print('AWS_ACCESS_KEY_ID="' + creds["AccessKeyId"] + '"')
            print('AWS_SECRET_ACCESS_KEY="' + creds["SecretAccessKey"] + '"')
            print('AWS_SESSION_TOKEN="' + creds["SessionToken"] + '"')
            print('AWS_SESSION_EXPIRATION="' + creds["Expiration"].strftime("%a, %d %b %Y %H:%M:%S +0000") + '"')
            print("export AWS_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY AWS_SESSION_TOKEN AWS_SESSION_EXPIRATION")


def clean_snapshots():
    """Clean snapshots that are older than a number of days (30 by default) and
    have one of specified tag values
    """
    parser = get_parser()
    parser.add_argument(
        "-r",
        "--region",
        help="The region to delete "
        + "snapshots from. Can also be "
        + "set with env variable "
        + "AWS_DEFAULT_REGION or is "
        + "gotten from instance "
        + "metadata as a last resort",
    )
    parser.add_argument(
        "-d",
        "--days",
        help="The number of days that is the" + "minimum age for snapshots to " + "be deleted",
        type=int,
        default=30,
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Do not delete, but print what would be deleted",
    )
    parser.add_argument("tags", help="The tag values to select deleted " + "snapshots", nargs="+")
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    if args.region:
        os.environ["AWS_DEFAULT_REGION"] = args.region
    ebs.clean_snapshots(args.days, args.tags, dry_run=args.dry_run)


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
    """Show stack parameters and outputs as a single json documents"""
    parser = get_parser()
    parser.add_argument(
        "-r", "--region", help="Region for the stack to show", default=region()
    ).completer = ChoicesCompleter(regions())
    parser.add_argument(
        "-p",
        "--parameter",
        help="Name of paremeter if only" + " one parameter required",
    )
    parser.add_argument("stack_name", help="The stack name to show").completer = ChoicesCompleter(best_effort_stacks())
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    resp, _ = stack_params_and_outputs_and_stack(stack_name=args.stack_name, stack_region=args.region)
    if args.parameter:
        if args.parameter in resp:
            print(resp[args.parameter])
        else:
            parser.error("Parameter " + args.parameter + " not found")
    else:
        print(json.dumps(resp, indent=2))


def show_terraform_params():
    """Show available parameters for a terraform subcomponent"""
    parser = get_parser()
    parser.add_argument(
        "component", help="The component containg the terraform subcomponet"
    ).completer = ChoicesCompleter(component_having_a_subcomponent_of_type("terraform"))
    parser.add_argument("terraform", help="The name of the terraform subcomponent").completer = SubCCompleter(
        "terraform"
    )
    param = parser.add_mutually_exclusive_group(required=False)
    param.add_argument("-j", "--jmespath", help="Show just a matching jmespath value")
    param.add_argument(
        "-p",
        "--parameter",
        help="Name of paremeter if only" + " one parameter required",
    )
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


def show_azure_params():
    """Show available parameters for a azure subcomponent"""
    parser = get_parser()
    parser.add_argument("component", help="The component containg the azure subcomponet").completer = ChoicesCompleter(
        component_having_a_subcomponent_of_type("azure")
    )
    parser.add_argument("azure", help="The name of the azure subcomponent").completer = SubCCompleter("azure")
    param = parser.add_mutually_exclusive_group(required=False)
    param.add_argument(
        "-p",
        "--parameter",
        help="Name of paremeter if only" + " one parameter required",
    )
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    azure = fetch_properties(load_parameters(component=args.component, azure=args.azure))
    if args.parameter:
        if args.parameter in azure:
            print(azure[args.parameter])
    else:
        print(json.dumps(azure, indent=2))


def cli_get_images():
    """Gets a list of images given a bake job name"""
    parser = get_parser()
    parser.add_argument("job_name", help="The job name to look for")
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    images = get_images(args.job_name)
    for image in images:
        print(image["ImageId"] + ":" + image["Name"])


def cli_promote_image():
    """Promotes an image for use in another branch"""
    parser = get_parser()
    parser.add_argument("image_id", help="The image to promote")
    parser.add_argument("target_job", help="The job name to promote the image to")
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    if ":" in args.image_id:
        args.image_id = args.image_id.split(":")[0]
    promote_image(args.image_id, args.target_job)


def cli_share_to_another_region():
    """Shares an image to another region for potentially another account"""
    parser = get_parser()
    parser.add_argument("ami_id", help="The ami to share")
    parser.add_argument("to_region", help="The region to share to").completer = ChoicesCompleter(regions())
    parser.add_argument("ami_name", help="The name for the ami")
    parser.add_argument("account_id", nargs="+", help="The account ids to sh" + "are ami to")
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    share_to_another_region(args.ami_id, args.to_region, args.ami_name, args.account_id)


def cli_interpolate_file():
    """Replace placeholders in file with parameter values from stack and
    optionally from vault
    """
    parser = get_parser()
    parser.add_argument(
        "-s",
        "--stack",
        help="Stack name for values. " + "Automatically resolved on ec2" + " instances",
    )
    parser.add_argument(
        "-k",
        "--skip-stack",
        help="Skip stack parameters in" + " all cases",
        action="store_true",
    )
    parser.add_argument(
        "-n",
        "--use-environ",
        help="Use environment variables" + " for interpolation",
        action="store_true",
    )
    parser.add_argument(
        "-v",
        "--vault",
        help="Use vault values as well." + "Vault resovled from env " + "variables or default is used",
        action="store_true",
    )
    parser.add_argument("-o", "--output", help="Output file")
    parser.add_argument(
        "-e",
        "--encoding",
        help="Encoding to use for the " + "file. Defaults to utf-8",
        default="utf-8",
    )
    parser.add_argument("file", help="File to interpolate").completer = FilesCompleter()
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    interpolate_file(
        args.file,
        stack_name=args.stack,
        use_vault=args.vault,
        destination=args.output,
        use_environ=args.use_environ,
        skip_stack=args.skip_stack,
        encoding=args.encoding,
    )


def cli_ecr_ensure_repo():
    """Ensure that an ECR repository exists and get the uri and login token for
    it"""
    parser = get_parser()
    parser.add_argument("name", help="The name of the ecr repository to verify")
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    ensure_repo(args.name)


def cli_ecr_repo_uri():
    """Get the repo uri for a named docker"""
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
    """Upsert Route53 records for all aliases of a CloudFront distribution"""
    parser = get_parser()
    stack_select = parser.add_mutually_exclusive_group(required=True)
    stack_select.add_argument(
        "-i", "--distribution_id", help="Id for the " + "distribution to " + "upsert"
    ).completer = ChoicesCompleter(distributions())
    stack_select.add_argument(
        "-c",
        "--distribution_comment",
        help="Comment for the" + " distribution " + "to upsert",
    ).completer = ChoicesCompleter(distribution_comments())
    parser.add_argument("-w", "--wait", help="Wait for request to sync", action="store_true")
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    upsert_cloudfront_records(args)


def cli_mfa_add_token():
    """Adds an MFA token to be used with role assumption.
    Tokens will be saved in a .ndt subdirectory in the user's home directory.
    If a token with the same name already exists, it will not be overwritten."""
    parser = get_parser()
    parser.add_argument(
        "token_name",
        help="Name for the token. Use this to refer to the token later with " + "the assume-role command.",
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-i",
        "--interactive",
        help="Ask for token details interactively.",
        action="store_true",
    )
    group.add_argument(
        "-b",
        "--bitwarden-entry",
        help="Use a bitwarden entry as the source of the totp secret",
    )
    parser.add_argument("-a", "--token_arn", help="ARN identifier for the token.")
    parser.add_argument("-s", "--token_secret", help="Token secret.")
    parser.add_argument(
        "-f",
        "--force",
        help="Force an overwrite if the token already exists.",
        action="store_true",
    )
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
    elif not (args.token_secret or args.bitwarden_entry):
        parser.error("Token secret is required.")
    try:
        mfa_add_token(args)
    except ValueError as error:
        parser.error(error)


def cli_mfa_delete_token():
    """Deletes an MFA token file from the .ndt subdirectory in the user's
    home directory"""
    parser = get_parser()
    parser.add_argument("token_name", help="Name of the token to delete.").completer = ChoicesCompleter(
        list_mfa_tokens()
    )
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    mfa_delete_token(args.token_name)


def cli_mfa_code():
    """Generates a TOTP code using an MFA token."""
    parser = get_parser()
    parser.add_argument("token_name", help="Name of the token to use.").completer = ChoicesCompleter(list_mfa_tokens())
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    print(mfa_generate_code(args.token_name))


def cli_mfa_to_qrcode():
    """Generates a QR code to import a token to other devices."""
    parser = get_parser()
    parser.add_argument("token_name", help="Name of the token to use.").completer = ChoicesCompleter(list_mfa_tokens())
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    mfa_to_qrcode(args.token_name)


def cli_mfa_backup_tokens():
    """Encrypt or decrypt a backup JSON structure of tokens.

    To output an encrypted backup, provide an encryption secret.

    To decrypt an existing backup, use --decrypt <file>.
    """
    parser = get_parser()
    parser.add_argument("backup_secret", help="Secret to use for encrypting or decrypts the backup.")
    parser.add_argument(
        "-d",
        "--decrypt",
        help="Outputs a decrypted token backup read from given file.",
        nargs=1,
        metavar="FILE",
    )
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    if args.decrypt:
        print(mfa_decrypt_backup_tokens(args.backup_secret, args.decrypt[0]))
    else:
        print(mfa_backup_tokens(args.backup_secret))


def cli_create_account():
    """Creates a subaccount."""
    parser = get_parser()
    parser.add_argument("email", help="Email for account root")
    parser.add_argument("account_name", help="Organization unique account name")
    parser.add_argument("-d", "--deny-billing-access", action="store_true")
    parser.add_argument(
        "-o",
        "--organization-role-name",
        help="Role name for " + "admin access from" + " parent account",
        default="OrganizationAccountAccessRole",
    )
    parser.add_argument(
        "-r",
        "--trust-role-name",
        help="Role name for admin " + "access from parent account",
        default="TrustedAccountAccessRole",
    )
    parser.add_argument(
        "-a",
        "--trusted-accounts",
        nargs="*",
        help="Account to trust with user management",
    ).completer = ChoicesCompleter(list_created_accounts())
    parser.add_argument(
        "-t",
        "--mfa-token",
        metavar="TOKEN_NAME",
        help="Name of MFA token to use",
        required=False,
    )
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    create_account(
        args.email,
        args.account_name,
        role_name=args.organization_role_name,
        trust_role=args.trust_role_name,
        access_to_billing=not args.deny_billing_access,
        trusted_accounts=args.trusted_accounts,
        mfa_token=args.mfa_token,
    )


def cli_load_parameters():
    """Load parameters from infra*.properties files in the order:
    branch.properties
    [branch].properties
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
    parser.add_argument("component", nargs="?", help="Compenent to descend into").completer = ChoicesCompleter(
        [c.name for c in Project().get_components()]
    )
    parser.add_argument("--branch", "-b", help="Branch to get active parameters for").completer = ChoicesCompleter(
        Git().get_branches()
    )
    parser.add_argument(
        "--resolve-images",
        "-r",
        action="store_true",
        help="Also resolve subcomponent AMI IDs and docker repo urls",
    )
    subcomponent_group = parser.add_mutually_exclusive_group()
    subcomponent_group.add_argument(
        "--stack", "-s", help="CloudFormation subcomponent to descent into"
    ).completer = SubCCompleter("stack")
    subcomponent_group.add_argument(
        "--serverless", "-l", help="Serverless subcomponent to descent into"
    ).completer = SubCCompleter("serverless")
    subcomponent_group.add_argument(
        "--docker", "-d", help="Docker image subcomponent to descent into"
    ).completer = SubCCompleter("docker")
    subcomponent_group.add_argument(
        "--image",
        "-i",
        const="",
        nargs="?",
        help="AMI image subcomponent to descent into",
    ).completer = SubCCompleter("image")
    subcomponent_group.add_argument("--cdk", "-c", help="CDK subcomponent to descent into").completer = SubCCompleter(
        "cdk"
    )
    subcomponent_group.add_argument(
        "--terraform", "-t", help="Terraform subcomponent to descent into"
    ).completer = SubCCompleter("terraform")
    subcomponent_group.add_argument(
        "--azure", "-a", help="Azure subcomponent to descent into"
    ).completer = SubCCompleter("azure")
    subcomponent_group.add_argument(
        "--connect", "-n", help="Connect subcomponent to descent into"
    ).completer = SubCCompleter("connect")
    format_group = parser.add_mutually_exclusive_group()
    format_group.add_argument("--json", "-j", action="store_true", help="JSON format output (default)")
    format_group.add_argument("--yaml", "-y", action="store_true", help="YAML format output")
    format_group.add_argument("--properties", "-p", action="store_true", help="properties file format output")
    format_group.add_argument(
        "--terraform-variables",
        "-v",
        action="store_true",
        help="terraform syntax variables",
    )
    format_group.add_argument(
        "--export-statements",
        "-e",
        action="store_true",
        help="Output as eval-able export statements",
    )
    format_group.add_argument(
        "--azure-parameters",
        "-z",
        action="store_true",
        help="Azure parameter file syntax variables",
    )
    parser.add_argument("-f", "--filter", help="Comma separated list of parameter names to output")
    argcomplete.autocomplete(parser)
    args = parser.parse_args()

    transform = json.dumps
    if args.export_statements:
        transform = map_to_exports
    if args.properties:
        transform = map_to_properties
    if args.yaml:
        transform = yaml.dump
    if args.terraform_variables:
        transform = map_to_tfvars
    if args.azure_parameters:
        transform = map_to_azure_params
    del args.export_statements
    del args.yaml
    del args.json
    del args.properties
    del args.terraform_variables
    del args.azure_parameters

    if (
        args.stack
        or args.serverless
        or args.docker
        or args.azure
        or args.connect
        or args.cdk
        or args.terraform
        or not isinstance(args.image, NoneType)
    ) and not args.component:
        parser.error(
            "image, stack, doker, serverless, azure, connect, cdk or terraform do not make sense without component"
        )
    filter_arr = []
    if args.filter:
        filter_arr = args.filter.split(",")
        filter_types = {}
        for filter_entry in filter_arr.copy():
            if len(filter_entry.split(":")) > 1:
                filter_arr = list(map(lambda x: x.replace(filter_entry, filter_entry.split(":")[0]), filter_arr))
                filter_types[filter_entry.split(":")[0]] = filter_entry.split(":")[1]
    del args.filter
    parameters = load_parameters(**vars(args))
    if filter_arr:
        for param_key in set(parameters.keys()):
            if param_key not in filter_arr:
                del parameters[param_key]
            elif param_key in filter_types:
                _cast_param(param_key, parameters, filter_types[param_key])
    print(transform(parameters))


def _cast_param(key, params, param_type):
    if param_type == "int":
        params[key] = int(params[key])
    elif param_type == "bool":
        params[key] = params[key] and params[key].lower() == "true"
    return


class SubCCompleter:
    def __init__(self, sc_type):
        self.sc_type = sc_type

    def __call__(self, prefix="", action=None, parser=None, parsed_args=None):
        p_args = {}
        if hasattr(parsed_args, "branch") and parsed_args.branch:
            p_args["branch"] = parsed_args.branch
        if hasattr(parsed_args, "component") and parsed_args.component:
            return [
                sc.name
                for sc in Project(**p_args).get_component(parsed_args.component).get_subcomponents()
                if sc.type == self.sc_type and sc.name.startswith(prefix)
            ]
        else:
            return [sc.name for sc in Project(**p_args).get_all_subcomponents() if sc.type == self.sc_type]
        return None


def map_to_exports(map):
    """Prints the map as eval-able set of environment variables. Keys
    will be cleaned of all non-word letters and values will be escaped so
    that they will be exported as literal values."""
    ret = ""
    keys = []
    for key, val in list(map.items()):
        if isinstance(val, str):
            value = "'" + val.replace("'", "'\"'\"'") + "'"
        elif isinstance(val, list):
            value = "("
            for elem in val:
                if isinstance(elem, str):
                    value += "'" + elem.replace("'", "'\"'\"'") + "' "
                else:
                    value += "'" + json_save_small(elem).replace("'", "'\"'\"'") + "' "
            value = value[:-1] + ")"
        else:
            value = "'" + json_save_small(val) + "'"
        key = re.sub("[^a-zA-Z0-9_]", "", key)
        ret += key + "=" + value + os.linesep
        keys.append(key)
    ret += "export " + " ".join(keys) + os.linesep
    return ret


def map_to_properties(map):
    """Prints the map as loadable set of java properties. Keys
    will be cleaned of all non-word letters."""
    ret = ""
    for key, val in list(map.items()):
        key = re.sub("[^a-zA-Z0-9_]", "", key)
        if isinstance(val, str):
            ret += key + "=" + val + os.linesep
        else:
            ret += key + "=" + json_save_small(val) + os.linesep
    return ret


def map_to_tfvars(map):
    """Prints the map in terraform syntax variables"""
    ret = ""
    for key, val in list(map.items()):
        if "${" not in val:
            ret += key + "=" + json.dumps(val) + "\n"
    return ret


def map_to_azure_params(map):
    """Prints the map in azure parameter file syntax"""
    ret_map = {
        "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentParameters.json#",
        "contentVersion": "1.0.0.0",
        "parameters": {},
    }
    for key, val in list(map.items()):
        ret_map["parameters"][key] = {"value": val}
    return json.dumps(ret_map)


def cli_assumed_role_name():
    """Read the name of the assumed role if currently defined"""
    parser = get_parser()
    argcomplete.autocomplete(parser)
    _ = parser.parse_args()
    print(assumed_role_name())


def cli_list_jobs():
    """Prints a line for every runnable job in this git repository, in all branches and
    optionally exports the properties for each under '$root/job-properties/"""
    parser = get_parser()
    parser.add_argument(
        "-e",
        "--export-job-properties",
        action="store_true",
        help="Set if you want the properties of all jobs into files under job-properties/",
    )
    parser.add_argument(
        "-j",
        "--json",
        action="store_true",
        help="Print in json format. Optionally " "exported parameters will be in the json document",
    )
    parser.add_argument(
        "-b",
        "--branch",
        help="The branch to process. Default is to process all branches",
    ).completer = ChoicesCompleter(Git().get_branches())
    parser.add_argument(
        "-c",
        "--component",
        help="Component to process. Default is to process all components",
    ).completer = branch_components
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
    """Prints the components in a branch, by default the current branch"""
    parser = get_parser()
    parser.add_argument("-j", "--json", action="store_true", help="Print in json format.")
    parser.add_argument(
        "-b",
        "--branch",
        help="The branch to get components from. Default is to process current branch",
    ).completer = ChoicesCompleter(Git().get_branches())
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    ret = list_components(**vars(args))
    if args.json:
        print(json.dumps(ret, indent=2))
    else:
        print("\n".join(ret))


def cli_upsert_codebuild_projects():
    """
    Creates or updates codebuild projects to deploy or bake ndt subcomponents in the current branch.

    Parameters are read from properties files as described in 'ndt load-parameters -h'.
    To check all job paramters you can run 'ndt list-jobs -e -j -b [current-branch]'
    The only mandatory parameter is CODEBUILD_SERVICE_ROLE,
    which defines the role that the codebuild project assumes for building.
    Other parameters that affect jobs are:
    * BUILD_JOB_NAME - name for the codebuild project
    * NDT_VERSION - version to use to run bakes and deployments.
        - Defaults to current version.
        - You may also want to uses 'latest' to always run the latest released ndt version (only recommended for dev/testing workloads).
    * BUILD_SPEC - file or yaml snippet to use as the build definition.
        - See https://docs.aws.amazon.com/codebuild/latest/userguide/build-spec-ref.html
        - subcomponent variables and special variables ${command}, ${component} and ${subcomponent} are available and will be substituted accordingly
    * CODEBUILD_SOURCE_TYPE - one of BITBUCKET, CODECOMMIT, CODEPIPELINE, GITHUB, GITHUB_ENTERPRISE, NO_SOURCE, S3
    * CODEBUILD_SOURCE_LOCATION - the location of the source code
        - if either of the above is missing, then the source part of the build will be omitted
    * CODEBUILD_EVENT_FILTER - the type of event to trigger the build.
        - By default PULL_REQUEST_MERGED
        - Other possible values: PUSH, PULL_REQUEST_CREATED, PULL_REQUEST_UPDATED and PULL_REQUEST_REOPENED
    * CODEBUILD_TIMEOUT - timeout in minutes for the codebuild execution. 60 by default
    * BUILD_ENVIRONMENT_COMPUTE - the compute environment for the build.
        - BUILD_GENERAL1_SMALL by default
        - Other possible values BUILD_GENERAL1_MEDIUM, BUILD_GENERAL1_LARGE, BUILD_GENERAL1_2XLARGE
    * NEEDS_DOCKER - if 'y' (by default on for docker bakes and missing otheriwise), docker server is started inside the container
        - Needed for bakes and for example serverless python dockerized dependencies
    * SKIP_BUILD_JOB - skip creating build jobs where this parameter is 'y'
    * SKIP_IMAGE_JOB, SKIP_DOCKER_JOB, SKIP_SERVERLESS_JOB, SKIP_CDK_JOB, SKIP_TERRAFORM_JOB - skip creating jobs where these parameters are 'y' and match the subcomponent type
    """  # noqa
    parser = get_parser(formatter=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "-d",
        "--dry-run",
        action="store_true",
        help="Do not actually create or update projects, just print configuration",
    )
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    upsert_codebuild_projects(dry_run=args.dry_run)


def upsert_dns_record():
    """Update a dns record in Route53."""
    parser = get_parser()
    parser.add_argument("name", help="The name of the record to create")
    parser.add_argument(
        "-t",
        "--type",
        help="The type of record to create. Defaults to 'A'",
        default="A",
    )
    parser.add_argument("value", help="The value to put into the record")
    parser.add_argument(
        "-l",
        "--ttl",
        help="Time To Live for the record. Defaults to 300",
        default=300,
        type=int,
    )
    parser.add_argument(
        "-n",
        "--no-wait",
        help="Do not wait for the record to be synced within Route53",
        action="store_false",
    )
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    upsert_record(args.name, args.type, args.value, ttl=args.ttl, wait=args.no_wait)


def azure_ensure_group():
    """Ensures that an azure resource group exists."""
    parser = get_parser()
    parser.add_argument(
        "-l",
        "--location",
        help="The location for the resource group. If not defined looked from the environment "
        + "variable AZURE_LOCATION and after that seen if location is defined for the project.",
    )
    parser.add_argument("name", help="The name of the resource group to make sure exists")
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    if not args.location:
        args.location = resolve_location()
    ensure_group(args.location, args.name)


def azure_ensure_management_group():
    """Ensures that an azure resource group exists."""
    parser = get_parser()
    parser.add_argument("name", help="The name of the resource group to make sure exists")
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    ensure_management_group(args.name)


def azure_template_parameters():
    """Lists the parameters in an Azure Resource Manager template"""
    parser = get_parser()
    parser.add_argument("template", help="The json template to scan for parameters").competer = FilesCompleter()
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    template = {}
    if args.template.endswith(".bicep"):
        process = Popen(["az", "bicep", "build", "--file", args.template, "--stdout"], stdout=PIPE, stderr=PIPE)
        out, _ = process.communicate()
        template = json.loads(out)
    else:
        template = json_load(open(args.template).read())
    parameters = []
    if "parameters" in template and template["parameters"]:
        for param in template["parameters"]:
            parameters.append(f"{param}:{template['parameters'][param]['type']}")
        print(",".join(parameters))


def azure_location():
    """
    Resolve an azure location based on 'AZURE_LOCATION' enviroment variable, local project or az cli configuration.
    Defaults to 'northeurope'
    """
    parser = get_parser()
    argcomplete.autocomplete(parser)
    _ = parser.parse_args()
    print(resolve_location())


def resolve_location():
    if "AZURE_LOCATION" in os.environ and os.environ["AZURE_LOCATION"] and os.environ["AZURE_LOCATION"] != "default":
        return os.environ["AZURE_LOCATION"]
    else:
        parameters = load_parameters()
        if (
            "AZURE_LOCATION" in parameters
            and parameters["AZURE_LOCATION"]
            and parameters["AZURE_LOCATION"] != "default"
        ):
            return parameters["AZURE_LOCATION"]
        else:
            proc = Popen(
                ["az", "configure", "--list-defaults"],
                stdout=PIPE,
                stderr=PIPE,
            )
            default_location = None
            output, err = proc.communicate()
            if proc.returncode == 0 and output:
                confs = json.loads(output)
                for conf in confs:
                    if "name" in conf and conf["name"] == "location" and "value" in conf and conf["value"]:
                        default_location = conf["value"]
            if default_location:
                return default_location
            else:
                return "northeurope"


def deploy_connect_contact_flows():
    """Deploy AWS Connect contact flows from a subcomponent"""
    parser = get_parser()
    parser.add_argument(
        "component",
        help="the component directory where the connect contact flow directory is",
    ).completer = ChoicesCompleter(component_having_a_subcomponent_of_type("connect"))
    parser.add_argument(
        "contactflowname",
        help="the name of the connect subcomponent directory that has the contact flow template",
    ).completer = SubCCompleter("connect")
    parser.add_argument(
        "-d",
        "--dryrun",
        help="Dry run - don't do changes but show what would happen of deployed",
        action="store_true",
    )
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    connect.deploy_connect_contact_flows(args.component, args.contactflowname, dry_run=args.dryrun)


def export_connect_contact_flow():
    """Export AWS Connect contact flow from an existing instance"""
    parser = get_parser()
    parser.add_argument(
        "-c",
        "--component",
        help="the component directory where the connect contact flow directory is",
    ).completer = ChoicesCompleter(component_having_a_subcomponent_of_type("connect"))
    parser.add_argument(
        "-f",
        "--contactflowname",
        help="the name of the connect subcomponent directory that has the contact flow template",
    ).completer = SubCCompleter("connect")
    instance_sel = parser.add_mutually_exclusive_group()
    instance_sel.add_argument(
        "-i", "--instanceid", help="id of the connect instance to export from"
    ).completer = lambda **kwargs: connect.get_instance_ids()
    instance_sel.add_argument(
        "-a", "--instancealias", help="alias of the connect instance to export from"
    ).completer = lambda **kwargs: connect.get_instance_aliases()
    parser.add_argument("--colorize", "-o", help="Colorize output", action="store_true")
    parser.add_argument("name", help="The name of the contact flow to export").competer = FlowNameCompleter()
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    instance_id = _resolve_connect_instance(args)
    if not instance_id:
        parser.error("Need to define an instance, either with an id or alias or by referring to a connect template.")
    out = connect.export_connect_contact_flow(instance_id, args.name)
    if args.colorize:
        colorprint(out)
    else:
        print(out)


def list_connect_contact_flows():
    """List existing AWS Connect contact flows in an instance"""
    parser = get_parser()
    parser.add_argument(
        "-c",
        "--component",
        help="the component directory where the connect contact flow directory is",
    ).completer = ChoicesCompleter(component_having_a_subcomponent_of_type("connect"))
    parser.add_argument(
        "-f",
        "--contactflowname",
        help="the name of the connect subcomponent directory that has the contact flow template",
    ).completer = SubCCompleter("connect")
    instance_sel = parser.add_mutually_exclusive_group()
    instance_sel.add_argument(
        "-i", "--instanceid", help="id of the connect instance to export from"
    ).completer = lambda **kwargs: connect.get_instance_ids()
    instance_sel.add_argument(
        "-a", "--instancealias", help="alias of the connect instance to export from"
    ).completer = lambda **kwargs: connect.get_instance_aliases()
    parser.add_argument("-t", "--trash", help="Include trashed flows", action="store_true")
    parser.add_argument("-m", "--match", help="Pattern to match printed flows")
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    instance_id = _resolve_connect_instance(args)
    if not instance_id:
        parser.error("Need to define an instance, either with an id or alias or by referring to a connect template.")
    for flow in connect.get_flows(instance_id).keys():
        if not flow.startswith("zzTrash_") or args.trash:
            if not args.match or re.match(args.match, flow):
                print(flow)


def component_having_a_subcomponent_of_type(subcomponent_type):
    ret = []
    for dir in [x for x in next(os.walk("."))[1] if not x.startswith(".")]:
        for subd in next(os.walk(dir))[1]:
            if subd.startswith(subcomponent_type + "-") and dir not in ret:
                ret.append(dir)
    return ret


def _resolve_connect_instance(args):
    if not args:
        return None
    if hasattr(args, "instanceid") and args.instanceid:
        return args.instanceid
    if hasattr(args, "instancealias") and args.instancealias:
        return connect.alias_to_id(args.instancealias)
    if hasattr(args, "component") and args.component and hasattr(args, "contactflowname") and args.contactflowname:
        template_dir = (
            Project().get_component(args.component).get_subcomponent("connect", args.contactflowname).get_dir()
        )
        flow_template = yaml_to_dict(template_dir + os.sep + "template.yaml")
        if "connectInstanceId" in flow_template:
            return flow_template["connectInstanceId"]
    return None


class FlowNameCompleter:
    def __call__(self, prefix="", action=None, parser=None, parsed_args=None):
        instance_id = _resolve_connect_instance(parsed_args)
        if instance_id:
            return [flow for flow in connect.get_flows(instance_id).keys() if flow.startswith(prefix)]
