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
      compgen -W "-h -i $(get_stack_dirs)" -- $COMP_CUR
      ;;
    3)
      compgen -W "$(get_dockers $COMP_PREV)" -- $COMP_CUR
      ;;
    *)
      exit 1
      ;;
  esac
  exit 0
fi

usage() {
  echo "usage: ndt bake-docker [-h] [-i] component docker-name" >&2
  echo "" >&2
  echo "Runs a docker build, ensures that an ecr repository with the docker name" >&2
  echo "(by default <component>/<branch>-<docker-name>) exists and pushes the built" >&2
  echo "image to that repository with the tags \"latest\" and \"\$BUILD_NUMBER\"" >&2
  echo "" >&2
  echo "positional arguments:" >&2
  echo "  component   the component directory where the docker directory is" >&2
  echo "  docker-name the name of the docker directory that has the Dockerfile" >&2
  echo "              For example for ecs-cluster/docker-cluster/Dockerfile" >&2
  echo "              you would give cluster" >&2
  echo "" >&2
  echo "optional arguments:" >&2
  echo "  -h, --help  show this help message and exit"  >&2
  echo "  -i, --imagedefinitions  create imagedefinitions.json for AWS CodePipeline"  >&2
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
  usage
}
set -xe

if [ "$1" = "--imagedefinitions" -o "$1" = "-i" ]; then
  shift
  OUTPUT_DEFINITION=1
fi

component="$1" ; shift
[ "${component}" ] || die "You must give the component name as argument"
docker="$1"; shift
[ "${docker}" ] || die "You must give the docker name as argument"

TSTAMP=$(date +%Y%m%d%H%M%S)
if [ -z "$BUILD_NUMBER" ]; then
  BUILD_NUMBER=$TSTAMP
else
  BUILD_NUMBER=$(printf "%04d\n" $BUILD_NUMBER)
fi

[ -d "$component/docker-$ORIG_DOCKER_NAME" ] || die "Docker directory $component/docker-$ORIG_DOCKER_NAME does not exist"

eval "$(ndt load-parameters "$component" -d "$docker" -e)"

if [ -x "$component/docker-$ORIG_DOCKER_NAME/pre_build.sh" ]; then
  cd "$component/docker-$ORIG_DOCKER_NAME"
  "./pre_build.sh"
  cd ../..
fi

#If assume-deploy-role.sh is on the path, run it to assume the appropriate role for deployment
if [ -n "$DOCKER_BAKE_ROLE_ARN" ] && [ -z "$AWS_SESSION_TOKEN" ]; then
  eval "$(ndt assume-role "DOCKER_BAKE_ROLE_ARN")"
elif [ -n "$DEPLOY_ROLE_ARN" ] && [ -z "$AWS_SESSION_TOKEN" ]; then
  eval "$(ndt assume-role "$DEPLOY_ROLE_ARN")"
elif which assume-deploy-role.sh > /dev/null && [ -z "$AWS_SESSION_TOKEN" ]; then
  eval "$(assume-deploy-role.sh)"
fi

eval "$(ndt session-to-env)"

docker build -t "$DOCKER_NAME" --build-arg "AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID"  --build-arg "AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY" --build-arg "AWS_SESSION_TOKEN=$AWS_SESSION_TOKEN" "$component/docker-$ORIG_DOCKER_NAME"

eval "$(ndt ecr-ensure-repo "$DOCKER_NAME")"
docker tag $DOCKER_NAME:latest $DOCKER_NAME:$BUILD_NUMBER
docker tag $DOCKER_NAME:latest $REPO:latest
docker tag $DOCKER_NAME:$BUILD_NUMBER $REPO:$BUILD_NUMBER
docker push $REPO:latest
docker push $REPO:$BUILD_NUMBER

if [ -n "$OUTPUT_DEFINITION" ]; then
  printf '[{"name":"%s","imageUri":"%s"}]' $docker $REPO:$BUILD_NUMBER > imagedefinitions.json
fi
