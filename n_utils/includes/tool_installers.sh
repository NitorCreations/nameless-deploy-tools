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

# Make sure we get logging
if ! grep cloud-init-output.log /etc/cloud/cloud.cfg.d/05_logging.cfg > /dev/null ; then
  echo "output: {all: '| tee -a /var/log/cloud-init-output.log'}" >> /etc/cloud/cloud.cfg.d/05_logging.cfg
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
install_nexus3() {
  wget -O - https://sonatype-download.global.ssl.fastly.net/repository/repositoryManager/3/nexus-$NEXUS3_VERSION-unix.tar.gz | tar -xzf - -C /opt/nexus
  chown -R nexus:nexus /opt/nexus
  ln -snf /opt/nexus/nexus-* /opt/nexus/current
  mv /opt/nexus/sonatype-work /opt/nexus/sonatype-work-initial
  cat > /usr/lib/systemd/system/nexus.service << MARKER
[Unit]
Description=Sonatype Nexus

[Service]
Type=simple
User=nexus
LimitNOFILE=65536
ExecStart=/opt/nexus/current/bin/nexus run

[Install]
Alias=nexus
WantedBy=default.target
MARKER
}
install_fail2ban() {
  yum update -y selinux-policy*
  mkdir -p /var/run/fail2ban
  local SOURCE=$(n-include fail2ban-rundir.te)
  local BASE=${SOURCE%.te}
  local MODULE=$BASE.mod
  local PACKAGE=$BASE.pp
  checkmodule -M -m -o $MODULE $SOURCE
  semodule_package -o $PACKAGE -m $MODULE
  semodule -i $PACKAGE
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
allow_authorizedkeyscommand() {
  yum update -y selinux-policy*
  local SOURCE=$(n-include ssh-authorized-keys-command.te)
  local BASE=${SOURCE%.te}
  local MODULE=$BASE.mod
  local PACKAGE=$BASE.pp
  checkmodule -M -m -o $MODULE $SOURCE
  semodule_package -o $PACKAGE -m $MODULE
  semodule -i $PACKAGE
}
update_deploytools() {
  if [ ! "$DEPLOYTOOLS_VERSION" ]; then
    echo "Specific version not defined - updating to latest"
    DEPLOYTOOLS_VERSION="latest"
  fi
  echo "Updating nameless-deploy-tools to $DEPLOYTOOLS_VERSION"
  bash "$(n-include install_tools.sh)" "${DEPLOYTOOLS_VERSION}"
}
update_aws_utils () {
  echo "###########################"
  echo "#        DEPRECATED       #"
  echo "###########################"
  echo "Updating ndt as part of a bootup is no longer recommended"
  update_deploytools "$@"
}

install_nexus3_aptrepository() {
  INST_DIR=/opt/nexus/current/system/net/staticsnow/nexus-repository-apt/$NEXUS_REPOSITORY_APT_VERSION/
  mkdir -p $INST_DIR
  FILE=nexus-repository-apt-$NEXUS_REPOSITORY_APT_VERSION.jar
  wget -O $INST_DIR/$FILE https://github.com/freelancer/nexus-repository-apt/releases/download/$NEXUS_REPOSITORY_APT_VERSION/$FILE
  chown -R nexus:nexus /opt/nexus/current/system/net/
  FEATURES_FILE=/opt/nexus/current/system/org/sonatype/nexus/assemblies/nexus-core-feature/$NEXUS3_VERSION/nexus-core-feature-$NEXUS3_VERSION-features.xml
  sed -i '/>nexus-repository-maven/a \ \ \ \ \ \ \ \ <feature prerequisite="false" dependency="false">nexus-repository-apt</feature>' "$FEATURES_FILE"
  sed -i "/feature name=\"nexus-repository-maven\"/i  <feature name=\"nexus-repository-apt\" description=\"net.staticsnow:nexus-repository-apt\" version=\"$NEXUS_REPOSITORY_APT_VERSION\">\n  <details>net.staticsnow:nexus-repository-apt</details>\n  <bundle>mvn:net.staticsnow/nexus-repository-apt/$NEXUS_REPOSITORY_APT_VERSION</bundle>\n  <bundle>mvn:org.tukaani/xz/1.8</bundle>\n</feature>\n" "$FEATURES_FILE"
}
