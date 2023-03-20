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

mode="444"

fetch() {
  for path; do
    if [ "$path" = "--optional" ]; then
      optional=1
      continue
    fi
    FNAME="$(basename "$path")"
    DNAME="$(dirname "$path")"
    mkdir -p "$DNAME"
    if [ -e "$path" ]; then
      TMPDIR=$(mktemp -d $path.XXXXXXX)
      mv "$path" "$TMPDIR/"
    fi
    if ! vault -l "$FNAME" > "$path"; then
      rm -f "$path"
      if [ -n "$TMPDIR" ]; then
        mv "$TMPDIR/$FNAME" "$path"
        rm -rf "$TMPDIR"
      fi
      if [ ! "$optional" ]; then
        echo "ERROR: Failed to get file $path"
        exit 1
      else
        echo "Optional file $path not found"
      fi
    else
      chmod $mode $path
      rm -rf "$TMPDIR"
      echo "Fetched $path"
    fi
  done
}

case "$1" in
  login)
    # usage: fetch-secrets.sh login
    shift
    ;;
  get)
    # usage: fetch-secrets.sh get <mode> [<file> ...] [--optional <file> ...]
    # logs in automatically if necessary
    shift
    mode="$1"
    shift
    fetch "$@"
    ;;
  show)
    shift
    vault -l "$1"
    ;;
  logout)
    # usage: fetch-secrets.sh logout
    shift
    ;;
  *)
    fetch "$@"
    ;;
esac
