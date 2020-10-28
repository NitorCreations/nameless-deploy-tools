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

jenkins_setup_dotssh () {
  check_parameters CF_paramDnsName
  DOT_SSH_DIR=/var/lib/jenkins/jenkins-home/.ssh
  mkdir -p $DOT_SSH_DIR
  chmod 700 $DOT_SSH_DIR
  fetch-secrets.sh get 600 $DOT_SSH_DIR/${CF_paramDnsName}.rsa
  mv -v $DOT_SSH_DIR/${CF_paramDnsName}.rsa $DOT_SSH_DIR/id_rsa
  ssh-keygen -y -f $DOT_SSH_DIR/id_rsa > $DOT_SSH_DIR/id_rsa.pub
  chmod 600 $DOT_SSH_DIR/*
  for SCAN_HOST in "github.com" $CF_extraScanHosts; do
    if ! ssh-keygen -f $DOT_SSH_DIR/known_hosts -H -F "$SCAN_HOST" | grep . > /dev/null; then
      ssh-keyscan -t rsa "$SCAN_HOST" >> $DOT_SSH_DIR/known_hosts
    fi
  done
  cat > /var/lib/jenkins/jenkins-home/.gitconfig << MARKER
[user]
	email = jenkins@${CF_paramDnsName}
	name = Jenkins
[push]
	default = simple
[branch]
	autosetuprebase = always
[pull]
	rebase = true
MARKER
  if [ -n "$CF_paramMvnDeployId" ]; then
    [ -n "$MAVEN_HOME" ] || MAVEN_HOME=/var/lib/jenkins/jenkins-home/.m2
    mkdir -p "$MAVEN_HOME"
    chmod 700 "$MAVEN_HOME"
    if ! [ -r "$MAVEN_HOME/settings-security.xml" ]; then
      if [ "$(set -o | grep xtrace | awk '{ print $2 }')" = "on" ]; then
        set +x
        RESET_XTRACE="true"
      fi
      MASTER_PWD=$(mvn -emp "$(cat /dev/urandom | tr -cd [:alnum:] | head -c 12)")
      cat > "$MAVEN_HOME/settings-security.xml" << MARKER
<settingsSecurity>
  <master>$MASTER_PWD</master>
</settingsSecurity>
MARKER
    chmod 600 "$MAVEN_HOME/settings-security.xml"
    fi
    if ! [ -r "$MAVEN_HOME/settings.xml" ]; then
      cat > "$MAVEN_HOME/settings.xml" << MARKER
<settings>
</settings>
MARKER
      chmod 600 "$MAVEN_HOME/settings.xml"
    fi
    if [ "$(set -o | grep xtrace | awk '{ print $2 }')" = "on" ]; then
      set +x
      RESET_XTRACE="true"
    fi
    DEPLOYER_PWD=$(fetch-secrets.sh show "$CF_paramMvnDeployId")
    export DEPLOYER_PASSWORD=$(sudo -iu jenkins mvn -ep "$DEPLOYER_PWD")
    ndt add-deployer-server "$MAVEN_HOME/settings.xml" "$CF_paramMvnDeployId"
    if [ "$RESET_XTRACE" ]; then
      unset RESET_XTRACE
      set -x
    fi
  fi
}

jenkins_mount_ebs_home () {
  check_parameters CF_paramEBSTag
  local SIZE=$1
  if [ -z "$SIZE" ]; then
    SIZE=32
  fi
  local MOUNT_PATH=/var/lib/jenkins/jenkins-home
  ndt volume-from-snapshot ${CF_paramEBSTag} ${CF_paramEBSTag} $MOUNT_PATH  $SIZE
  usermod -d /var/lib/jenkins/jenkins-home jenkins
  mkdir -p /var/lib/jenkins/jenkins-home
  if ! [ -e /var/lib/jenkins/jenkins-home/config.xml ]; then
    if [ -e /var/lib/jenkins-default/config.xml ]; then
      cp -a /var/lib/jenkins-default/* /var/lib/jenkins/jenkins-home/
    fi
  fi
  cat > /etc/cron.d/${CF_paramEBSTag}-snapshot << MARKER
SHELL=/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin:/root/bin

30 * * * * root ndt snapshot-from-volume -w ${CF_paramEBSTag} ${CF_paramEBSTag} $MOUNT_PATH >> /var/log/snapshots.log 2>&1
MARKER
}

jenkins_setup_snapshot_script () {
  if [ ! -e /var/lib/jenkins/jenkins-home/snapshot_jenkins_home.sh ]; then
    cat > /var/lib/jenkins/jenkins-home/snapshot_jenkins_home.sh << EOF
#!/bin/bash -xe

ndt snapshot-from-volume -w ${CF_paramEBSTag} ${CF_paramEBSTag} /var/lib/jenkins/jenkins-home
EOF
  fi
  chmod 755 /var/lib/jenkins/jenkins-home/snapshot_jenkins_home.sh
}

jenkins_setup_snapshot_on_shutdown () {
  # Amend service script to call snapshot_jenkins_home right after stopping the service - original script saved as jenkins.orig
  if [ "$SYSTEM_TYPE" = "ubuntu" ]; then
    perl -i.orig -e 'while(<>){print;if(m!^(\s+)do_stop!){print $1.'\''retval="$?"'\''."\n".$1."/usr/local/bin/ndt snapshot-from-volume '${CF_paramEBSTag}' '${CF_paramEBSTag}' /var/lib/jenkins/jenkins-home\n";last;}}$_=<>;s/\$\?/\$retval/;print;while(<>){print}' /etc/init.d/jenkins
  elif [ "$SYSTEM_TYPE" = "centos" -o "$SYSTEM_TYPE" = "fedora" ]; then
    perl -i.orig -e 'while(<>){print;if(m!^(\s+)killproc!){print $1.'\''retval="$?"'\''."\n".$1."/usr/local/bin/ndt snapshot-from-volume '${CF_paramEBSTag}' '${CF_paramEBSTag}' /var/lib/jenkins/jenkins-home\n";last;}}$_=<>;s/\$\?/\$retval/;print;while(<>){print}' /etc/init.d/jenkins
  else
    echo "Unkown system type $SYSTEM_TYPE"
  fi
}

jenkins_setup_snapshot_job () {
  if ! find /var/lib/jenkins/jenkins-home/jobs -name config.xml -print0 | xargs -0 fgrep -q snapshot_jenkins_home.sh ; then
    sync_jenkins_conf_job_name="snapshot-jenkins-home"
    mkdir -p /var/lib/jenkins/jenkins-home/jobs/${sync_jenkins_conf_job_name}
    cat > /var/lib/jenkins/jenkins-home/jobs/${sync_jenkins_conf_job_name}/config.xml << 'EOF'
<?xml version='1.0' encoding='UTF-8'?>
<project>
  <actions/>
  <description>Runs the &quot;snapshot_jenkins_home.sh&quot; script that pushes the latest jenkins config to the remote Jenkins repo.</description>
  <keepDependencies>false</keepDependencies>
  <properties>
    <jenkins.model.BuildDiscarderProperty>
      <strategy class="hudson.tasks.LogRotator">
        <daysToKeep>60</daysToKeep>
        <numToKeep>-1</numToKeep>
        <artifactDaysToKeep>-1</artifactDaysToKeep>
        <artifactNumToKeep>-1</artifactNumToKeep>
      </strategy>
    </jenkins.model.BuildDiscarderProperty>
  </properties>
  <scm class="hudson.scm.NullSCM"/>
  <canRoam>true</canRoam>
  <disabled>true</disabled>

  <blockBuildWhenDownstreamBuilding>false</blockBuildWhenDownstreamBuilding>
  <blockBuildWhenUpstreamBuilding>false</blockBuildWhenUpstreamBuilding>
  <triggers>
    <hudson.triggers.TimerTrigger>
      <spec>H H(18-19) * * *
H H(4-5) * * *</spec>
    </hudson.triggers.TimerTrigger>
  </triggers>
  <concurrentBuild>false</concurrentBuild>
  <builders>
    <hudson.tasks.Shell>
      <command>/var/lib/jenkins/jenkins-home/snapshot_jenkins_home.sh 2&gt;&amp;1 | tee -a /var/lib/jenkins/snapshot_jenkins_home.log</command>
    </hudson.tasks.Shell>
  </builders>
  <publishers/>
  <buildWrappers/>
</project>
EOF
  fi
}

jenkins_discard_default_install () {
  rm -rf /var/lib/jenkins-default
}

jenkins_fetch_additional_files () {
  fetch-secrets.sh get 600 ${CF_paramAdditionalFiles}
  for i in ${CF_paramAdditionalFiles} ; do
    case "$i" in
      /var/lib/jenkins/*)
	      chown -R jenkins:jenkins "$i"
	      ;;
    esac
  done
}

jenkins_improve_config_security () {
  mkdir -p /var/lib/jenkins/jenkins-home/secrets/
  echo false > /var/lib/jenkins/jenkins-home/secrets/slave-to-master-security-kill-switch
}

jenkins_set_home () {
  case "$SYSTEM_TYPE" in
    ubuntu)
      local SYSCONFIG=/etc/default/jenkins
      ;;
    centos|fedora)
      local SYSCONFIG=/etc/sysconfig/jenkins
      ;;
    *)
      echo "Unkown system type $SYSTEM_TYPE"
      exit 1
  esac
  sed -i -e 's/JENKINS_HOME=.*/JENKINS_HOME=\/var\/lib\/jenkins\/jenkins-home/g' \
  -e 's/\(JENKINS_JAVA_OPTIONS=\"[^\"]*\)\"/\1 -Dhudson.model.DirectoryBrowserSupport.CSP= -Djava.awt.headless=true -Dhudson.model.User.SECURITY_243_FULL_DEFENSE=false -Dhudson.model.ParametersAction.keepUndefinedParameters=true\"/g' \
  -e 's/^JENKINS_AJP_PORT=.*$/JENKINS_AJP_PORT="-1"/g' $SYSCONFIG
}

jenkins_disable_and_shutdown_service () {
  case "$SYSTEM_TYPE" in
    ubuntu)
      update-rc.d jenkins disable
      service jenkins stop
      ;;
    centos|fedora)
      systemctl disable jenkins
      systemctl stop jenkins
      ;;
    *)
      echo "Unkown system type $SYSTEM_TYPE"
      exit 1
  esac
}

jenkins_enable_and_start_service () {
  chown -R jenkins:jenkins /var/lib/jenkins/ /var/lib/jenkins/jenkins-home/
  systemctl enable jenkins
  systemctl start jenkins
}

jenkins_setup() {
  jenkins_mount_ebs_home ${CF_paramEBSSize}
  jenkins_discard_default_install
  jenkins_setup_dotssh
  jenkins_setup_snapshot_script
  jenkins_setup_snapshot_on_shutdown
  jenkins_setup_snapshot_job
  jenkins_improve_config_security

  jenkins_fetch_additional_files
  jenkins_set_home
  jenkins_enable_and_start_service
}

jenkins_wait_service_up () {
  # Tests to see if everything is OK
  COUNT=0
  SERVER=""
  while [ $COUNT -lt 300 ] && [ "$SERVER" != "Jenkins" ]; do
    sleep 1
    SERVER="$(curl -sv http://localhost:8080 2>&1 | grep 'X-Jenkins:' | awk -NF'-|:' '{ print $2 }')"
    COUNT=$(($COUNT + 1))
  done
  if [ "$SERVER" != "Jenkins" ]; then
    fail "Jenkins server not started"
  fi
}

