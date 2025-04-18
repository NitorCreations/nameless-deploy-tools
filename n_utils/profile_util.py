import argparse
import json
import os
import re

from datetime import datetime, timezone
from os import R_OK, access
from os.path import exists, expanduser, isdir, isfile, join

import argcomplete

from argcomplete.completers import ChoicesCompleter
from dateutil.parser import parse
from dateutil.parser._parser import ParserError
from dateutil.tz import tzutc
from threadlocal_aws.clients import sso

from n_utils.az_util import az_select_subscription
from n_utils.bw_util import get_bwentry
from n_utils.lp_util import get_lpentry
from n_utils.mfa_utils import mfa_generate_code


def ConfigParser():  # noqa: N802
    import configparser

    return configparser.ConfigParser()


def read_expiring_profiles():
    ret = []
    home = expanduser("~")
    credentials = join(home, ".aws", "credentials")
    if exists(credentials):
        parser = ConfigParser()
        with open(credentials) as credfile:
            parser.read_file(credfile)
            for profile in parser.sections():
                if parser.has_option(profile, "aws_session_expiration") or parser.has_option(profile, "aws_expiration"):
                    ret.append(profile)
    return ret


def read_profiles(prefix=""):
    """Return a list of all unique AWS profile names found from config."""
    ret = set()
    home = expanduser("~")
    credentials = join(home, ".aws", "credentials")
    if isfile(credentials) and access(credentials, R_OK):
        parser = ConfigParser()
        with open(credentials) as credfile:
            parser.read_file(credfile)
            for profile in parser.sections():
                if profile and profile.startswith(prefix):
                    ret.add(profile)

    config = join(home, ".aws", "config")
    if isfile(config) and access(config, R_OK):
        parser = ConfigParser()
        with open(config) as configfile:
            parser.read_file(configfile)
            for profile in parser.sections():
                if profile and profile.startswith("profile ") and profile[8:].startswith(prefix):
                    ret.add(profile[8:])

    return sorted(ret)


PROFILES = {}
PROFILES_WITH_CREDS = {}


def get_profile(profile, include_creds=True):
    home = expanduser("~")
    if include_creds and profile in PROFILES_WITH_CREDS:
        return PROFILES_WITH_CREDS[profile]
    elif not include_creds and profile in PROFILES:
        return PROFILES[profile]
    from collections import OrderedDict

    ret = OrderedDict()
    config = join(home, ".aws", "config")
    profile_section = "profile " + profile
    if isfile(config) and access(config, R_OK):
        parser = ConfigParser()
        with open(config) as configfile:
            parser.read_file(configfile)
            if profile_section in parser.sections():
                for option in parser.options(profile_section):
                    ret[option] = parser.get(profile_section, option)

    if include_creds:
        credentials = join(home, ".aws", "credentials")
        if isfile(credentials) and access(credentials, R_OK):
            parser = ConfigParser()
            with open(credentials) as credfile:
                parser.read_file(credfile)
                if profile in parser.sections():
                    for option in parser.options(profile):
                        ret[option] = parser.get(profile, option)

        PROFILES_WITH_CREDS[profile] = ret

    PROFILES[profile] = ret
    return ret


def read_profile_expiry(profile, profile_type=None):
    if profile_type != "sso":
        home = expanduser("~")
        credentials = join(home, ".aws", "credentials")
        if exists(credentials):
            parser = ConfigParser()
            with open(credentials) as credfile:
                parser.read_file(credfile)
                if parser.has_option(profile, "aws_expiration"):
                    return parse(parser.get(profile, "aws_expiration"))
                elif parser.has_option(profile, "aws_session_expiration"):
                    return parse(parser.get(profile, "aws_session_expiration"))
    return read_sso_profile_expiry(profile)


def read_sso_profile_expiry(profile):
    profile_data = read_sso_profile(profile)
    if profile_data:
        try:
            return parse(profile_data.get("expiresAt", "1970-01-01T00:00:00Z")[:-1] + ".000Z")
        except ParserError:
            return parse(profile_data.get("expiresAt", "1970-01-01T00:00:00.000Z"))
    return parse("1970-01-01T00:00:00.000Z")


def read_sso_profile(profile):
    profile_data = get_profile(profile, include_creds=False)
    if "sso_start_url" in profile_data:
        home = expanduser("~")
        sso_cache = join(home, ".aws", "sso", "cache")
        if isdir(sso_cache):
            for filename in os.listdir(sso_cache):
                full_file = os.path.join(sso_cache, filename)
                if isfile(full_file) and access(full_file, R_OK):
                    with open(full_file) as cache_file:
                        cache_json = json.load(cache_file)
                        if (
                            cache_json
                            and "startUrl" in cache_json
                            and cache_json["startUrl"] == profile_data["sso_start_url"]
                        ):
                            return cache_json
    return {}


def read_profile_expiry_epoc(profile, profile_type=None):
    return _epoc_secs(read_profile_expiry(profile, profile_type=profile_type).replace(tzinfo=tzutc()))


def check_profile_expired(profile, profile_type=None):
    return read_profile_expiry_epoc(profile, profile_type) < _epoc_secs(datetime.now(tzutc()))


def print_aws_profiles():
    """
    Prints profile names from the credentials file (~/.aws/credentials),
    and the config file (~/.aws/config) for autocomplete tools.
    """
    parser = argparse.ArgumentParser(description=print_aws_profiles.__doc__)
    if "_ARGCOMPLETE" in os.environ:
        parser.add_argument(
            "prefix", help="Prefix of profiles to print", default="", nargs="?"
        ).completer = ChoicesCompleter(read_profiles())
        argcomplete.autocomplete(parser)
    else:
        parser.add_argument("prefix", help="Prefix of profiles to print", default="", nargs="?")

    args = parser.parse_args()
    print(" ".join(read_profiles(prefix=args.prefix)))


def profile_to_env():
    """Prints profile parameters from credentials file (~/.aws/credentials) as eval-able environment variables"""
    parser = argparse.ArgumentParser(description=profile_to_env.__doc__)
    parser.add_argument(
        "-t",
        "--target-role",
        action="store_true",
        help="Output also azure_default_role_arn",
    )
    parser.add_argument(
        "-r",
        "--role-arn",
        help="Output also the role given here as the target role for the profile",
    )
    if "_ARGCOMPLETE" in os.environ:
        parser.add_argument("profile", help="The profile to read profile info from").completer = ChoicesCompleter(
            read_profiles()
        )
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
                parser.read_file(configfile)
                if profile_entry in parser.sections() and parser.has_option(profile_entry, "azure_default_role_arn"):
                    params.append(role_param)
                    print(role_param + '="' + parser.get(profile_entry, "azure_default_role_arn") + '";')
                if profile_entry in parser.sections() and parser.has_option(profile_entry, "adfs_role_arn"):
                    params.append(role_param)
                    print(role_param + '="' + parser.get(profile_entry, "adfs_role_arn") + '";')
                if profile_entry in parser.sections() and parser.has_option(profile_entry, "lastpass_role_arn"):
                    params.append(role_param)
                    print(role_param + '="' + parser.get(profile_entry, "lastpass_role_arn") + '";')
    if args.role_arn:
        params.append(role_param)
        print(role_param + '="' + args.role_arn + '";')
    print_profile(args.profile, params)


def print_profile(profile_name, params):
    safe_profile = re.sub("[^A-Z0-9]", "_", profile_name.upper())
    profile = get_profile(profile_name)
    for key, value in list(profile.items()):
        upper_param = key.upper()
        if key == "aws_session_expiration" or key == "aws_expiration":
            d = parse(value)
            print("AWS_SESSION_EXPIRATION_EPOC_" + safe_profile + '="' + str(_epoc_secs(d)) + '";')
            params.append("AWS_SESSION_EXPIRATION_EPOC_" + safe_profile)
        params.append(upper_param)
        if value.startswith('"'):
            value = value[1:-1]
        print(upper_param + '="' + value + '";')
    print("export " + " ".join(params) + ";")


def profile_expiry_to_env():
    """
    Prints profile expiry from credentials file (~/.aws/credentials) as eval-able environment variables.
    """
    parser = argparse.ArgumentParser(description=profile_expiry_to_env.__doc__)
    if "_ARGCOMPLETE" in os.environ:
        parser.add_argument("profile", help="The profile to read expiry info from").completer = ChoicesCompleter(
            read_expiring_profiles()
        )
        argcomplete.autocomplete(parser)
    else:
        parser.add_argument("profile", help="The profile to read expiry info from")
    args = parser.parse_args()
    print_profile_expiry(args.profile)


def print_profile_expiry(profile, expiry_epoc=None):
    safe_profile = re.sub("[^A-Z0-9]", "_", profile.upper())
    if expiry_epoc:
        epoc = expiry_epoc
        expiry = _epoc_to_datetime(epoc)
    else:
        expiry = read_profile_expiry(profile)
        epoc = _epoc_secs(expiry.replace(tzinfo=tzutc()))
    print("AWS_SESSION_EXPIRATION_EPOC_" + safe_profile + "=" + str(epoc))
    print("AWS_SESSION_EXPIRATION_" + safe_profile + "=" + expiry.strftime("%Y-%m-%dT%H:%M:%S.%fZ"))
    print("export AWS_SESSION_EXPIRATION_" + safe_profile + " AWS_SESSION_EXPIRATION_EPOC_" + safe_profile + ";")


def cli_read_profile_expiry():
    """
    Read expiry field from credentials file,
    which is there if the login happened with aws-azure-login or another tool that implements the same logic
    (e.g. https://github.com/NitorCreations/adfs-aws-login).
    """
    parser = argparse.ArgumentParser(description=cli_read_profile_expiry.__doc__)
    parser.add_argument("profile", help="The profile to read expiry info from").completer = ChoicesCompleter(
        read_expiring_profiles()
    )
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    print(read_profile_expiry(args.profile).isoformat())


def cli_update_sso_profile():
    """
    Update current SSO-profile's session to ~/.aws/credentials.
    Running this enables SSO-support for the Serverless Framework.
    """
    parser = argparse.ArgumentParser(description=cli_update_sso_profile.__doc__)
    argcomplete.autocomplete(parser)
    _ = parser.parse_args()
    if "AWS_PROFILE" not in os.environ:
        return
    profile_name = os.environ["AWS_PROFILE"]
    profile = get_profile(profile_name)
    profile_type = resolve_profile_type(profile_name)
    if check_profile_expired(profile=profile_name, profile_type=profile_type):
        return
    if profile_type == "sso":
        cache_json = read_sso_profile(profile_name)
        if "accessToken" in cache_json and cache_json["accessToken"]:
            access_token = cache_json["accessToken"]
            creds = sso(region=profile["sso_region"]).get_role_credentials(
                roleName=profile["sso_role_name"], accountId=profile["sso_account_id"], accessToken=access_token
            )
            role_creds = creds["roleCredentials"]
            update_profile(profile_name, role_creds)


def update_profile(profile, creds):
    home = expanduser("~")
    credentials = join(home, ".aws", "credentials")
    profile_type = resolve_profile_type(profile)
    parser = ConfigParser()
    if not exists(credentials):
        with open(credentials, "w"):
            pass
    with open(credentials) as credfile:
        parser.read_file(credfile)
        if profile not in parser.sections():
            parser.add_section(profile)
        if profile_type == "sso":
            creds["AccessKeyId"] = creds["accessKeyId"]
            creds["SecretAccessKey"] = creds["secretAccessKey"]
            creds["SessionToken"] = creds["sessionToken"]
            creds["Expiration"] = datetime.fromtimestamp(creds["expiration"] / 1000)
        parser.set(profile, "aws_access_key_id", creds["AccessKeyId"])
        parser.set(profile, "aws_secret_access_key", creds["SecretAccessKey"])
        parser.set(profile, "aws_session_token", creds["SessionToken"])
        parser.set(
            profile,
            "aws_session_expiration",
            creds["Expiration"].strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        )
        parser.set(
            profile,
            "aws_expiration",
            creds["Expiration"].strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        )
    with open(credentials, "w") as credfile:
        parser.write(credfile)


def cli_profiles_to_json():
    """Prints aws config file contents as json for further parsing and use in other tools."""
    parser = argparse.ArgumentParser(description=cli_profiles_to_json.__doc__)
    argcomplete.autocomplete(parser)
    _ = parser.parse_args()
    profiles_to_json()


def profiles_to_json():
    from collections import OrderedDict

    home = expanduser("~")
    config = join(home, ".aws", "config")
    ret = OrderedDict()
    if exists(config):
        parser = ConfigParser()
        with open(config) as conffile:
            parser.read_file(conffile)
            for section in parser.sections():
                if section.startswith("profile "):
                    section_data = OrderedDict()
                    ret[section[8:]] = section_data
                    for option in parser.options(section):
                        section_data[option] = parser.get(section, option)
        print(json.dumps(ret, indent=2))


def update_profile_conf(profile, creds):
    home = expanduser("~")
    config = join(home, ".aws", "config")
    profile_section = "profile " + profile
    if exists(config):
        parser = ConfigParser()
        with open(config) as conffile:
            parser.read_file(conffile)
            if profile_section in parser.sections():
                parser.remove_section(profile_section)
            parser.add_section(profile_section)
            for key in creds:
                parser.set(profile_section, key, creds[key])
    with open(config, "w") as conffile:
        parser.write(conffile)
    return


def store_bw_profile(bw_entry_name):
    bw_entry = get_bwentry(bw_entry_name)
    if (
        bw_entry
        and "aws_access_key_id" in bw_entry.fields
        and "aws_secret_access_key" in bw_entry.fields
        and "profile_name" in bw_entry.fields
    ):
        profile = bw_entry.fields["profile_name"]
        home = expanduser("~")
        credentials = join(home, ".aws", "credentials")
        if exists(credentials):
            parser = ConfigParser()
            with open(credentials) as credfile:
                parser.read_file(credfile)
                if profile not in parser.sections():
                    parser.add_section(profile)
                parser.set(profile, "aws_access_key_id", bw_entry.fields["aws_access_key_id"])
                parser.set(
                    profile,
                    "aws_secret_access_key",
                    bw_entry.fields["aws_secret_access_key"],
                )
        with open(credentials, "w") as credfile:
            parser.write(credfile)
        return profile
    return None


def cli_store_bw_profile():
    """Fetches a Bitwarden entry and if it contains a definition of a aws credentials, stores it in aws cli
    configuration. Namely the entry needs to define the extra fields aws_access_key_id, aws_secret_access_key
    and profile_name"""
    parser = argparse.ArgumentParser(description=cli_store_bw_profile.__doc__)
    parser.add_argument("entryname", help="The name of the bitwarden entry to get")
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    profile = store_bw_profile(args.entryname)
    if profile:
        print("Saved profile " + profile)
    else:
        print("Entry " + args.entryname + " not found to contain an aws cli profile")


def cli_enable_profile():
    """
    Enable a configured profile.

    Simple IAM user, AzureAD, ADFS and ndt assume-role profiles are supported.
    """
    parser = argparse.ArgumentParser(description=cli_enable_profile.__doc__)
    type_select = parser.add_mutually_exclusive_group(required=False)
    type_select.add_argument("-i", "--iam", action="store_true", help="IAM user type profile")
    type_select.add_argument("-a", "--azure", action="store_true", help="Azure login type profile")
    type_select.add_argument("-f", "--adfs", action="store_true", help="ADFS login type profile")
    type_select.add_argument("-l", "--lastpass", action="store_true", help="Lastpass login type profile")
    type_select.add_argument("-n", "--ndt", action="store_true", help="NDT assume role type profile")
    type_select.add_argument(
        "-s",
        "--azure-subscription",
        action="store_true",
        help="Microsoft Azure subscription",
    )
    type_select.add_argument("-o", "--sso", action="store_true", help="AWS SSO type profile")
    if "_ARGCOMPLETE" in os.environ:
        parser.add_argument("profile", help="The profile to enable").completer = ChoicesCompleter(read_profiles())
        argcomplete.autocomplete(parser)
    else:
        parser.add_argument("profile", help="The profile to enable")

    args = parser.parse_args()
    if args.iam:
        profile_type = "iam"
    elif args.azure:
        profile_type = "azure"
    elif args.adfs:
        profile_type = "adfs"
    elif args.lastpass:
        profile_type = "lastpass"
    elif args.ndt:
        profile_type = "ndt"
    elif args.azure_subscription:
        profile_type = "azure-subscription"
    elif args.sso:
        profile_type = "sso"
    else:
        profile_type = resolve_profile_type(args.profile)

    enable_profile(profile_type, args.profile)


def resolve_profile_type(profile_name):
    profile = get_profile(profile_name)
    if "azure_tenant_id" in profile:
        profile_type = "azure"
    elif "ndt_role_arn" in profile:
        profile_type = "ndt"
    elif "adfs_login_url" in profile:
        profile_type = "adfs"
    elif "lastpass_saml_id" in profile:
        profile_type = "lastpass"
    elif "sso_start_url" in profile:
        profile_type = "sso"
    else:
        profile_type = "iam"
    return profile_type


def enable_profile(profile_type, profile):
    orig_profile = profile
    profile = re.sub("[^a-zA-Z0-9_-]", "_", profile)
    safe_profile = re.sub("[^A-Z0-9]", "_", profile.upper())
    profile_expired = check_profile_expired(profile, profile_type=profile_type)
    if profile_type == "iam":
        _print_profile_switch(profile)
    elif profile_type == "azure" or profile_type == "adfs" or profile_type == "lastpass" or profile_type == "sso":
        _print_profile_switch(profile)
        if profile_expired:
            expiry = read_profile_expiry_epoc(profile, profile_type=profile_type)
            if "AWS_SESSION_EXPIRATION_EPOC_" + safe_profile in os.environ:
                del os.environ["AWS_SESSION_EXPIRATION_EPOC_" + safe_profile]
        if profile_expired:
            bw_prefix = ""
            bw_entry = None
            lp_entry = None
            profile_data = get_profile(profile)
            if "bitwarden_entry" in profile_data and profile_data["bitwarden_entry"]:
                bw_entry = get_bwentry(profile_data["bitwarden_entry"])
            if "lastpass_entry" in profile_data and profile_data["lastpass_entry"]:
                lp_entry = get_lpentry(profile_data["lastpass_entry"])
            if "AWS_SESSION_EXPIRATION_EPOC_" + safe_profile in os.environ:
                print("unset AWS_SESSION_EXPIRATION_EPOC_" + safe_profile + ";")
            if profile_type == "azure":
                gui_mode = ""
                if "azure_login_mode" in profile_data:
                    gui_mode = " --mode=" + profile_data["azure_login_mode"]
                if bw_entry:
                    bw_prefix = "AZURE_DEFAULT_PASSWORD='" + bw_entry.password + "' "
                elif lp_entry:
                    bw_prefix = "AZURE_DEFAULT_PASSWORD='" + lp_entry.password + "' "
                print(bw_prefix + "npx aws-azure-login --profile " + profile + gui_mode + " --no-prompt --no-sandbox")
            elif profile_type == "adfs":
                if bw_entry:
                    bw_prefix = "ADFS_DEFAULT_PASSWORD='" + bw_entry.password + "' "
                elif lp_entry:
                    bw_prefix = "ADFS_DEFAULT_PASSWORD='" + lp_entry.password + "' "
                print(bw_prefix + "adfs-aws-login --profile " + profile + " --no-prompt")
            elif profile_type == "lastpass":
                if bw_entry:
                    bw_prefix = "LASTPASS_DEFAULT_PASSWORD='" + bw_entry.password + "' "
                    if bw_entry.totp_now:
                        bw_prefix += "LASTPASS_DEFAULT_OTP='" + bw_entry.totp_now + "' "
                elif lp_entry:
                    bw_prefix = "LASTPASS_DEFAULT_PASSWORD='" + lp_entry.password + "' "
                if "ndt_mfa_token" in profile_data:
                    bw_prefix += "LASTPASS_DEFAULT_OTP='" + mfa_generate_code(profile_data["ndt_mfa_token"]) + "' "
                print(bw_prefix + "lastpass-aws-login --profile " + profile + " --no-prompt")
            elif profile_type == "sso":
                command = "aws sso login --profile"
                if "NDT_AWS_SSO_COMMAND" in os.environ:
                    command = os.environ["NDT_AWS_SSO_COMMAND"]
                print(f"{command} {profile};")
                print('eval "$(ndt update-sso-profile)"')
        elif "AWS_SESSION_EXPIRATION_EPOC_" + safe_profile not in os.environ:
            expiry = read_profile_expiry_epoc(profile, profile_type=profile_type)
            print_profile_expiry(profile, expiry_epoc=expiry)
    elif profile_type == "ndt":
        if "AWS_SESSION_EXPIRATION_EPOC_" + safe_profile in os.environ:
            expiry = int(os.environ["AWS_SESSION_EXPIRATION_EPOC_" + safe_profile])
        if profile_expired:
            expiry = read_profile_expiry_epoc(profile)
        if profile_expired:
            if "AWS_SESSION_EXPIRATION_EPOC_" + safe_profile in os.environ:
                print("unset AWS_SESSION_EXPIRATION_EPOC_" + safe_profile + ";")
            profile_data = get_profile(profile)
            if "ndt_origin_profile" not in profile_data:
                return

            origin_profile = profile_data["ndt_origin_profile"]
            origin_profile_data = get_profile(origin_profile)
            if "azure_tenant_id" in origin_profile_data:
                origin_type = "azure"
            elif "adfs_login_url" in origin_profile_data:
                origin_type = "adfs"
            elif "lastpass_saml_id" in origin_profile_data:
                origin_type = "lastpass"
            else:
                origin_type = "iam"

            enable_profile(origin_type, origin_profile)

            command = ["ndt", "assume-role"]
            if "ndt_mfa_token" in profile_data:
                command.append("-t")
                command.append(profile_data["ndt_mfa_token"])
            if "ndt_default_duration_hours" in profile_data:
                command.append("-d")
                duration = str(int(profile_data["ndt_default_duration_hours"]) * 60)
                command.append(duration)

            command.append("-p")
            command.append(profile)
            command.append(profile_data["ndt_role_arn"])
            print(" ".join(command))
        elif "AWS_SESSION_EXPIRATION_EPOC_" + safe_profile not in os.environ:
            expiry = read_profile_expiry_epoc(profile, profile_type=profile_type)
            print_profile_expiry(profile, expiry_epoc=expiry)
        _print_profile_switch(profile)
    elif profile_type == "azure-subscription":
        if not ("AZURE_SUBSCRIPTION" in os.environ and os.environ["AZURE_SUBSCRIPTION"] == orig_profile):
            subscription_id = az_select_subscription(orig_profile)
            if subscription_id:
                print('AZURE_SUBSCRIPTION="' + orig_profile + '";')
                print('AZURE_SUBSCRIPTION_ID="' + subscription_id + '";')
                print("export AZURE_SUBSCRIPTION AZURE_SUBSCRIPTION_ID")


def _print_profile_switch(profile):
    unset = []
    profile_type = resolve_profile_type(profile_name=profile)
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
            print(param + '="' + profile + '";')
        print("export " + " ".join(set_env) + ";")
        if profile_type == "sso":
            print('eval "$(ndt update-sso-profile)"')


def _epoc_to_str(epoc):
    return _epoc_to_datetime(epoc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def _epoc_to_datetime(epoc):
    return datetime.fromtimestamp(epoc, timezone.utc)


def _epoc_secs(d):
    return int((d - datetime.fromtimestamp(0, timezone.utc).replace(tzinfo=tzutc())).total_seconds())
