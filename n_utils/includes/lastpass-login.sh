#!/bin/bash -e

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
  # Handle command completion executions
  case $COMP_CWORD in
    2)
      exit 0
      ;;
    *)
      echo '-'
      compgen -f -- $COMP_CUR
      ;;
  esac
  exit 0
fi

LPASS_USER="$1"
LPASS_PASSFILE="$2"

if [ ! "$LPASS_USER" -o ! "$LPASS_PASSFILE" ]; then
  echo "usage: $0 <lastpass-username> <lastpass-password-file>" >&2
  echo "lastpass-password-file can be - to read password from stdin."
  exit 1
fi

if [ "$LPASS_PASSFILE" = "-" ]; then
  LPASS_DISABLE_PINENTRY=1 lpass login --plaintext-key -f "$LPASS_USER" 2>&1 > /dev/null
else
  if ! [ -r "$LPASS_PASSFILE" -a "$(stat -c '%a' "$LPASS_PASSFILE")" = "600" ]; then
    echo "Requires $LPASS_PASSFILE with only user access with the lastpass password"
    exit 1
  fi
  LPASS_DISABLE_PINENTRY=1 lpass login --plaintext-key -f "$LPASS_USER" < "$LPASS_PASSFILE" 2>&1 > /dev/null
fi

lpass sync 2>&1 > /dev/null
