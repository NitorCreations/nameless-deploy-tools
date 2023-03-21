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

source "$(dirname "${BASH_SOURCE[0]}")/common_tools.sh"

ssh_install_hostkeys() {
  check_parameters CF_paramDnsName
  fetch-secrets.sh get 500 --optional /etc/ssh/${CF_paramDnsName}-ssh-hostkeys.sh
  if [ -x /etc/ssh/${CF_paramDnsName}-ssh-hostkeys.sh ]; then
    sleep 2
    source /etc/ssh/${CF_paramDnsName}-ssh-hostkeys.sh
    # ssh is restarted later in the userdata script when elastic ip has been associated
    chmod 600 /etc/ssh/ssh_host_*_key
  fi
}

ssh_restart_service() {
  sed -i 's/^#PermitRootLogin.*$/PermitRootLogin no/g' /etc/ssh/sshd_config
  case "$SYSTEM_TYPE" in
    ubuntu)
      service ssh restart
      ;;
    centos | rhel | rocky | fedora)
      systemctl restart sshd
      ;;
    *)
      echo "Unknown system type $SYSTEM_TYPE"
      exit 1
      ;;
  esac
}
