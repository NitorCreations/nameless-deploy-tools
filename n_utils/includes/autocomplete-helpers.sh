#!/bin/bash

get_bakeable_images() {
  if [ -r infra.properties -o -r infra-master.properties ]; then
    echo $(find . -mindepth 2 -maxdepth 2 -name image -a -type d -o -name 'image-*' -a -type d | cut -d '/' -f 2)
  fi
}
get_stack_dirs() {
  if [ -r infra.properties -o -r infra-master.properties ]; then
    echo $(find . -mindepth 2 -maxdepth 3 -name 'infra*.properties' | cut -d '/' -f 2 | sort -u)
  fi
}
get_stacks() {
  if [ -r infra.properties -o -r infra-master.properties ]; then
    echo $(find $1 -mindepth 1 -maxdepth 1 -name 'stack-*' | sed 's/.*stack-\(.*\)/\1/g')
  fi
}
get_imageids() {
  if [ -r infra.properties -o -r infra-master.properties ]; then
    [ "$GIT_BRANCH" ] || GIT_BRANCH="$(git rev-parse --abbrev-ref HEAD)"
    GIT_BRANCH=${GIT_BRANCH##*/}
    if [ -d "$1/image" ] && [ -r "$1/infra.properties" -o -r "$1/infra-$GIT_BRANCH.properties" ]; then
      ndt get-images $2 | cut -d: -f1
    fi
  fi
}
get_images() {
  if [ -r infra.properties -o -r infra-master.properties ]; then
    echo $(find $1 -mindepth 1 -maxdepth 1 -name image -o -name 'image-*' | sed -e 's/.*image\(.*\)/\1/g' -e 's/^-//')
  fi
}
get_dockers() {
  if [ -r infra.properties -o -r infra-master.properties ]; then
    echo $(find $1 -mindepth 1 -maxdepth 1 -name 'docker-*' | sed 's/.*docker-\(.*\)/\1/g')
  fi
}
get_serverless() {
  if [ -r infra.properties -o -r infra-master.properties ]; then
    echo $(find $1 -mindepth 1 -maxdepth 1 -name 'serverless-*' | sed 's/.*serverless-\(.*\)/\1/g')
  fi
}
get_cdk() {
  if [ -r infra.properties -o -r infra-master.properties ]; then
    echo $(find $1 -mindepth 1 -maxdepth 1 -name 'cdk-*' | sed 's/.*cdk-\(.*\)/\1/g')
  fi
}
get_terraform() {
  if [ -r infra.properties -o -r infra-master.properties ]; then
    echo $(find $1 -mindepth 1 -maxdepth 1 -name 'terraform-*' | sed 's/.*terraform-\(.*\)/\1/g')
  fi
}
get_azure() {
  if [ -r infra.properties -o -r infra-master.properties ]; then
    echo $(find $1 -mindepth 1 -maxdepth 1 -name 'azure-*' | sed 's/.*azure-\(.*\)/\1/g')
  fi
}
checkout_branch() {
  local BRANCH=$1
  mkdir -p "$BRANCH-checkout" > /dev/null 2>&1
  git archive "origin/$BRANCH" | tar -xC "$BRANCH-checkout" > /dev/null 2>&1
  if [ -r "$BRANCH-checkout/infra.properties" ] || [ -r "$BRANCH-checkout/infra-$BRANCH.properties" ]; then
    echo $BRANCH
  else
    rm -rf "$BRANCH-checkout" > /dev/null 2>&1
  fi
}
job_properties() {
  ndt load-parameters $2 $3 $4 -p -b $1
}

current_branch_job_properties() {
  [ "$GIT_BRANCH" ] || GIT_BRANCH="$(git rev-parse --abbrev-ref HEAD)"
  GIT_BRANCH=${GIT_BRANCH##*/}
  job_properties $GIT_BRANCH $1 $2 $3
}
