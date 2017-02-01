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

# Functions to install various tools meant to be sourced and used as Functions
if [ -z "$DEPLOYTOOLS_VERSION" ]; then
  if [ -n "${CF_paramDeployToolsVersion}" ]; then
    DEPLOYTOOLS_VERSION="${CF_paramDeployToolsVersion}"
  fi
fi
if [ -z "$MAVEN_VERSION" ]; then
  MAVEN_VERSION=3.3.9
fi
if [ -z "$PHANTOMJS_VERSION" ]; then
  PHANTOMJS_VERSION=2.1.1
fi
if [ -z "$NEXUS_VERSION" ]; then
  NEXUS_VERSION=2.12.0-01
fi

install_lein() {
  wget -O /usr/bin/lein https://raw.githubusercontent.com/technomancy/leiningen/stable/bin/lein
  chmod 755 /usr/bin/lein
}
install_phantomjs() {
  wget -O - https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-$PHANTOMJS_VERSION-linux-x86_64.tar.bz2 | tar -xjvf -
  mv phantomjs-*/bin/phantomjs /usr/bin
  rm -rf phantomjs-*
}
install_yarn() {
  mkdir /opt/yarn
  # The tarball unpacks to dist/, we strip that out
  wget -O - https://yarnpkg.com/latest.tar.gz | tar --strip-components=1 -C /opt/yarn -xzv
}
install_cftools() {
  curl -s https://s3.amazonaws.com/cloudformation-examples/aws-cfn-bootstrap-latest.tar.gz | tar -xzvf -
  cd aws-cfn-bootstrap-*
  pip install .
  cd ..
}
install_maven() {
  wget -O - http://mirror.netinch.com/pub/apache/maven/maven-3/$MAVEN_VERSION/binaries/apache-maven-$MAVEN_VERSION-bin.tar.gz | tar -xzvf - -C /opt/
  ln -snf /opt/apache-maven-$MAVEN_VERSION /opt/maven
  ln -snf  /opt/maven/bin/mvn /usr/bin/mvn
}
install_nexus() {
  wget -O - https://sonatype-download.global.ssl.fastly.net/nexus/oss/nexus-$NEXUS_VERSION-bundle.tar.gz | tar -xzf - -C /opt/nexus
  chown -R nexus:nexus /opt/nexus
  ln -snf /opt/nexus/nexus-* /opt/nexus/current
  cat > /usr/lib/systemd/system/nexus.service << MARKER
[Unit]
Description=Sonatype Nexus

[Service]
Type=forking
User=nexus
PIDFile=/opt/nexus/current/bin/jsw/linux-x86-64/nexus.pid
ExecStart=/opt/nexus/current/bin/nexus start
ExecReload=/opt/nexus/current/bin/nexus restart
ExecStop=/opt/nexus/current/bin/nexus stop

[Install]
Alias=nexus
WantedBy=default.target
MARKER
  sed -i 's/nexus-webapp-context-path=.*/nexus-webapp-context-path=\//' /opt/nexus/current/conf/nexus.properties
}
install_fail2ban() {
  yum update -y selinux-policy*
  cat > /etc/fail2ban/jail.d/sshd.local << MARKER
[sshd]
enabled = true
port = ssh
logpath = %(sshd_log)s
maxretry = 5
bantime = 86400
MARKER
  systemctl enable fail2ban
  systemctl start fail2ban
}
update_deploytools() {
  if [ ! "$DEPLOYTOOLS_VERSION" ]; then
    echo "Specific version not defined - updating to latest"
    DEPLOYTOOLS_VERSION="latest"
  fi
  echo "Updating nitor-deploy-tools to $DEPLOYTOOLS_VERSION"
  bash "$(dirname "${BASH_SOURCE[0]}")/install_tools.sh" "${DEPLOYTOOLS_VERSION}"
}
update_aws_utils () {
  update_deploytools "$@"
}
