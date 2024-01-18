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

set -eo pipefail

USAGE="Usage: $0 [OPTIONS] [MESSAGE]

Create new release for ndt.

OPTIONS: All options are optional
  -h | --help
    Display these instructions.

  -d | --dryrun
    Only print commands instead of executing them.

  -m | --major
    Increment major version.

  --message
    Message for git version tag.

  -v | --version <NEW_VERSION>
    Use given version as the new version number.

  --verbose
    Display commands being executed."

init_options() {
  DRYRUN=false
  INCREMENT_MAJOR=false
  while [ $# -gt 0 ]; do
    case "$1" in
      -h | --help)
        echo "$USAGE"
        exit 1
        ;;
      -d | --dryrun)
        DRYRUN=true
        ;;
      -m | --major)
        INCREMENT_MAJOR=true
        ;;
      --message)
        MESSAGE="$2"
        shift
        ;;
      -v | --version)
        NEW_VERSION="$2"
        shift
        ;;
      --verbose)
        set -x
        ;;
      *)
        MESSAGE="$1"
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

if [ "$INCREMENT_MAJOR" = true ]; then
  echo "Incrementing major version"
  MAJOR=$(($MAJOR + 1))
  MINOR="0"
  NEW_VERSION=$MAJOR.$MINOR
elif [ -z "$NEW_VERSION" ]; then
  echo "Incrementing minor version"
  MINOR=$(($MINOR + 1))
  NEW_VERSION=$MAJOR.$MINOR
fi

echo "Current version: $VERSION"
print_green "New version:     $NEW_VERSION"

if [ -z "$MESSAGE" ]; then
  print_yellow "No message given, using new version"
  MESSAGE="$NEW_VERSION"
fi

print_magenta "Updating command list..."
./update-commandlist.sh
"${SED_COMMAND[@]}" "s/$VERSION/$NEW_VERSION/g" setup.cfg
"${SED_COMMAND[@]}" "s/$VERSION/$NEW_VERSION/g" pyproject.toml
"${SED_COMMAND[@]}" "s/## Released version.*/## Released version $NEW_VERSION/g" README.md
"${SED_COMMAND[@]}" "s/^VERSION.*=.*/VERSION\ =\ \"$NEW_VERSION\"/" n_utils/__init__.py

print_magenta "Version tagging release..."
git commit -m "$MESSAGE" setup.cfg pyproject.toml README.md docs/commands.md n_utils/__init__.py
git tag "$NEW_VERSION" -m "$MESSAGE"
run_command git push
run_command git push origin "$NEW_VERSION"

check_and_set_python

print_magenta "Build and upload package..."
rm -rf dist/*
# https://pypa-build.readthedocs.io/en/stable/
$PYTHON -m build
run_command twine upload dist/*
