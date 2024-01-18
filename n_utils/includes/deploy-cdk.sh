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
        SUBMODULES="$(get_cdk $FOUND_STACK_DIR)"
      fi
    else
      SUBMODULES="$(get_cdk $FOUND_STACK_DIR)"
    fi
  done
  compgen -W "${DRY}${HELP}${STACK_DIRS}${SUBMODULES}" -- $COMP_CUR
  exit 0
fi

usage() {
  echo "usage: ndt deploy-cdk [-d] [-h] component cdk-name" >&2
  echo "" >&2
  echo "Exports ndt parameters into component/cdk-name/variables.json, runs pre_deploy.sh in the" >&2
  echo "cdk project and runs cdk diff; cdk deploy for the same" >&2
  echo "If pre_deploy.sh and post_deploy.sh exist and are executable in the subcompoent directory," >&2
  echo "they will be executed before and after the deployment, respectively." >&2
  echo "Similarly if a readable pre_deploy_source.sh exists in the subcompoent directory," >&2
  echo "it will be sourced before the deployment to enable things like activating a python venv." >&2
  echo "" >&2
  echo "positional arguments:" >&2
  echo "  component   the component directory where the cdk directory is" >&2
  echo "  cdk-name the name of the cdk directory that has the template" >&2
  echo "                  For example for lambda/cdk-sender/bin/MyProject.ts" >&2
  echo "                  you would give sender" >&2
  echo "" >&2
  echo "optional arguments:" >&2
  echo "  -d, --dryrun  dry-run - do only parameter expansion and pre_deploy.sh and cdk diff" >&2
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
  die "You must specify both the component and the cdk name."
fi
set -xe
component="${ARGS[0]}"
cdk="${ARGS[1]}"

TSTAMP=$(date +%Y%m%d%H%M%S)
if [ -z "$BUILD_NUMBER" ]; then
  BUILD_NUMBER=$TSTAMP
else
  BUILD_NUMBER=$(printf "%04d\n" $BUILD_NUMBER)
fi

eval "$(ndt load-parameters "$component" -c "$cdk" -e -r)"

#If assume-deploy-role.sh is on the path, run it to assume the appropriate role for deployment
if [ -n "$DEPLOY_ROLE_ARN" ] && [ -z "$AWS_SESSION_TOKEN" ]; then
  eval $(ndt assume-role $DEPLOY_ROLE_ARN)
elif which assume-deploy-role.sh &> /dev/null && [ -z "$AWS_SESSION_TOKEN" ]; then
  eval $(assume-deploy-role.sh)
fi

ndt load-parameters "$component" -c "$cdk" -j -r > "$component/cdk-$ORIG_CDK_NAME/variables.json"

cd "$component/cdk-$ORIG_CDK_NAME"

if [ -x "./pre_deploy.sh" ]; then
  "./pre_deploy.sh"
fi

if [ -r "./pre_deploy_source.sh" ]; then
  source "./pre_deploy_source.sh"
fi

npx cdk synth
npx cdk diff || :

if [ "$DRYRUN" -eq 1 ]; then
  echo "Dry run - quitting"
  exit 0
fi

set -e
npx cdk deploy --ci --require-approval never

if [ -x "./post_deploy.sh" ]; then
  "./post_deploy.sh"
fi
