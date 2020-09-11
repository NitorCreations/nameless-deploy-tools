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

check_parameters () {
  fail=0
  for param ; do
    if ! eval echo \"\$\{"${param}"\}\" | grep -q . ; then
      echo "Missing parameter: $param"
      fail=1
    fi
  done
  if [ "$fail" = "1" ]; then
    exit 1
  fi
}

system_type() {
  (source /etc/os-release; echo $ID)
}

system_like() {
  source /etc/os-release
  [[ "$ID_LIKE"  =~ $1 ]]
}

system_type_and_version() {
  (source /etc/os-release; echo ${ID}_$VERSION_ID)
}

set_timezone() {
  # Timezone (based on http://askubuntu.com/a/623299 )
  if [ -z "$tz" ]; then
    tz=Europe/Helsinki
  fi
  ln -snf ../usr/share/zoneinfo/$tz /etc/localtime
  [ ! -e /etc/timezone ] || echo $tz > /etc/timezone
}
# Set aws-cli region to the region of the current instance
set_region() {
  [ "${REGION}" -o ! "${CF_AWS__Region}" ] || REGION="${CF_AWS__Region}"
  [ "${REGION}" ] || REGION=$(curl -s --connect-timeout 3 http://169.254.169.254/latest/dynamic/instance-identity/document|grep region|awk -F\" '{print $4}')
  aws configure set default.region $REGION
}

set_hostname() {
  if [ -n "${CF_paramDnsName}" ]; then
    hostname ${CF_paramDnsName}
    echo "${CF_paramDnsName}" > /etc/hostname
  fi
}
allow_cloud_init_firewall_cmd() {
  local SOURCE=$(n-include cloud-init-firewall-cmd.te)
  local BASE=${SOURCE%.te}
  local MODULE=$BASE.mod
  local PACKAGE=$BASE.pp
  checkmodule -M -m -o $MODULE $SOURCE
  semodule_package -o $PACKAGE -m $MODULE
  semodule -i $PACKAGE
}
allow_authorizedkeyscommand() {
  if system_like rhel; then
    yum update -y selinux-policy*
  elif system_like debian; then
    apt install -y selinux-policy-default
  fi
  local SOURCE=$(n-include ssh-authorized-keys-command.te)
  local BASE=${SOURCE%.te}
  local MODULE=$BASE.mod
  local PACKAGE=$BASE.pp
  checkmodule -M -m -o $MODULE $SOURCE
  semodule_package -o $PACKAGE -m $MODULE
  semodule -i $PACKAGE
}
safe_download() {
  url="$1"
  csum="$2"
  out="$3"

  wget --no-verbose --output-document="$out" "$url"
  echo "$csum  $out" | sha256sum --check
}
wait_background_jobs() {
  for i in $(jobs -p); do
    wait $i
  done
}
SYSTEM_TYPE=$(system_type)
