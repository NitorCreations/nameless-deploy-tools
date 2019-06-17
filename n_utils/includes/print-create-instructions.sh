#!/bin/bash

if [ "$_ARGCOMPLETE" ]; then
  unset _ARGCOMPLETE
  source $(n-include autocomplete-helpers.sh)
  # Handle command completion executions
  COMP_WORDS=( $COMP_LINE )
  IMAGE_DIR=${COMP_WORDS[2]}
  STACK=${COMP_WORDS[3]}
  IMAGE=$(echo $IMAGE_DIR| tr "-" "_")
  case $COMP_CWORD in
    2)
      compgen -W "$(get_stack_dirs)" -- $COMP_CUR
      ;;
    3)
      compgen -W "$(get_stacks $IMAGE_DIR)" -- $COMP_CUR
      ;;
    *)
      exit 1
      ;;
  esac
  exit 0
fi

usage() {
  echo "usage: ndt print-create-instructions [-h] component stack-name" >&2
  echo "" >&2
  echo "Prints out the instructions to create and deploy the resources in a stack"
  echo "" >&2
  echo "positional arguments:" >&2
  echo "  component   the component directory where the stack template is" >&2
  echo "  stack-name  the name of the stack directory inside the component directory" >&2
  echo "              For example for ecs-cluster/stack-cluster/template.yaml" >&2
  echo "              you would give cluster" >&2
  echo "" >&2
  echo "optional arguments:" >&2
  echo "  -h, --help  show this help message and exit" >&2
  exit 1
}
if [ "$1" = "--help" -o "$1" = "-h" ]; then
  usage
fi
source $(n-include autocomplete-helpers.sh)

COMPONENT=$1
STACK=$2

[ "$GIT_BRANCH" ] || GIT_BRANCH="$(git rev-parse --abbrev-ref HEAD)"

if [ -d $COMPONENT/image ]; then
  echo "You can bake the component image by running 'ndt bake-image $COMPONENT'"
  eval "$(ndt load-parameters -e "$1")"
fi

PREFIX=$COMPONENT/docker-
if ls $COMPONENT/docker-* > /dev/null 2>&1; then
  for DOCKER in $COMPONENT/docker-*; do
    DOCKER_NAME=${DOCKER#$PREFIX}
    echo "You can bake the $DOCKER_NAME docker image by running 'ndt bake-docker $COMPONENT $DOCKER_NAME'"
  done
fi

echo "You can deploy the stack $STACK by running 'ndt deploy-stack $COMPONENT $STACK'"