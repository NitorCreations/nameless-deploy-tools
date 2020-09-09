#!/bin/bash

# Copyright 2017 Nitor Creations Oy
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
  case $COMP_CWORD in
    2)
      compgen -W "-h lpass s3 vault" -- $COMP_CUR
      ;;
    *)
      exit 1
      ;;
  esac
  exit 0
fi

usage() {
  echo "usage: setup-fetch-secrets.sh [-h] <lpass|s3|vault>" >&2
  echo "" >&2
  echo "Sets up a global fetch-secrets.sh that fetches secrets from either LastPass, S3 or nitor-vault" >&2
  echo "" >&2
  echo "positional arguments" >&2
  echo "  lpass|s3|vault   the selected secrets backend." >&2
  echo "" >&2
  echo "optional arguments:" >&2
  echo "  -h, --help  show this help message and exit" >&2  exit 1
}

if [ "$1" = "--help" -o "$1" = "-h" ]; then
  usage
fi

if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit 1
fi
if ! [[ "$1" =~ ^lpass$|^s3$|^vault$ ]]; then
  echo "usage: $0 <lpass|s3|vault>"
  exit 1
fi

ln -snf $(n-include fetch-secrets-$1.sh) /usr/bin/fetch-secrets.sh
ln -snf $(n-include store-secret-$1.sh) /usr/bin/store-secret.sh
