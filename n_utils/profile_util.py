import argparse
import os
import re
from datetime import datetime
from os import R_OK, access
from os.path import exists, expanduser, isfile, join

import argcomplete
from argcomplete.completers import ChoicesCompleter
from dateutil.parser import parse
from dateutil.tz import tzutc
from n_utils import _to_str

def ConfigParser():
    import configparser
    return configparser.ConfigParser()

def read_expiring_profiles():
    ret = []
    home = expanduser("~")
    credentials = join(home, ".aws", "credentials")
    if exists(credentials):
        parser = ConfigParser()
        with open(credentials) as credfile:
            parser.readfp(credfile)
            for profile in parser.sections():
                if parser.has_option(profile, "aws_session_expiration"):
                    ret.append(profile)
    return ret

def read_profiles():
    ret = []
    home = expanduser("~")
    credentials = join(home, ".aws", "credentials")
    if isfile(credentials) and access(credentials, R_OK):
        parser = ConfigParser()
        with open(credentials) as credfile:
            parser.readfp(credfile)
            for profile in parser.sections():
                ret.append(profile)
    config = join(home, ".aws", "config")
    if isfile(config) and access(config, R_OK):
        parser = ConfigParser()
        with open(config) as configfile:
            parser.readfp(configfile)
            for profile in parser.sections():
                if profile.startswith("profile ") and profile[8:] not in ret:
                    ret.append(profile[8:])
    return ret


def get_profile(profile):
    home = expanduser("~")
    from collections import OrderedDict
    ret = OrderedDict()
    config = join(home, ".aws", "config")
    profile_section = "profile " + profile
    if isfile(config) and access(config, R_OK):
        parser = ConfigParser()
        with open(config) as configfile:
            parser.readfp(configfile)
            if profile_section in parser.sections():
                for option in parser.options(profile_section):
                    ret[option] = parser.get(profile_section, option)
    credentials = join(home, ".aws", "credentials")
    if isfile(credentials) and access(credentials, R_OK):
        parser = ConfigParser()
        with open(credentials) as credfile:
            parser.readfp(credfile)
            if profile in parser.sections():
                for option in parser.options(profile):
                    ret[option] = parser.get(profile, option)
    return ret

def read_profile_expiry(profile):
    home = expanduser("~")
    credentials = join(home, ".aws", "credentials")
    if exists(credentials):
        parser = ConfigParser()
        with open(credentials) as credfile:
            parser.readfp(credfile)
            if parser.has_option(profile, "aws_session_expiration"):
                return parser.get(profile, "aws_session_expiration")
    return "1970-01-01T00:00:00.000Z"

def profile_to_env():
    """ Prints profile parameters from credentials file (~/.aws/credentials) as eval-able environment variables """
    parser = argparse.ArgumentParser(description=profile_to_env.__doc__)
    parser.add_argument("-t", "--target-role", action="store_true", help="Output also azure_default_role_arn")
    parser.add_argument("-r", "--role-arn", help="Output also the role given here as the target role for the profile")
    if "_ARGCOMPLETE" in os.environ:
        parser.add_argument("profile", help="The profile to read profile info from").completer = \
            ChoicesCompleter(read_profiles())
        argcomplete.autocomplete(parser)
    else:
        parser.add_argument("profile", help="The profile to read profile info from")
    args = parser.parse_args()
    safe_profile = re.sub("[^A-Z0-9]", "_", args.profile.upper())
    params = []
    role_param = "AWS_TARGET_ROLE_ARN_" + safe_profile
    if args.target_role:
        profile_entry = "profile " + args.profile
        home = expanduser("~")
        config = join(home, ".aws", "config")
        if exists(config):
            parser = ConfigParser()
            with open(config) as configfile:
                parser.readfp(configfile)
                if profile_entry in parser.sections() and parser.has_option(profile_entry, "azure_default_role_arn"):
                    params.append(role_param)
                    print(role_param + "=\"" + parser.get(profile_entry, "azure_default_role_arn") + "\"")
    if args.role_arn:
        params.append(role_param)
        print(role_param + "=\"" + args.role_arn + "\"")
    print_profile(args.profile, params)

def print_profile(profile_name, params):
    safe_profile = re.sub("[^A-Z0-9]", "_", profile_name.upper())
    profile = get_profile(profile_name)
    for key, value in list(profile.items()):
        upper_param = key.upper()
        if key == "aws_session_expiration":
            d = parse(value)
            print("AWS_SESSION_EXPIRATION_EPOC_" + safe_profile + "=\"" + _to_str(_epoc_secs(d)) + "\"")
            params.append("AWS_SESSION_EXPIRATION_EPOC_" + safe_profile)
        params.append(upper_param)
        if value.startswith("\""):
            value = value[1:-1]
        print(upper_param + "=\"" + value + "\"")
    print("export " + " ".join(params) + ";")

def profile_expiry_to_env():
    """ Prints profile expiry from credentials file (~/.aws/credentials) as eval-able environment variables """
    parser = argparse.ArgumentParser(description=profile_expiry_to_env.__doc__)
    if "_ARGCOMPLETE" in os.environ:
        parser.add_argument("profile", help="The profile to read expiry info from").completer = \
            ChoicesCompleter(read_expiring_profiles())
        argcomplete.autocomplete(parser)
    else:
        parser.add_argument("profile", help="The profile to read expiry info from")
    args = parser.parse_args()
    print_profile_expiry(args.profile)

def print_profile_expiry(profile):
    safe_profile = re.sub("[^A-Z0-9]", "_", profile.upper())
    expiry = read_profile_expiry(profile)
    epoc = _epoc_secs(parse(expiry).replace(tzinfo=tzutc()))
    print("AWS_SESSION_EXPIRATION_EPOC_" + safe_profile + "=" + _to_str(epoc))
    print("AWS_SESSION_EXPIRATION_" + safe_profile + "=" + expiry)
    print("export AWS_SESSION_EXPIRATION_" + safe_profile + " AWS_SESSION_EXPIRATION_EPOC_" + safe_profile + ";")

def cli_read_profile_expiry():
    """ Read expiry field from credentials file, which is there if the login happened
    with aws-azure-login or another tool that implements the same logic (none currently known)."""
    parser = argparse.ArgumentParser(description=cli_read_profile_expiry.__doc__)
    parser.add_argument("profile", help="The profile to read expiry info from").completer = \
        ChoicesCompleter(read_expiring_profiles())
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    print(read_profile_expiry(args.profile))

def update_profile(profile, creds):
    home = expanduser("~")
    credentials = join(home, ".aws", "credentials")
    if exists(credentials):
        parser = ConfigParser()
        with open(credentials, 'rb') as credfile:
            parser.readfp(credfile)
            if profile not in parser.sections():
                parser.add_section(profile)
            parser.set(profile, "aws_access_key_id", creds['AccessKeyId'])
            parser.set(profile, "aws_secret_access_key", creds['SecretAccessKey'])
            parser.set(profile, "aws_session_token", creds['SessionToken'])
            parser.set(profile, "aws_session_expiration", creds['Expiration'].strftime("%Y-%m-%dT%H:%M:%S.%fZ"))
    with open(credentials, 'wb') as credfile:
        parser.write(credfile)

def cli_enable_profile():
    """Enable a configured profile. Simple IAM user, AzureAD and ndt assume-role profiles are supported"""
    parser = argparse.ArgumentParser(description=cli_enable_profile.__doc__)
    type_select = parser.add_mutually_exclusive_group(required=False)
    type_select.add_argument("-i", "--iam", action="store_true", help="IAM user type profile")
    type_select.add_argument("-a", "--azure", action="store_true", help="Azure login type profile")
    type_select.add_argument("-n", "--ndt", action="store_true", help="NDT assume role type profile")
    if "_ARGCOMPLETE" in os.environ:
        parser.add_argument("profile", help="The profile to enable").completer = \
            ChoicesCompleter(read_profiles())
        argcomplete.autocomplete(parser)
    else:
        parser.add_argument("profile", help="The profile to enable")
    args = parser.parse_args()
    if args.iam:
        profile_type = "iam"
    elif args.azure:
        profile_type = "azure"
    elif args.ndt:
        profile_type = "ndt"
    else:
        profile = get_profile(args.profile)
        if "azure_tenant_id" in profile:
            profile_type = "azure"
        elif "ndt_role_arn" in profile:
            profile_type = "ndt"
        else:
            profile_type = "iam"
    enable_profile(profile_type, args.profile)

def enable_profile(profile_type, profile):
    profile = re.sub("[^a-zA-Z0-9_-]", "_", profile)
    safe_profile = re.sub("[^A-Z0-9]", "_", profile.upper())
    if profile_type == "iam":
        _print_profile_switch(profile)
    elif profile_type == "azure":
        _print_profile_switch(profile)
        if "AWS_SESSION_EXPIRATION_EPOC_" + safe_profile in os.environ:
            expiry = int(os.environ["AWS_SESSION_EXPIRATION_EPOC_" + safe_profile])
        else:
            expiry = _epoc_secs(parse(read_profile_expiry(profile)).replace(tzinfo=tzutc()))
        if expiry < _epoc_secs(datetime.now(tzutc())):
            if "AWS_SESSION_EXPIRATION_EPOC_" + safe_profile in os.environ:
                print("unset AWS_SESSION_EXPIRATION_EPOC_" + safe_profile + ";")
            print("aws-azure-login --profile " + profile + " --no-prompt")
        elif "AWS_SESSION_EXPIRATION_EPOC_" + safe_profile not in os.environ:
            print_profile_expiry(profile)
    elif profile_type == "ndt":
        if "AWS_SESSION_EXPIRATION_EPOC_" + safe_profile in os.environ:
            expiry = int(os.environ["AWS_SESSION_EXPIRATION_EPOC_" + safe_profile])
        else:
            expiry = _epoc_secs(parse(read_profile_expiry(profile)).replace(tzinfo=tzutc()))
        if expiry < _epoc_secs(datetime.now(tzutc())):
            if "AWS_SESSION_EXPIRATION_EPOC_" + safe_profile in os.environ:
                print("unset AWS_SESSION_EXPIRATION_EPOC_" + safe_profile + ";")
            profile_data = get_profile(profile)
            if "ndt_origin_profile" not in profile_data:
                return
            origin_profile = profile_data["ndt_origin_profile"]
            origin_profile_data = get_profile(origin_profile)
            if "azure_tenant_id" in origin_profile_data:
                origin_type = "azure"
            else:
                origin_type = "iam"
            enable_profile(origin_type, origin_profile)

            command = ["ndt", "assume-role"]
            if "ndt_mfa_token" in profile_data:
                command.append("-t")
                command.append(profile_data["ndt_mfa_token"])
            if "ndt_default_duration_hours" in profile_data:
                command.append("-d")
                duration = _to_str(int(profile_data["ndt_default_duration_hours"]) * 60)
                command.append(duration)
            command.append("-p")
            command.append(profile)
            command.append(profile_data["ndt_role_arn"])
            print(" ".join(command))
        elif "AWS_SESSION_EXPIRATION_EPOC_" + safe_profile not in os.environ:
            print_profile_expiry(profile)
        _print_profile_switch(profile)

def _print_profile_switch(profile):
    unset = []
    for env in ["AWS_SESSION_TOKEN", "AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"]:
        if env in os.environ:
            unset.append(env)
    if unset:
        print("unset " + " ".join(unset) + ";")
    set_env = []
    if "AWS_DEFAULT_PROFILE" not in os.environ or os.environ["AWS_DEFAULT_PROFILE"] != profile:
        set_env.append("AWS_DEFAULT_PROFILE")
    if "AWS_PROFILE" not in os.environ or os.environ["AWS_PROFILE"] != profile:
        set_env.append("AWS_PROFILE")
    if set_env:
        for param in set_env:
            print(param + "=\"" + profile + "\"")
        print("export " + " ".join(set_env) + ";")

def _epoc_secs(d):
    return int((d - datetime.utcfromtimestamp(0).replace(tzinfo=tzutc())).total_seconds())
