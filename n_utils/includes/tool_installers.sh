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
  MAVEN_VERSION=3.9.0
fi
if [ -z "$PHANTOMJS_VERSION" ]; then
  PHANTOMJS_VERSION=2.1.1
fi
if [ -z "$NEXUS_VERSION" ]; then
  NEXUS_VERSION=2.15.1-02
fi
if [ -z "$NEXUS3_VERSION" ]; then
  NEXUS3_VERSION=3.47.1-01
fi
if [ -z "$CARGO_PLUGIN_VERSION" ]; then
  CARGO_PLUGIN_VERSION=0.0.6
fi
if [ -z "$ONEAGENT_VERSION" ]; then
  ONEAGENT_VERSION=1.215.163
fi
if [ -z "$ACTIVEGATE_VERSION" ]; then
  ACTIVEGATE_VERSION=1.215.163
fi
if [ -z "$FLUTTER_VERSION" ]; then
  FLUTTER_VERSION=3.7.3
  FLUTTER_CSUM=7b3d2900ce0e367d73d85591d5d43a11f94a223278dd3220776b03a83e234865
fi
if [ -z "$LEIN_COMMIT" ]; then
  LEIN_COMMIT=64e02a842e7bb50edc9b8b35de1e2ef1fac090dd # 2.10.0
fi
if [ -z "$GITHUB_RUNNER_VERSION" ]; then
  GITHUB_RUNNER_VERSION=2.303.0
  GITHUB_RUNNER_CSUM=e4a9fb7269c1a156eb5d5369232d0cd62e06bec2fd2b321600e85ac914a9cc73
fi
if [ -z "$RUSTUP_INIT_CSUM" ]; then
  RUSTUP_INIT_CSUM=bb31eaf643926b2ee9f4d8d6fc0e2835e03c0a60f34d324048aa194f0b29a71c
fi

# Make sure we get logging
if ! grep cloud-init-output.log /etc/cloud/cloud.cfg.d/05_logging.cfg > /dev/null; then
  echo "output: {all: '| tee -a /var/log/cloud-init-output.log'}" >> /etc/cloud/cloud.cfg.d/05_logging.cfg
fi

install_lein() {
  wget -O /usr/bin/lein https://codeberg.org/leiningen/leiningen/raw/commit/$LEIN_COMMIT/bin/lein
  chmod 755 /usr/bin/lein
}

install_phantomjs() {
  echo "############################################################################"
  echo " PHANTOMJS IS DEPRECATED AND INSTALLATION IS NO LONGER SUPPORTED BY DEFAULT"
  echo " IF YOU STILL NEED IT AND CANNOT MIGRATE TO E.G. HEADLESS CHROME AND YOU"
  echo " UNDERSTAND THE IMPLICATIONS IF RUNNING OBSOLETE BROWSER SOFTWARE, YOU CAN"
  echo " CHANGE install_phantomjs TO install_phantomjs_insecure"
  echo " REMOVING PHANTOMJS IS STRONGLY RECOMMENDED HOWEVER."
  echo "############################################################################"

}

install_phantomjs_insecure() {
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
  if python --version | grep -q "Python 3"; then
    wget -O - https://s3.amazonaws.com/cloudformation-examples/aws-cfn-bootstrap-py3-latest.tar.gz | tar -xzvf -
  else
    wget -O - https://s3.amazonaws.com/cloudformation-examples/aws-cfn-bootstrap-latest.tar.gz | tar -xzvf -
  fi
  pushd aws-cfn-bootstrap-*
  pip install --disable-pip-version-check .
  popd
}

install_maven() {
  source $(n-include common_tools.sh)
  add_gpg_key 29BEA2A645F2D6CED7FB12E02B172E3E156466E8
  gpg_safe_download https://archive.apache.org/dist/maven/maven-3/$MAVEN_VERSION/binaries/apache-maven-$MAVEN_VERSION-bin.tar.gz maven.tar.gz asc
  tar -xzvf maven.tar.gz -C /opt/
  rm maven.tar.gz
  ln -snf /opt/apache-maven-$MAVEN_VERSION /opt/maven
  ln -snf /opt/maven/bin/mvn /usr/bin/mvn
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
  source $(n-include common_tools.sh)
  add_gpg_key 0374CF2E8DD1BDFD
  gpg_safe_download https://sonatype-download.global.ssl.fastly.net/repository/downloads-prod-group/3/nexus-$NEXUS3_VERSION-unix.tar.gz nexus3.tar.gz asc
  mkdir -p /opt/nexus
  tar -xzf nexus3.tar.gz -C /opt/nexus
  chown -R nexus:nexus /opt/nexus
  rm -f nexus3.tar.gz nexus3.tar.gz.sig
  ln -snf /opt/nexus/nexus-* /opt/nexus/current
  mkdir -p /opt/nexus/sonatype-work
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

install_nexus3_cargo_plugin() {
  add_gpg_key 80900DA1952D7C7968F3CFD98C79C4D0382A0E3A
  gpg_safe_download https://repo1.maven.org/maven2/org/sonatype/nexus/plugins/nexus-repository-cargo/$CARGO_PLUGIN_VERSION/nexus-repository-cargo-$CARGO_PLUGIN_VERSION.jar nexus-repository-cargo-$CARGO_PLUGIN_VERSION.jar asc
  mkdir -p /opt/nexus/current/system/org/sonatype/nexus/plugins/nexus-repository-cargo/$CARGO_PLUGIN_VERSION/
  mv nexus-repository-cargo-$CARGO_PLUGIN_VERSION.jar /opt/nexus/current/system/org/sonatype/nexus/plugins/nexus-repository-cargo/$CARGO_PLUGIN_VERSION/

  cat >> diff.xml << MARKER
<diff xmlns:krf="http://karaf.apache.org/xmlns/features/v1.6.0">
  <add sel="//krf:feature[@name='nexus-core-feature']">    <krf:feature prerequisite="false" dependency="false">nexus-repository-cargo</krf:feature>
    </add>
  <add sel="//krf:feature[@name='nexus-repository-maven']" pos="after">
    <krf:feature name="nexus-repository-cargo" description="org.sonatype.nexus.plugins:nexus-repository-cargo" version="$CARGO_PLUGIN_VERSION">
        <krf:details>org.sonatype.nexus.plugins:nexus-repository-cargo</krf:details>
        <krf:bundle>mvn:org.sonatype.nexus.plugins/nexus-repository-cargo/$CARGO_PLUGIN_VERSION</krf:bundle>
    </krf:feature></add>
</diff>
MARKER
  add_gpg_key 379CE192D401AB61
  gpg_safe_download https://search.maven.org/remotecontent?filepath=com/github/dnault/xml-patch/0.3.1/xml-patch-0.3.1.jar xml-patch.jar asc
  java -jar xml-patch.jar /opt/nexus/current/system/org/sonatype/nexus/assemblies/nexus-core-feature/*/nexus-core-feature-*-features.xml diff.xml temp.xml
  mv -f temp.xml /opt/nexus/current/system/org/sonatype/nexus/assemblies/nexus-core-feature/*/nexus-core-feature-*-features.xml
  chown nexus:nexus /opt/nexus/current/system/org/sonatype/nexus/assemblies/nexus-core-feature/*/nexus-core-feature-*-features.xml
  rm -f xml-patch.jar diff.xml
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

update_deploytools() {
  if [ ! "$DEPLOYTOOLS_VERSION" ]; then
    echo "Specific version not defined - updating to latest"
    DEPLOYTOOLS_VERSION="latest"
  fi
  echo "Updating nameless-deploy-tools to $DEPLOYTOOLS_VERSION"
  bash "$(n-include install_tools.sh)" "${DEPLOYTOOLS_VERSION}"
}

update_aws_utils() {
  echo "###########################"
  echo "#        DEPRECATED       #"
  echo "###########################"
  echo "Updating ndt as part of a bootup is no longer recommended"
  update_deploytools "$@"
}

install_dynatrace_oneagent() {
  # Requires secrets dynatrace.apikey and dt-root.cert.pem (from dynatrace web installation instructions) to be stored in secrets storage
  wget -O Dynatrace-OneAgent-Linux-$ONEAGENT_VERSION.sh \
    "https://bmq38893.live.dynatrace.com/api/v1/deployment/installer/agent/unix/default/latest?arch=x86&flavor=default" \
    --header="Authorization: Api-Token $(fetch-secrets.sh show dynatrace.apikey)"

  fetch-secrets.sh get 400 dt-root.cert.pem
  (
    echo 'Content-Type: multipart/signed; protocol="application/x-pkcs7-signature"; micalg="sha-256"; boundary="--SIGNED-INSTALLER"'
    echo
    echo
    echo '----SIGNED-INSTALLER'
    cat Dynatrace-OneAgent-Linux-$ONEAGENT_VERSION.sh
  ) | openssl cms -verify -CAfile dt-root.cert.pem > /dev/null
  rm -f dt-root.cert.pem

  /bin/sh Dynatrace-OneAgent-Linux-$ONEAGENT_VERSION.sh
  rm -f Dynatrace-OneAgent-Linux-$ONEAGENT_VERSION.sh
}

install_dynatrace_activegate() {
  # Requires secrets dynatrace.apikey and dt-root.cert.pem (from dynatrace web installation instructions) to be stored in secrets storage
  wget -O Dynatrace-ActiveGate-Linux-x86-$ACTIVEGATE_VERSION.sh \
    "https://bmq38893.live.dynatrace.com/api/v1/deployment/installer/gateway/unix/latest?arch=x86&flavor=default" \
    --header="Authorization: Api-Token $(fetch-secrets.sh show dynatrace.apikey)"

  fetch-secrets.sh get 400 dt-root.cert.pem
  (
    echo 'Content-Type: multipart/signed; protocol="application/x-pkcs7-signature"; micalg="sha-256"; boundary="--SIGNED-INSTALLER"'
    echo
    echo
    echo '----SIGNED-INSTALLER'
    cat Dynatrace-ActiveGate-Linux-x86-$ACTIVEGATE_VERSION.sh
  ) | openssl cms -verify -CAfile dt-root.cert.pem > /dev/null
  rm -f dt-root.cert.pem

  /bin/sh Dynatrace-ActiveGate-Linux-x86-$ACTIVEGATE_VERSION.sh
  rm -f Dynatrace-ActiveGate-Linux-x86-$ACTIVEGATE_VERSION.sh
}

enable_systemd_portforward() {
  local SOURCE=$(n-include systemd-portforward.te)
  local BASE=${SOURCE%.te}
  local MODULE=$BASE.mod
  local PACKAGE=$BASE.pp
  checkmodule -M -m -o $MODULE $SOURCE
  semodule_package -o $PACKAGE -m $MODULE
  semodule -i $PACKAGE
}

install_androidsdk() {
  source $(n-include common_tools.sh)
  safe_download https://dl.google.com/android/repository/commandlinetools-linux-8512546_latest.zip 2ccbda4302db862a28ada25aa7425d99dce9462046003c1714b059b5c47970d8 commandlinetools-linux_latest.zip
  safe_download https://dl.google.com/android/repository/platform-tools_r33.0.2-linux.zip defcee9da1f22fe5c2324ec0edf612122f1c6ffe01a7b124191e07fcc74f8fff platform-tools-linux.zip
  mkdir /opt/android
  unzip -d /opt/android commandlinetools-linux_latest.zip
  unzip -d /opt/android platform-tools-linux.zip
  rm -f commandlinetools-linux_latest.zip platform-tools-linux.zip
  mkdir /opt/android/cmdline-tools/latest
  mv /opt/android/cmdline-tools/* /opt/android/cmdline-tools/latest || :
  cat > /etc/profile.d/android.sh << MARKER
export PATH="\$PATH:/opt/android/platform-tools:/opt/android/cmdline-tools/latest/bin"
MARKER
  chmod 755 /etc/profile.d/android.sh
  source /etc/profile.d/android.sh
  yes | sdkmanager --sdk_root=/opt/android "platform-tools" "platforms;android-31" "platforms;android-30" "platforms;android-29" "emulator" "build-tools;33.0.0"
  yes | sdkmanager --sdk_root=/opt/android --licenses
}

install_flutter() {
  source $(n-include common_tools.sh)
  safe_download https://storage.googleapis.com/flutter_infra_release/releases/stable/linux/flutter_linux_$FLUTTER_VERSION-stable.tar.xz $FLUTTER_CSUM flutter_linux-stable.tar.xz
  tar -xJvf flutter_linux-stable.tar.xz -C /opt/
  rm -f flutter_linux-stable.tar.xz
  cat > /etc/profile.d/flutter.sh << MARKER
export PATH="\$PATH:/opt/flutter/bin"
MARKER
  chmod 755 /etc/profile.d/flutter.sh
  source /etc/profile.d/flutter.sh
  flutter precache
  yes | flutter doctor --android-licenses
}

install_rust_toolchain() {
  # https://rustup.rs/
  # https://forge.rust-lang.org/infra/other-installation-methods.html#rustup
  source $(n-include common_tools.sh)
  local URL
  local FILE
  URL="https://static.rust-lang.org/rustup/dist/x86_64-unknown-linux-gnu/rustup-init"
  FILE="$(basename "$URL")"
  safe_download "$URL" "$RUSTUP_INIT_CSUM" "$FILE"
  ./"$FILE" -y
  source "$HOME/.cargo/env"
  "$HOME/.cargo/bin/rustup" --version
  "$HOME/.cargo/bin/rustup" update
  "$HOME/.cargo/bin/rustc" --version
  "$HOME/.cargo/bin/rustup" component add rustfmt
  "$HOME/.cargo/bin/rustup" component add clippy
  rm -f "$FILE"
}

install_github_actions_runner() {
  source $(n-include common_tools.sh)
  mkdir /opt/github-runner
  local URL
  local FILE
  URL="https://github.com/actions/runner/releases/download/v$GITHUB_RUNNER_VERSION/actions-runner-linux-x64-$GITHUB_RUNNER_VERSION.tar.gz"
  FILE="$(basename "$URL")"
  safe_download "$URL" "$GITHUB_RUNNER_CSUM" "$FILE"
  tar -xzvf "$FILE" -C /opt/github-runner
  rm -f "$FILE"
  /opt/github-runner/bin/installdependencies.sh
}

start_github_actions_runner() {
  local LOCAL_USER=$1
  local URL_TARGET=$2
  local TOKEN=$3
  chown -R "$LOCAL_USER" /opt/github-runner
  pushd /opt/github-runner
  sudo -u "$LOCAL_USER" bash -c "./config.sh --unattended --url $URL_TARGET --token $TOKEN --replace"
  /opt/github-runner/svc.sh install "$LOCAL_USER"
  /opt/github-runner/svc.sh start
  popd
}

# requires PAT-TOKEN with write-access to org self hosted runner endpoints
# https://docs.github.com/en/rest/overview/permissions-required-for-fine-grained-personal-access-tokens?apiVersion=2022-11-28#organization-self-hosted-runners
# NOTE: create a fine-grained solely for this purpose
github_actions_get_create_token() {
  local PAT_TOKEN=$1
  local ORGANIZATION=$2
  curl -sL \
    -X POST \
    -H "Accept: application/vnd.github+json" \
    -H "Authorization: Bearer $PAT_TOKEN" \
    -H "X-GitHub-Api-Version: 2022-11-28" \
    https://api.github.com/orgs/$ORGANIZATION/actions/runners/registration-token | jq -r .token
}
