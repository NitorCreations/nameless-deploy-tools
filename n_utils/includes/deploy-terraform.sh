#!/bin/bash

# Copyright 2016 Nitor Creations Oy
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

if [ "$_ARGCOMPLETE" ]; then
  # Handle command completion executions
  unset _ARGCOMPLETE
  source $(n-include autocomplete-helpers.sh)
  case $COMP_CWORD in
    2)
      if [ "$COMP_INDEX" = "$COMP_CWORD" ]; then
        DRY="-d "
      fi
      compgen -W "$DRY-h $(get_stack_dirs)" -- $COMP_CUR
      ;;
    3)
      compgen -W "$(get_terraform $COMP_PREV)" -- $COMP_CUR
      ;;
    *)
      exit 1
      ;;
  esac
  exit 0
fi

usage() {
  echo "usage: ndt deploy-terraform [-d] [-h] component terraform-name" >&2
  echo "" >&2
  echo "Exports ndt parameters into component/terraform-name/terraform.tfvars as json, runs pre_deploy.sh in the" >&2
  echo "terraform project and runs terraform plan; terraform apply for the same" >&2
  echo "If TF_BACKEND_CONF is defined and points to a readable file relative to the ndt root," >&2
  echo "that file will get interpolated to \$component/terraform-\$terraform_name/backend.tf" >&2
  echo "If pre_deploy.sh and post_deploy.sh exist and are executable in the subcompoent directory," >&2
  echo "they will be executed before and after the deployment, respectively." >&2
  echo "" >&2
  echo "positional arguments:" >&2
  echo "  component   the component directory where the terraform directory is" >&2
  echo "  terraform-name the name of the terraform directory that has the template" >&2
  echo "                  For example for lambda/terraform-sender/main.tf" >&2
  echo "                  you would give sender" >&2
  echo "" >&2
  echo "optional arguments:" >&2
  echo "  -d, --dryrun  dry-run - do only parameter expansion and template pre-processing and npm i"  >&2
  echo "  -h, --help    show this help message and exit"  >&2
  if "$@"; then
    echo "" >&2
    echo "$@" >&2
  fi
  exit 1
}
if [ "$1" = "--help" -o "$1" = "-h" ]; then
  usage
fi
if [ "$1" = "-d" -o "$1" = "--dryrun" ]; then
  DRYRUN=1
  shift
fi
die () {
  echo "$1" >&2
  usage
}
set -xe

component="$1" ; shift
[ "${component}" ] || die "You must give the component name as argument"
terraform="$1"; shift
[ "${terraform}" ] || die "You must give the terraform name as argument"

TSTAMP=$(date +%Y%m%d%H%M%S)
if [ -z "$BUILD_NUMBER" ]; then
  BUILD_NUMBER=$TSTAMP
else
  BUILD_NUMBER=$(printf "%04d\n" $BUILD_NUMBER)
fi

eval "$(ndt load-parameters "$component" -t "$terraform" -e -r)"

#If assume-deploy-role.sh is on the path, run it to assume the appropriate role for deployment
if [ -n "$DEPLOY_ROLE_ARN" ] && [ -z "$AWS_SESSION_TOKEN" ]; then
  eval $(ndt assume-role $DEPLOY_ROLE_ARN)
elif which assume-deploy-role.sh &> /dev/null && [ -z "$AWS_SESSION_TOKEN" ]; then
  eval $(assume-deploy-role.sh)
elif [ -n "$AWS_PROFILE" ]; then
  eval "$(ndt profile-to-env $AWS_PROFILE)"
fi

COMPONENT_DIR="$component/terraform-$ORIG_TERRAFORM_NAME"
ndt load-parameters "$component" -t "$terraform" -v > "$COMPONENT_DIR/terraform.tfvars"

if [ "$SKIP_TF_BACKEND" != "y" ] && [ -r "$TF_BACKEND_CONF" ]; then
  ndt interpolate-file -n -k "$TF_BACKEND_CONF" -o "$COMPONENT_DIR/backend.tf"
fi

cd "$component/terraform-$ORIG_TERRAFORM_NAME"

if [ -x "./pre_deploy.sh" ]; then
  "./pre_deploy.sh"
fi

if ! terraform init; then
  rm -rf .terraform
  terraform init
fi

terraform plan

if [ -n "$DRYRUN" ]; then
  exit 0
fi

set -e
terraform apply -auto-approve

if [ -x "./post_deploy.sh" ]; then
  "./post_deploy.sh"
fi
