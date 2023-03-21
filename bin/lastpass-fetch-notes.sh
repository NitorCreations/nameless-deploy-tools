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
      echo "-h"
      ;;
    *)
      echo '--optional'
      compgen -f -- $COMP_CUR
      ;;
  esac
  exit 0
fi

usage() {
  echo "usage: lasptass-fetch-notes.sh [-h] mode file [file ...] [--optional file ...]" >&2
  echo "" >&2
  echo "Fetches secure notes from lastpass that match the basename of each listed file." >&2
  echo "Files specified after --optional won't fail if the file does not exist." >&2
  echo "" >&2
  echo "positional arguments" >&2
  echo "  mode   the file mode for the downloaded files" >&2
  echo "  file   the file(s) to download. The source will be the note that matches the basename of the file" >&2
  echo "" >&2
  echo "optional arguments:" >&2
  echo "  --optional  marks that following files will not fail and exit the script in they do not exist"
  echo "  -h, --help  show this help message and exit" >&2
  exit 1
}

if [ "$1" = "--help" -o "$1" = "-h" ]; then
  usage
fi

mode="$1"
shift

if [ ! "$mode" ]; then
  usage
fi

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
  if ! lpass show --notes "$FNAME" > "$path"; then
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
      rm -f $path
    fi
  else
    chmod $mode $path
    rm -rf "$TMPDIR"
    echo "Fetched $path"
  fi
done
