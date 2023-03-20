#!/bin/bash -ex

source $(n-include tool_installers.sh)
source $(n-include apache_tools.sh)
setup-fetch-secrets.sh vault

pip install ansible pywinrm pylint wmi s3cmd

npm i --no-update-notifier --no-fund --no-audit -g gulp browserify jshint

install_cftools
install_lein
install_maven
install_fail2ban
sed -i '/Defaults\s*requiretty/d' /etc/sudoers

$(n-include get-docker.sh)

# Disable apache & jenkins before certs & conf are there
systemctl start jenkins

while ! wget -qO jenkins-cli.jar http://localhost:8080/jnlpJars/jenkins-cli.jar; do
  echo "Retrying fetch jenkins-cli.jar"
  sleep 2
done
set +x
ADMIN_AUTH=$(cat /var/lib/jenkins/secrets/initialAdminPassword)
for PLUGIN in ansicolor cron_column extensible-choice-parameter extra-columns git \
  git-client git-server greenballs job-dsl mailer next-build-number parameterized-trigger \
  pipeline-input-step progress-bar-column-plugin rebuild script-security simple-theme-plugin; do
  java -jar jenkins-cli.jar -s http://localhost:8080/ -auth "admin:$ADMIN_AUTH" install-plugin $PLUGIN -deploy
done
set -x
systemctl disable jenkins
systemctl disable httpd
systemctl disable docker || :
systemctl stop jenkins || :
systemctl stop httpd || :
systemctl stop docker || :

groupadd -aG docker jenkins

apache_prepare_ssl_conf
# Move jenkins installation away from default location & configure jenkins user
mv /var/lib/jenkins /var/lib/jenkins-default
mkdir --mode=755 /var/lib/jenkins
chown -R jenkins:jenkins /var/lib/jenkins

allow_cloud_init_firewall_cmd
