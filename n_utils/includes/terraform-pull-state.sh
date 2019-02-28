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
      compgen -W "-h $(get_stack_dirs)" -- $COMP_CUR
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
  echo "usage: ndt terraform-init-state [-h] component terraform-name" >&2
  echo "" >&2
  echo "Make sure terraform state is initialized either for backend or locally" >&2
  echo "" >&2
  echo "positional arguments:" >&2
  echo "  component   the component directory where the terraform directory is" >&2
  echo "  terraform-name the name of the terraform directory that has the template" >&2
  echo "                  For example for lambda/terraform-sender/template.yaml" >&2
  echo "                  you would give sender" >&2
  echo "" >&2
  echo "optional arguments:" >&2
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
die () {
  echo "$1" >&4
  usage
}
onexit() {
    EXIT_VAL=$?
    if [ "$EXIT_VAL" != "0" ]; then
        cat $TF_INIT_OUTPUT >&4
    fi
    rm -f $OUTPUT
    exit "$EXIT_VAL"
}
export TF_INIT_OUTPUT="$(mktemp)"
exec 3>&1 4>&2 >$TF_INIT_OUTPUT 2>&1
trap onexit EXIT
set -xe

component="$1" ; shift
[ "${component}" ] || die "You must give the component name as argument"
terraform="$1"; shift
[ "${terraform}" ] || die "You must give the terraform name as argument"

eval "$(ndt load-parameters "$component" -t "$terraform" -e -r)"

#If assume-deploy-role.sh is on the path, run it to assume the appropriate role for deployment
if [ -n "$DEPLOY_ROLE_ARN" ] && [ -z "$AWS_SESSION_TOKEN" ]; then
  eval $(ndt assume-role $DEPLOY_ROLE_ARN)
elif which assume-deploy-role.sh > /dev/null && [ -z "$AWS_SESSION_TOKEN" ]; then
  eval $(assume-deploy-role.sh)
elif [ -n "$AWS_PROFILE" ]; then
  eval "$(ndt profile-to-env $AWS_PROFILE)"
fi

COMPONENT_DIR="$component/terraform-$ORIG_TERRAFORM_NAME"

if [ "$SKIP_TF_BACKEND" != "y" ] && [ -r "$TF_BACKEND_CONF" ]; then
  ndt interpolate-file -n -k "$TF_BACKEND_CONF" -o "$COMPONENT_DIR/backend.tf"
fi

cd $COMPONENT_DIR

if ! terraform init; then
  rm -rf .terraform
  terraform init
fi

set +x
#Restore output
exec 1>&3 2>&4

terraform state pull