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

# Import common functions
DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
# shellcheck source=./common.sh
source "$DIR/common.sh"

USAGE="Usage: $0 [OPTIONS]

Re-compile requirements files using pip compile.

OPTIONS: All options are optional
  -h | --help      Display these instructions.
  -c | --commit    Create git commit for changes to requirements.
  -d | --dryrun    Only print commands instead of executing them.
  -x | --verbose   Display commands being executed."

DRYRUN=false
COMMIT_CHANGES=false
while [ $# -gt 0 ]; do
  case "$1" in
    -h | --help)
      echo "$USAGE"
      exit 1
      ;;
    -c | --commit)
      COMMIT_CHANGES=true
      ;;
    -d | --dryrun)
      DRYRUN=true
      ;;
    -x | --verbose)
      set -x
      ;;
  esac
  shift
done

cd "$REPO_ROOT"

if [ -n "$(command -v uv)" ]; then
  COMPILE_CMD="uv pip compile"
elif [ -n "$(command -v pip-compile)" ]; then
  print_yellow "uv is the recommended tool for running pip compile: https://github.com/astral-sh/uv"
  if [ -n "$(command -v pipx)" ]; then
    echo "Installing pip-tools with pipx"
    pipx install pip-tools
    COMPILE_CMD="pip-compile"
  fi
fi

if [ -z "$COMPILE_CMD" ]; then
  print_error_and_exit "pip tools are not installed. Use uv, or install 'pip-tools' with pipx."
fi

# Remove old files to force upgrade of all dependencies
rm -f requirements.txt dev-requirements.txt

print_magenta "Compiling requirements.txt"
$COMPILE_CMD --output-file=requirements.txt --strip-extras pyproject.toml

print_magenta "Compiling dev-requirements.txt"
$COMPILE_CMD --output-file=dev-requirements.txt --all-extras pyproject.toml

if [ "$COMMIT_CHANGES" = true ]; then
  git add requirements.txt dev-requirements.txt
  if git diff --name-only --cached | grep -qE '^(requirements\.txt|dev-requirements\.txt)$'; then
    run_command git commit -m "re-compile requirements"
  else
    print_yellow "No changes to requirements files. Skipping commit."
  fi
fi
