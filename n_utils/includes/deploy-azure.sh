#!/bin/bash

# Copyright 2016-2024 Nitor Creations Oy
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
  COMP_WORDS=( $COMP_LINE )

  DRY="-d --dry-run "
  HELP="-h --help "
  STACK_DIRS="$(get_stack_dirs) "
  FOUND_STACK_DIR=""
  for i in "${!COMP_WORDS[@]}"; do
    if [ "$i" -lt 2 ]; then
      continue
    fi
    word="${COMP_WORDS[$i]}"
    if [ "$word" = "-d" -o "$word" = "--dry-run" ]; then
      DRY=""
    elif [ "$word" = "-h" -o "$word" = "--help" ]; then
      HELP=""
    elif [ -z "$FOUND_STACK_DIR" ]; then
      if [ -d "$word" ]; then
        FOUND_STACK_DIR="$word"
        STACK_DIRS=""
        SUBMODULES="$(get_azure $FOUND_STACK_DIR)"
      fi
    else
      SUBMODULES="$(get_azure $FOUND_STACK_DIR)"
    fi
  done
  compgen -W "${DRY}${HELP}${STACK_DIRS}${SUBMODULES}" -- $COMP_CUR
  exit 0
fi

usage() {
  echo "usage: ndt deploy-azure [-d] [-h] component azure-name" >&2
  echo "" >&2
  echo "Exports ndt parameters into component/azure-name/variables.json" >&2
  echo "and deploys template.yaml or template.bicep with the azure cli referencing the parameter file" >&2
  echo "If pre_deploy.sh and post_deploy.sh exist and are executable in the subcompoent directory," >&2
  echo "they will be executed before and after the deployment, respectively." >&2
  echo "Similarly, if a readable pre_deploy_source.sh exists in the subcompoent directory," >&2
  echo "it will be sourced before the deployment to enable things like activating a python venv." >&2
  echo "" >&2
  echo "positional arguments:" >&2
  echo "  component   the component directory where the azure directory is" >&2
  echo "  azure-name  the name of the azure directory that has the template" >&2
  echo "                  For example for lambda/azure-blobstore/template.yaml" >&2
  echo "                  you would give blobstore" >&2
  echo "" >&2
  echo "optional arguments:" >&2
  echo "  -d, --dryrun  dry-run - do only parameter expansion and template pre-processing and azure cli what-if operation" >&2
  echo "  -v, --verbose verbose - verbose output from azure cli" >&2
  echo "  -h, --help    show this help message and exit" >&2
  if "$@"; then
    echo "" >&2
    echo "$@" >&2
  fi
}

die() {
  set +x
  echo "$1" >&2
  usage
  exit 1
}

DRYRUN=0
HELP=0
ARGS=()

# Iterate over all arguments
while (( "$#" )); do
  case "$1" in
    -h|--help)
      HELP=1
      shift
      ;;
    -d|--dry-run)
      DRYRUN=1
      shift
      ;;
    *) # Preserve other arguments
      ARGS+=("$1")
      shift
      ;;
  esac
done

# If help is requested, show usage
if [ "$HELP" -eq 1 ]; then
  usage
  exit 0
fi

# Process the remaining arguments
if [ ${#ARGS[@]} -lt 2 ]; then
  die "You must specify both the component and the azure name."
fi
set -xe
component="${ARGS[0]}"
azure="${ARGS[1]}"

TSTAMP=$(date +%Y%m%d%H%M%S)
if [ -z "$BUILD_NUMBER" ]; then
  BUILD_NUMBER=$TSTAMP
else
  BUILD_NUMBER=$(printf "%04d\n" $BUILD_NUMBER)
fi

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

PARAMETERS="$component/azure-$ORIG_AZURE_NAME/variables.json"
if [ -r "$component/azure-$ORIG_AZURE_NAME/template.yaml" ]; then
  DEPLOY_TEMPLATE="$component/azure-$ORIG_AZURE_NAME/azuredeploy.json"
  ndt yaml-to-json "$component/azure-$ORIG_AZURE_NAME/template.yaml" > "$DEPLOY_TEMPLATE"
  TEMPLATE_TYPE=json
elif [ -r "$component/azure-$ORIG_AZURE_NAME/template.bicep" ]; then
  DEPLOY_TEMPLATE="$component/azure-$ORIG_AZURE_NAME/azuredeploy.bicep"
  ndt interpolate-file -n -o "$DEPLOY_TEMPLATE" "$component/azure-$ORIG_AZURE_NAME/template.bicep"
  TEMPLATE_TYPE=bicep
else
  echo "Template not found. Looked for $component/azure-$ORIG_AZURE_NAME/template.yaml and $component/azure-$ORIG_AZURE_NAME/template.bicep"
  exit 1
fi
ndt load-parameters "$component" -a "$azure" -z -r -f "$(ndt azure-template-parameters "$DEPLOY_TEMPLATE")" > "$PARAMETERS"

cd "$component/azure-$ORIG_AZURE_NAME"

if [ -x "./pre_deploy.sh" ]; then
  "./pre_deploy.sh"
fi

if [ -r "./pre_deploy_source.sh" ]; then
  source "./pre_deploy_source.sh"
fi

case "$AZURE_SCOPE" in
  group)
    SCOPE_COMMAND="group"
    GROUP_ARGS="--resource-group $AZURE_GROUP"
    ndt azure-ensure-group -l $AZURE_LOCATION "$AZURE_GROUP"
    ;;
  management-group)
    SCOPE_COMMAND="mg"
    GROUP_ARGS="--management-group-id $AZURE_MANAGEMENT_GROUP"
    ndt azure-ensure-management-group "$AZURE_MANAGEMENT_GROUP"
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

if [ "$DRYRUN" -eq 1 ]; then
  WHATIF_ARG="--confirm-with-what-if"
fi

set -e
az $VERBOSE deployment $SCOPE_COMMAND create \
  --name $DEPLOYMENT_NAME \
  $GROUP_ARGS \
  $WHATIF_ARG \
  --template-file azuredeploy.$TEMPLATE_TYPE \
  --parameters @variables.json

if [ -x "./post_deploy.sh" ]; then
  "./post_deploy.sh"
fi
