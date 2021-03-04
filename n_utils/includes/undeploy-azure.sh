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
      compgen -W "$DRY-v -h $(get_stack_dirs)" -- $COMP_CUR
      ;;
    3)
      compgen -W "$(get_azure $COMP_PREV)" -- $COMP_CUR
      ;;
    *)
      exit 1
      ;;
  esac
  exit 0
fi

usage() {
  echo "usage: ndt deploy-azure [-d] [-h] component azure-name" >&2
  echo "" >&2
  echo "Exports ndt parameters into component/azure-name/variables.json" >&2
  echo "and deletes the deployment" >&2
  echo "" >&2
  echo "positional arguments:" >&2
  echo "  component   the component directory where the azure directory is" >&2
  echo "  azure-name  the name of the azure directory that has the template" >&2
  echo "                  For example for lambda/azure-blobstore/template.yaml" >&2
  echo "                  you would give blobstore" >&2
  echo "" >&2
  echo "optional arguments:" >&2
  echo "  -d, --dryrun  dry-run - do only parameter expansion and template pre-processing and azure cli what-if operation"  >&2
  echo "  -v, --verbose verbose - verbose output from azure cli"  >&2
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
while [ "$1" = "-d" -o "$1" = "--dryrun" -o "$1" = "-v" -o "$1" = "--verbose" ]; do
  if [ "$1" = "-d" -o "$1" = "--dryrun" ]; then
    DRYRUN=1
    shift
  elif [ "$1" = "-v" -o "$1" = "--verbose" ]; then
    VERBOSE="--debug"
    shift
  fi
done
die () {
  set +x
  echo "$1" >&2
  usage
}
set -xe

component="$1" ; shift
[ "${component}" ] || die "You must give the component name as argument"
azure="$1"; shift
[ "${azure}" ] || die "You must give the azure name as argument"

eval "$(ndt load-parameters "$component" -a "$azure" -e -r)"

[ "$AZURE_LOCATION" ] || die "You must define the Azure location to deploy to with parameter AZURE_LOCATION"

if [ "$AZURE_LOCATION" = "default" ]; then
  AZURE_LOCATION=$(ndt azure-location)
fi

[ "$DEPLOYMENT_NAME" ] || DEPLOYMENT_NAME="${BUILD_JOB_PREFIX}_${component}_${ORIG_AZURE_NAME}"
#If assume-azure-deploy-role.sh is on the path, run it to assume the appropriate role for deployment
if [ -n "$DEPLOY_AZURE_SUBSCRIPTION" ] && [ -z "$AZURE_SUBSCRIPTION" ]; then
  eval $(ndt assume-role -s $DEPLOY_AZURE_SUBSCRIPTION)
elif which assume-azure-deploy-role.sh &> /dev/null && [ -z "$AZURE_SUBSCRIPTION" -o "$AZURE_SUBSCRIPTION" != "$DEPLOY_AZURE_SUBSCRIPTION" ]; then
  eval $(assume-azure-deploy-role.sh)
fi

cd "$component/azure-$ORIG_AZURE_NAME"

if [ -x "./pre_undeploy.sh" ]; then
  "./pre_undeploy.sh"
fi

case "$AZURE_SCOPE" in
  group)
    SCOPE_COMMAND="group"
    GROUP_ARGS="--resource-group $AZURE_GROUP"
    ;;
  management-group)
    SCOPE_COMMAND="mg"
    GROUP_ARGS="--management-group-id $AZURE_MANAGEMENT_GROUP"
    ;;
  subscription)
    SCOPE_COMMAND="sub"
    ;;
  tenant)
    SCOPE_COMMAND="tenant"
    ;;
  *)
    echo "Unknown Azure deployment scope $AZURE_SCOPE"
    ;;
esac

set -e
az $VERBOSE deployment $SCOPE_COMMAND delete \
  --name $DEPLOYMENT_NAME $GROUP_ARGS

if [ -x "./post_undeploy.sh" ]; then
  "./post_undeploy.sh"
fi
