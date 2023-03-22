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

OS_TYPE=$(
  source /etc/os-release
  echo ${ID}
)
OS_VERSION=$(
  source /etc/os-release
  echo ${VERSION_ID}
)
if [ "$OS_TYPE" = "ubuntu" ]; then
  export LC_ALL="en_US.UTF-8"
  export LC_CTYPE="en_US.UTF-8"
  locale-gen --purge en_US.UTF-8
  echo -e 'LANG="en_US.UTF-8"\nLANGUAGE="en_US:en"\n' > /etc/default/locale
fi


add_gpg_key() {
  local key=$1
    gpg --batch --keyserver hkps://keyserver.ubuntu.com:443 --recv-keys "$key" ||
    gpg --batch --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys "$key" ||
    gpg --batch --keyserver hkps://keys.openpgp.org --recv-keys "$key"
}

gpg_safe_download() {
  local URL=$1
  local DST=$2
  local SIG_SUFFIX=${3:-sig}
  if python --version | grep "Python 2" > /dev/null; then
    python -c "from urllib import urlretrieve; urlretrieve('$URL', '$DST')"
    python -c "from urllib import urlretrieve; urlretrieve('$URL.$SIG_SUFFIX', '$DST.sig')"
  else
    python -c "from urllib.request import urlretrieve; urlretrieve('$URL', '$DST')"
    python -c "from urllib.request import urlretrieve; urlretrieve('$URL.$SIG_SUFFIX', '$DST.sig')"
  fi
  gpg --verify $DST.sig $DST
}

install_awscliv2() {
  AWS_CLI_INSTALL_DIR=$(mktemp -d)
  ZIP_DST="$AWS_CLI_INSTALL_DIR"/awscliv2.zip
  add_gpg_key A6310ACC4672475C
  if uname -a | grep -e "x86_64" -e "amd64" > /dev/null; then
    if ! gpg_safe_download "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" "$ZIP_DST"; then
      rm -rf "$AWS_CLI_INSTALL_DIR"
      echo "ERROR: failed to download of awscliv2.zip" && return 1
    fi
  elif uname -a | grep "aarch64" > /dev/null; then
    if ! gpg_safe_download "https://awscli.amazonaws.com/awscli-exe-linux-aarch64.zip" "$ZIP_DST"; then
      rm -rf "$AWS_CLI_INSTALL_DIR"
      echo "ERROR: failed to download of awscliv2.zip" && return 1
    fi
  else
    echo "ERROR: Processor type is unsupported." && return 1
  fi

  unzip -qo "$ZIP_DST" -d "$AWS_CLI_INSTALL_DIR"
  if [ $? -ne 0 ]; then
    rm -rf "$AWS_CLI_INSTALL_DIR"
    echo "ERROR: failed to unzip of awscliv2.zip" && return 1
  fi
  "$AWS_CLI_INSTALL_DIR"/aws/install -u
  if [ $? -ne 0 ]; then
    rm -rf "$AWS_CLI_INSTALL_DIR"
    echo "ERROR: aws cli install failure" && return 1
  fi
  rm -rf "$AWS_CLI_INSTALL_DIR"
  return 0
}

python -m pip install --disable-pip-version-check -U pip wheel --ignore-installed
install_awscliv2
# Setuptools installed with pip breaks the platform python setup on CentOS 8
if [ "$OS_TYPE" = "centos" -a "$OS_VERSION" = "8" ]; then
  pip install --disable-pip-version-check -U boto3
else
  pip install --disable-pip-version-check -U boto3 setuptools
fi
# If alpha, get first all non-alpha dependencies
pip install --disable-pip-version-check -U "nameless-deploy-tools$DEPLOYTOOLS_VERSION" --ignore-installed
if [ "$1" = "alpha" ]; then
  # Upgrade just ndt to alpha
  pip install --disable-pip-version-check -U --pre --no-deps "nameless-deploy-tools" --ignore-installed
fi
aws configure set default.s3.signature_version s3v4
rm -f /opt/nameless/instance-data.json
# Make sure we get logging
if ! grep cloud-init-output.log /etc/cloud/cloud.cfg.d/05_logging.cfg > /dev/null; then
  echo "output: {all: '| tee -a /var/log/cloud-init-output.log'}" >> /etc/cloud/cloud.cfg.d/05_logging.cfg
fi
