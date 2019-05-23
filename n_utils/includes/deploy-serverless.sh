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
      compgen -W "$(get_serverless $COMP_PREV)" -- $COMP_CUR
      ;;
    *)
      exit 1
      ;;
  esac
  exit 0
fi

usage() {
  echo "usage: ndt deploy-serverless [-d] [-h] component serverless-name" >&2
  echo "" >&2
  echo "Exports ndt parameters into component/serverless-name/variables.yml, runs npm i in the" >&2
  echo "serverless project and runs sls deploy -s \$paramEnvId for the same" >&2
  echo "" >&2
  echo "positional arguments:" >&2
  echo "  component   the component directory where the serverless directory is" >&2
  echo "  serverless-name the name of the serverless directory that has the template" >&2
  echo "                  For example for lambda/serverless-sender/template.yaml" >&2
  echo "                  you would give sender" >&2
  echo "" >&2
  echo "optional arguments:" >&2
  echo "  -d, --dryrun  dry-run - do only parameter expansion and template pre-processing and npm i"  >&2
  echo "  -v, --verbose verbose - verbose output from serverless framework"  >&2
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
    VERBOSE="-v"
    shift
  fi
done
die () {
  echo "$1" >&2
  usage
}
set -xe

component="$1" ; shift
[ "${component}" ] || die "You must give the component name as argument"
serverless="$1"; shift
[ "${serverless}" ] || die "You must give the serverless name as argument"

TSTAMP=$(date +%Y%m%d%H%M%S)
if [ -z "$BUILD_NUMBER" ]; then
  BUILD_NUMBER=$TSTAMP
else
  BUILD_NUMBER=$(printf "%04d\n" $BUILD_NUMBER)
fi

eval "$(ndt load-parameters "$component" -l "$serverless" -e -r)"

#If assume-deploy-role.sh is on the path, run it to assume the appropriate role for deployment
if [ -n "$DEPLOY_ROLE_ARN" ] && [ -z "$AWS_SESSION_TOKEN" ]; then
  eval $(ndt assume-role $DEPLOY_ROLE_ARN)
elif which assume-deploy-role.sh > /dev/null && [ -z "$AWS_SESSION_TOKEN" ]; then
  eval $(assume-deploy-role.sh)
fi

ndt load-parameters "$component" -l "$serverless" -y -r > "$component/serverless-$ORIG_SERVERLESS_NAME/variables.yml"
ndt yaml-to-yaml "$component/serverless-$ORIG_SERVERLESS_NAME/template.yaml" > "$component/serverless-$ORIG_SERVERLESS_NAME/serverless.yml"

cd "$component/serverless-$ORIG_SERVERLESS_NAME"

if [ -x "./pre_deploy.sh" ]; then
  "./pre_deploy.sh"
fi

if [ -z "$SKIP_NPM" -o "$SKIP_NPM" = "n" ]; then
  npm i
fi

if [ -n "$DRYRUN" ]; then
  sls package $VERBOSE -s $paramEnvId
  exit 0
fi

sls deploy $VERBOSE -s $paramEnvId