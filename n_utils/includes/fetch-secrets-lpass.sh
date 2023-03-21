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
[ "$CF_paramSecretsUser" ] || CF_paramSecretsUser="$(ndt cf-get-parameter paramSecretsUser)"

login_if_not_already() {
  if ! lpass ls not-meant-to-return-anything > /dev/null 2>&1; then
    export AWS_DEFAULT_REGION=$(ndt ec2-region)
    aws s3 cp s3://${CF_paramSecretsBucket}/webmaster.pwd - | $(n-include lastpass-login.sh) ${CF_paramSecretsUser} - > /dev/null 2>&1
  fi
}

case "$1" in
  login)
    # usage: fetch-secrets.sh login
    shift
    login_if_not_already
    ;;
  get)
    # usage: fetch-secrets.sh get <mode> [<file> ...] [--optional <file> ...]
    # logs in automatically if necessary
    shift
    mode="$1"
    shift
    login_if_not_already
    lastpass-fetch-notes.sh "$mode" "$@"
    ;;
  show)
    shift
    login_if_not_already
    lpass show --password "$1"
    ;;
  logout)
    # usage: fetch-secrets.sh logout
    $(n-include lastpass-logout.sh)
    ;;
  *)
    # old api
    export AWS_DEFAULT_REGION=$(ndt ec2-region)
    aws s3 cp s3://${CF_paramSecretsBucket}/webmaster.pwd .lpass-key
    chmod 600 .lpass-key
    lastpass-cert.sh "$@"
    rm -f .lpass-key
    ;;
esac
