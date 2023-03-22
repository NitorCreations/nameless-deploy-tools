#!/bin/bash

# Copyright 2016-2023 Nitor Creations Oy
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

set -eo pipefail

USAGE="Usage: $0 [OPTIONS]

Create new release for ndt.

OPTIONS: All options are optional
  -h | --help
      Display these instructions.

  -d | --dryrun
      Only print commands instead of executing them.

  -v | --verbose
      Display commands being executed."

init_options() {
  DRYRUN=false
    while [ $# -gt 0 ]; do
      case "$1" in
        -h | --help)
          echo "$USAGE"
          exit 1
          ;;
        -d | --dryrun)
          DRYRUN=true
          ;;
        -v | --verbose)
          set -x
          ;;
    esac
      shift
  done
}

init_options "$@"

# Import common functions
DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
# shellcheck source=./common.sh
source "$DIR/common.sh"

VERSION=$(grep -E '^VERSION' n_utils/__init__.py | cut -d\" -f 2)
MAJOR=${VERSION//.*/}
MINOR=${VERSION##*.}
if [ "$1" = "-m" ]; then
  MAJOR=$(($MAJOR + 1))
  MINOR="0"
  NEW_VERSION=$MAJOR.$MINOR
  shift
elif [ "$1" = "-v" ]; then
  shift
  NEW_VERSION="$1"
  shift
else
  MINOR=$(($MINOR + 1))
  NEW_VERSION=$MAJOR.$MINOR
  MESSAGE="$1"
fi

if [ -z "$MESSAGE" ]; then
  MESSAGE="$NEW_VERSION"
fi

print_magenta "Updating command list..."
./update-commandlist.sh
"${SED_COMMAND[@]}" "s/$VERSION/$NEW_VERSION/g" setup.cfg
"${SED_COMMAND[@]}" "s/$VERSION/$NEW_VERSION/g" pyproject.toml
"${SED_COMMAND[@]}" "s/## Released version.*/## Released version $NEW_VERSION/g" README.md
"${SED_COMMAND[@]}" "s/nameless-deploy-tools==.*/nameless-deploy-tools==$NEW_VERSION/g" docker/Dockerfile
"${SED_COMMAND[@]}" "s/^VERSION.*=.*/VERSION\ =\ \"$NEW_VERSION\"/" n_utils/__init__.py

print_magenta "Version tagging release..."
run_command git commit -m "$1" setup.cfg pyproject.toml README.md docker/Dockerfile docs/commands.md n_utils/__init__.py
run_command git tag "$NEW_VERSION" -m "$MESSAGE"
run_command git push origin "$NEW_VERSION"

check_and_set_python

print_magenta "Build and upload package..."
rm -rf dist/*
$PYTHON setup.py sdist bdist_wheel
run_command twine upload dist/*
run_command sleep 30

print_magenta "Building Docker image..."
run_command ./build-docker.sh "$NEW_VERSION"
