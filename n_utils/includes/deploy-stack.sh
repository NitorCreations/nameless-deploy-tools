#!/bin/bash

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

if [ "$_ARGCOMPLETE" ]; then
  unset _ARGCOMPLETE
  source $(n-include autocomplete-helpers.sh)
  # Handle command completion executions
  COMP_WORDS=( $COMP_LINE )
  if [ "${COMP_WORDS[2]}" = "-d" ]; then 
    COMP_INDEX=$(($COMP_CWORD - 1))
    IMAGE_DIR=${COMP_WORDS[3]}
    STACK=${COMP_WORDS[4]}
  else
    COMP_INDEX=$COMP_CWORD
    IMAGE_DIR=${COMP_WORDS[2]}
    STACK=${COMP_WORDS[3]}
  fi
  IMAGE=$(echo $IMAGE_DIR| tr "-" "_")
  case $COMP_INDEX in
    2)
      if [ "$COMP_INDEX" = "$COMP_CWORD" ]; then
        DRY="-d "
      fi
      compgen -W "-h $DRY$(get_stack_dirs)" -- $COMP_CUR
      ;;
    3)
      compgen -W "$(get_stacks "$IMAGE_DIR")" -- $COMP_CUR
      ;;
    4)
      eval "$(ndt load-parameters "$IMAGE_DIR" -s "$STACK" -e)"
      JOB_NAME="${BUILD_JOB_PREFIX}_${IMAGE}_bake"
      IMAGE_IDS="$(get_imageids $IMAGE_DIR $JOB_NAME)"
      compgen -W "$IMAGE_IDS" -- $COMP_CUR
      ;;
    5)
      eval "$(ndt load-parameters "$IMAGE_DIR" -s "$STACK" -e)"
      echo "${BUILD_JOB_PREFIX}_${IMAGE}_bake"
      ;;
    *)
      exit 1
      ;;
  esac
  exit 0
fi

usage() {
  echo "usage: ndt deploy-stack [-d] [-h] component stack-name ami-id bake-job" >&2
  echo "" >&2
  echo "Resolves potential ECR urls and AMI Ids and then deploys the given stack either updating or creating it." >&2
  echo "positional arguments:" >&2
  echo "  component   the component directory where the stack template is" >&2
  echo "  stack-name  the name of the stack directory inside the component directory" >&2
  echo "              For example for ecs-cluster/stack-cluster/template.yaml" >&2
  echo "              you would give cluster" >&2
  echo "  ami-id      If you want to specify a value for the paramAmi variable in the stack," >&2
  echo "              you can do so. Otherwise give an empty string with two quotation marks" >&2
  echo "  bake-job    If an ami-id is not given, the ami id is resolved by getting the latest" >&2
  echo "              ami that is tagged with the bake-job name"
  echo "" >&2
  echo "optional arguments:" >&2
  echo "  -d, --dryrun  dry-run - show only the change set without actually deploying it" >&2
  echo "  -h, --help  show this help message and exit" >&2
  exit 1
}
if [ "$1" = "--help" -o "$1" = "-h" ]; then
  usage
fi

source "$(n-include autocomplete-helpers.sh)"

set -xe

if [ "$1" = "-d" ]; then
  DRY_RUN="--dry-run"
  shift
fi
component="$1" ; shift
stackName="$1" ; shift
ARG_AMI_ID="$1"
shift ||:
ARG_IMAGE_JOB="$1"
shift ||:

if [ -n "$ARG_AMI_ID" ]; then
  export AMI_ID=$ARG_AMI_ID paramAmi=$ARG_AMI_ID
fi
if [ -n "$ARG_IMAGE_JOB" ]; then
  export IMAGE_JOB=$ARG_IMAGE_JOB
fi

eval "$(ndt load-parameters "$component" -s "$stackName" -e -r)"

#If assume-deploy-role.sh is on the path, run it to assume the appropriate role for deployment
if [ -n "$DEPLOY_ROLE_ARN" ] && [ -z "$AWS_SESSION_TOKEN" ]; then
  eval $(ndt assume-role $DEPLOY_ROLE_ARN)
elif which assume-deploy-role.sh &> /dev/null && [ -z "$AWS_SESSION_TOKEN" ]; then
  eval $(assume-deploy-role.sh)
fi

cd ${component}/stack-${ORIG_STACK_NAME}
if [ -x "./pre_deploy.sh" ]; then
  "./pre_deploy.sh"
fi
cd ../..

set -e
cf-update-stack "${STACK_NAME}" "${component}/stack-${ORIG_STACK_NAME}/template.yaml" "$REGION" $DRY_RUN

cd ${component}/stack-${ORIG_STACK_NAME}
if [ -z "$DRY_RUN" ] && [ -x "./post_deploy.sh" ]; then
  "./post_deploy.sh"
fi
