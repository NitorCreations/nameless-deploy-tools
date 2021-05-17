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
import six
import sys
import time
from builtins import input
from builtins import str

import argcomplete
import yaml
from argcomplete.completers import ChoicesCompleter, FilesCompleter
from ec2_utils import ebs, interface
from ec2_utils.instance_info import stack_params_and_outputs_and_stack, dthandler
from ec2_utils.logs import CloudWatchLogsThread
from ec2_utils.utils import best_effort_stacks
from pygments import highlight, lexers, formatters
from pygments.styles import get_style_by_name
from threadlocal_aws import region, regions

from n_utils import aws_infra_util, cf_bootstrap, cf_deploy, utils, \
    _to_bytes, _to_str
from n_utils.account_utils import list_created_accounts, create_account
from n_utils.aws_infra_util import load_parameters, json_save_small, json_load
from n_utils.cloudfront_utils import distributions, distribution_comments, \
    upsert_cloudfront_records
from n_utils.ecr_utils import ensure_repo, repo_uri
from n_utils.git_utils import Git
from n_utils.log_events import CloudFormationEvents
from n_utils.maven_utils import add_server
from n_utils.mfa_utils import mfa_add_token, mfa_delete_token, mfa_generate_code, \
    mfa_generate_code_with_secret, list_mfa_tokens, mfa_backup_tokens, mfa_decrypt_backup_tokens, \
    mfa_to_qrcode, mfa_read_token
from n_utils.ndt import find_include, find_all_includes, include_dirs
from n_utils.ndt_project import Project
from n_utils.ndt_project import list_jobs, list_components, upsert_codebuild_projects
from n_utils.profile_util import update_profile
from n_utils.tf_utils import pull_state, jmespath_var, flat_state
from n_utils.utils import session_token, get_images, promote_image, \
    share_to_another_region, interpolate_file, assumed_role_name
from n_utils.az_util import ensure_group, ensure_management_group
from n_utils.route53_util import upsert_record
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
        dump = lambda out_doc: json.dumps(out_doc, indent=2, default=dthandler)
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
    interface.associate_eip(eip=args.ip, allocation_id=args.allocationid,
                            eip_param=args.eipparam,
                            allocation_id_param=args.allocationidparam)


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
    creds = utils.assume_role(args.role_arn, mfa_token_name=args.mfa_token,
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
    if creds:
        print("AWS_ACCESS_KEY_ID=\"" + creds['AccessKeyId'] + "\"")
        print("AWS_SECRET_ACCESS_KEY=\"" + creds['SecretAccessKey'] + "\"")
        print("AWS_SESSION_TOKEN=\"" + creds['SessionToken'] + "\"")
        print("AWS_SESSION_EXPIRATION=\"" + creds['Expiration'].strftime("%a, %d %b %Y %H:%M:%S +0000") + "\"")
        print("export AWS_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY AWS_SESSION_TOKEN AWS_SESSION_EXPIRATION")


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
    parser.add_argument("--dry-run", action="store_true",
                        help="Do not delete, but print what would be deleted")
    parser.add_argument("tags", help="The tag values to select deleted " +
                                     "snapshots", nargs="+")
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    if args.region:
        os.environ['AWS_DEFAULT_REGION'] = args.region
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
    """ Show stack parameters and outputs as a single json documents
    """
    parser = get_parser()
    parser.add_argument("-r", "--region", help="Region for the stack to show",
                        default=region()).completer = ChoicesCompleter(regions())
    parser.add_argument("-p", "--parameter", help="Name of paremeter if only" +
                                                  " one parameter required")
    parser.add_argument("stack_name", help="The stack name to show").completer = \
        ChoicesCompleter(best_effort_stacks())
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
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-i", "--interactive", help="Ask for token details interactively.",
                        action="store_true")
    group.add_argument("-b", "--bitwarden-entry", help="Use a bitwarden entry as the source of the totp secret")
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
    elif not (args.token_secret or args.bitwarden_entry):
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
    subcomponent_group.add_argument("--azure", "-a", help="Terraform subcomponent to descent into").completer = \
        lambda prefix, parsed_args, **kwargs: component_typed_subcomponents("terraform", prefix, parsed_args, **kwargs)
    format_group = parser.add_mutually_exclusive_group()
    format_group.add_argument("--json", "-j", action="store_true", help="JSON format output (default)")
    format_group.add_argument("--yaml", "-y", action="store_true", help="YAML format output")
    format_group.add_argument("--properties", "-p", action="store_true", help="properties file format output")
    format_group.add_argument("--terraform-variables", "-v", action="store_true", help="terraform syntax variables")
    format_group.add_argument("--export-statements", "-e", action="store_true",
                              help="Output as eval-able export statements")
    format_group.add_argument("--azure-parameters", "-z", action="store_true", help="Azure parameter file syntax variables")
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
    if (args.stack or args.serverless or args.docker or args.azure or not isinstance(args.image, NoneType)) \
       and not args.component:
        parser.error("image, stack, doker or serverless, azure do not make sense without component")
    filter_arr = []
    if args.filter:
        filter_arr = args.filter.split(",")
    del args.filter
    parameters = load_parameters(**vars(args))
    if filter_arr:
        for param_key in set(parameters.keys()):
            if param_key not in filter_arr:
                del parameters[param_key]
    print(transform(parameters))

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
        if isinstance(val, six.string_types):
            value = "'" + val.replace("'", "'\"'\"'") + "'"
        elif isinstance(val, list):
            value = "("
            for elem in val:
                if isinstance(elem, six.string_types):
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
    """ Prints the map as loadable set of java properties. Keys
    will be cleaned of all non-word letters."""
    ret = ""
    for key, val in list(map.items()):
        key = re.sub("[^a-zA-Z0-9_]", "", key)
        if isinstance(val, six.string_types):
            ret += key + "=" + val + os.linesep
        else:
            ret += key + "=" + json_save_small(val) + os.linesep
    return ret

def map_to_tfvars(map):
    """ Prints the map in terraform syntax variables
    """
    ret = ""
    for key, val in list(map.items()):
        if "${" not in val:
            ret += key + "=" + json.dumps(val) + "\n"
    return ret

def map_to_azure_params(map):
    """ Prints the map in azure parameter file syntax
    """
    ret_map = {
        "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentParameters.json#",
        "contentVersion": "1.0.0.0",
        "parameters": {}
    }
    for key, val in list(map.items()):
        ret_map["parameters"][key] = {
            "value": val
        }
    return json.dumps(ret_map)

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

def cli_upsert_codebuild_projects():
    """ Creates or updates codebuild projects to deploy or bake ndt subcomponents in the current branch.

    Parameters are read from properties files as described in 'ndt load-parameters -h'. To check all job paramters you
    can run 'ndt list-jobs -e -j -b [current-branch]'
    The only mandatory parameter is CODEBUILD_SERVICE_ROLE, which defines the role that the codebuild project assumes
    for building.
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
    """
    parser = get_parser(formatter=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-d", "--dry-run", action="store_true",
                        help="Do not actually create or update projects, just print configuration")
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    upsert_codebuild_projects(dry_run=args.dry_run)

def upsert_dns_record():
    """ Update a dns record in Route53 """
    parser = get_parser()
    parser.add_argument("name", help="The name of the record to create")
    parser.add_argument("-t", "--type", help="The type of record to create. Defaults to 'A'", default="A")
    parser.add_argument("value", help="The value to put into the record")
    parser.add_argument("-l", "--ttl", help="Time To Live for the record. Defaults to 300", default=300, type=int)
    parser.add_argument("-n", "--no-wait", help="Do not wait for the record to be synced within Route53", action="store_false")
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    upsert_record(args.name, args.type, args.value, ttl=args.ttl, wait=args.no_wait)

def azure_ensure_group():
    """ Ensures that an azure resource group exists """
    parser = get_parser()
    parser.add_argument("-l", "--location", help="The location for the resource group. If not defined looked from the environment " + \
                                                 "variable AZURE_LOCATION and after that seen if location is defined for the project.")
    parser.add_argument("name", help="The name of the resource group to make sure exists")
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    if not args.location:
        args.location = resolve_location()
    ensure_group(args.location, args.name)

def azure_ensure_management_group():
    """ Ensures that an azure resource group exists """
    parser = get_parser()
    parser.add_argument("name", help="The name of the resource group to make sure exists")
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    ensure_management_group(args.name)

def azure_template_parameters():
    """ Lists the parameters in an Azure Resource Manager template """
    parser = get_parser()
    parser.add_argument("template", help="The json template to scan for parameters").competer = FilesCompleter()
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    template = json_load(open(args.template).read())
    if "parameters" in template and template["parameters"]:
        print(",".join(template["parameters"].keys()))

def azure_location():
    """ Resolve an azure location based on 'AZURE_LOCATION' enviroment variable, local project or az cli configuration. Defaults to 'northeurope' """
    parser = get_parser()
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    print(resolve_location())

def resolve_location():
    if "AZURE_LOCATION" in environ and environ["AZURE_LOCATION"] and environ["AZURE_LOCATION"] != "default":
        return environ["AZURE_LOCATION"]
    else:
        parameters = load_parameters()
        if "AZURE_LOCATION" in parameters and parameters["AZURE_LOCATION"] and parameters["AZURE_LOCATION"] != "default":
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
                    if "name" in conf and conf["name"] == "location" and \
                       "value" in conf and conf["value"]:
                        default_location = conf["value"]
            if default_location:
                return default_location
            else:
                return "northeurope"