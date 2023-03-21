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

[ "$CF_paramSecretsBucket" ] || CF_paramSecretsBucket="$(ndt cf-get-parameter paramSecretsBucket)"

COMMAND=$1
shift

case "$COMMAND" in
  get)
    MODE=$1
    shift
    ;;
  show)
    SHOW=1
    ;;
  login | logout)
    exit 0
    ;;
  *)
    #old api
    MODE=444
    ;;
esac

RET=0
for ABS_FILE in "$@"; do
  if [ "$ABS_FILE" == "--optional" ]; then
    OPTIONAL=true
    continue
  fi
  if [ -z "$SHOW" ]; then
    FILE=$(basename $ABS_FILE)
    DIR=$(dirname $ABS_FILE)
    mkdir -p $DIR
  else
    FILE=$ABS_FILE
    ABS_FILE="-"
  fi
  if aws s3 cp "s3://${CF_paramSecretsBucket}/$FILE" "$ABS_FILE"; then
    if [ -z "$SHOW" ]; then
      chmod $MODE $ABS_FILE
    fi
  elif [ -z "$OPTIONAL" ]; then
    RET=$(($RET + 1))
  fi
done
exit $RET
