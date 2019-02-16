#!/bin/bash

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

set -xe

if [ -z "$1" -o "$1" = "latest" -o "$1" = "alpha" ]; then
  DEPLOYTOOLS_VERSION=""
else
  DEPLOYTOOLS_VERSION="==$1"
fi
rm -f /opt/nameless/instance-data.json

OS_TYPE=$(source /etc/os-release; echo ${ID})
if [ "$OS_TYPE" = "ubuntu" ]; then
  export LC_ALL="en_US.UTF-8"
  export LC_CTYPE="en_US.UTF-8"
  locale-gen --purge en_US.UTF-8
  echo -e 'LANG="en_US.UTF-8"\nLANGUAGE="en_US:en"\n' > /etc/default/locale
fi
python -m pip install -U pip --ignore-installed
pip install -U setuptools awscli boto3
# If alpha, get first all non-alpha dependencies
pip install -U "nameless-deploy-tools$DEPLOYTOOLS_VERSION"
if [ "$1" = "alpha" ]; then
  # Upgrade just ndt to alpha
  pip install -U --pre --no-deps "nameless-deploy-tools"
fi
aws configure set default.s3.signature_version s3v4
rm -f /opt/nameless/instance-data.json
# Make sure we get logging
if ! grep cloud-init-output.log /etc/cloud/cloud.cfg.d/05_logging.cfg > /dev/null ; then
  echo "output: {all: '| tee -a /var/log/cloud-init-output.log'}" >> /etc/cloud/cloud.cfg.d/05_logging.cfg
fi
source $(n-include common_tools.sh)
