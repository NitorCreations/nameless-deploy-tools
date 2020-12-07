# Workspace
## Command completion

Most things have decent bash command completion, even for things like AMI Ids in AWS. To make it work, the things
outputted by `nameless-dt-register-complete` need to be in your environment. So put the following somewhere
(e.g. your ~/.bashrc) where it gets run for your profile (or run it manually when working with ndt)

```bash
eval "$(nameless-dt-register-complete)"
```

## Command completion on Macs

The default shell on Macs is `zsh` nowadays and that can be made to work via a compatibility trick described here:
https://stackoverflow.com/questions/3249432/can-a-bash-tab-completion-script-be-used-in-zsh

In short you need to append the following to `~/.zshrc`
```shell
autoload -U +X compinit && compinit
autoload -U +X bashcompinit && bashcompinit
eval "$(nitor-care-register-complete)"

## Project session switcher

Optionally you can add the argument `--project-env` to add a `PROMPT_COMMAND` hook for bash to check git
local variables to export a useful project environmnet that usually points to AWS credentials profile.
This could also be a script that does third a party login including some custom MFA. The script
is run for every prompt though inside the project so you will want to make it check if the session is still
valid before trying to assume the role. You can use then environment variable `AWS_SESSION_EXPIRATION` that
is set by `ndt assume-role` to only assume role when the previous role has expired. See documentation about
(TOTP MFA)[mfa.md] codes. An example of what a sourceable role script could be is below:

```bash
#!/bin/bash

# Reset variables potentially set by other projects
unset AWS_PROFILE AWS_DEFAULT_PROFILE
export AWS_DEFAULT_REGION=eu-central-1

ADMIN_ROLE="arn:aws:iam::432486532345:role/my-admin-role"
# Check that the current role matches the one we want
if [ "$AWS_ROLE_ARN" != "$ADMIN_ROLE" ]; then
  unset AWS_SESSION_EXPIRATION
fi
EXP_DATE=$(date +%s -d "$AWS_SESSION_EXPIRATION")
NOW=$(date +%s)
#Check that the session is still valid
if [ $NOW -lt $EXP_DATE  ]; then
  exit 0
fi
# Set the credentials that have access to the role
export AWS_PROFILE=myprofile AWS_DEFAULT_PROFILE=myprofile
# Reset wrong or expired variables
unset AWS_SESSION_TOKEN AWS_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY AWS_SESSION_EXPIRATION AWS_ROLE_ARN
eval $(ndt assume-role -t mytoken "$ADMIN_ROLE")
# Reset profile to make the assumed role take over
unset AWS_PROFILE AWS_DEFAULT_PROFILE
```

So taking project environment variables into use with your command completion would require setting

```bash
eval "$(nameless-dt-register-complete --project-env)"
```

Somewehere in your bash profile files - I have mine in `~/.bashrc`

The checked git local configurations are:
* `ndt.source.env` - source a file on every prompt
* `ndt.aws.profile` - export the name of an aws credentials profile on every prompt
* `ndt.aws.region` - export a default region name on every prompt
* `ndt.profile.azure` - enable a profile that includes `aws-azure-login` settings
* `ndt.profile.iam` - enable a profile that has simple iam keys settings
* `ndt.profile.ndt` - enable a profile that has settings to do a `ndt assume-role` including a potential mfa token.
* `ndt.profile.adfs` - enable a profile that includes `adfs-aws-login` settings

You can set these variables by calling `git config [variable] [value]` and you can check the commands
that would be executed by calling `nameless-dt-load-project-env`

So to complete the script example from above, you would put the script somewhere handy to execute -
say `~/bin/my-admin-role` if you have that on your `PATH`. Then you would just set that to be
sourced in your ndt project by calling `git config ndt.source.env my-admin-role` in your project
that needs that role and assuming you've set up command completion as above, every time you
change directory into the project, your credentials get set up automatically for you to work and
checked every time you give a command.

The simplest way to set up your working environment is to use a profile in `~/.aws/config` and
set either `ndt.profile.azure`, `ndt.profile.iam` or `ndt.profile.ndt`. Examples of these
profiles are below. That will run `nameless-dt-enable-profile` for every prompt command and that in
turn checks session validity from environment variables and doesn't actually execute anything
else if you have a valid session defined. You can also chain for example an azure profile and
and assume role if that is how multi-account access is setup for you.

`nameless-dt-register-complete` uses `nameless-dt-load-project-env` as a prompt command that is run
every time the shell prompt is created. By default that will be a python script and will have
the usual python startup slowness attached. On some systems you can work around this by compiling
that command into a native binary with [nuitka](http://nuitka.net/). The process of replacing
that python script with a binary version is as follows: 

```bash
sudo -H pip install -U nuitka
ENV_SCRIPT="$(dirname $(dirname $(n-include hook.sh)))/nameless-dt-load-project-env.py"
python -m nuitka --recurse-to=n_utils.project_util $ENV_SCRIPT
sudo cp nameless-dt-load-project-env.exe $(which nameless-dt-load-project-env)
```

Doing this on a machine that has the right tooling will give you a much snappier prompt.

## Project session profile types

The following details the kinds of profiles that enable project sessions to work.

### `aws-azure-login` profile

These types of profiles are configured to take advantage of Microsoft Azure Active Directory
SAML integration with AWS IAM. You can set this integration up by following the instructions
written for example here: https://docs.microsoft.com/en-us/azure/active-directory/saas-apps/aws-multi-accounts-tutorial

For every cli login role, you will have to set up a profile in `~/.aws/config` that looks similar
to this:

```ini
[profile infra]
# Default region - can be overridden with environment variables
region=eu-west-1
# The id of the organization in azure id
azure_tenant_id=aaaaaaaa-bbbb-cccc-dddd-eeeeffffgggg
# One of the identifierUris in the application registration manifest
azure_app_id_uri=urn:aws:infra
# The username to log in with
azure_default_username=your.username@example.com
# The role to assume in the target AWS account
azure_default_role_arn=arn:aws:iam::1234567890:role/AADMyAccountAdmin
# The default expiration time for the assumed role session
azure_default_duration_hours=12
```

To use these roles you will have to have [aws-azure-login](https://www.npmjs.com/package/aws-azure-login)
installed.

### ndt profile

This profile is meant to automate enabling a profile that assumes a role
with a previous profile enable for the assume role to be possible. The chained
profile may be a iam user profile or a `aws-azure-login` profile.

The configuration for this role looks something like this:

```ini
[profile my_role]
# Default region - can be overridden with environment variables
region=eu-west-1
# The chained profile that is enabled as a part of the process of assuming this role
ndt_origin_profile=infra
# The role to be assumend
ndt_role_arn=arn:aws:iam::1234567890:role/MyTargetRole
# The mfa token required for assuming the role. See mfa document
ndt_mfa_token=my_token
# The default expiration time for the assumed role session
ndt_default_duration_hours=1
```

The main benefit of this profile as compared with standard aws profiles is that
enabling this profile automatically renew expired profile sessions and records
the expiry of each. You may for example have 12 hour azure - aws iam sessions, but
have the actual used sessions renew every hour with very little impact on work if
the above project env is enabled.

### iam profile

Iam profiles are standard iam user key id and secret key settings and documented
with the aws cli tool.
