#!/bin/bash -x

CF_AWS__StackName=
CF_AWS__Region=
CF_paramAmiName=
CF_paramAdditionalFiles=
CF_paramAmi=
CF_paramDeployToolsVersion=
CF_paramDnsName=
CF_paramEip=
CF_paramEBSTag=
CF_paramEBSSize=32
CF_extraScanHosts=`#optional`
CF_paramMvnDeployId=`#optional`
CF_paramHostedZoneName=
CF_paramDockerEBSTag=docker
CF_paramDockerEBSSize=10

export HOME=/root
cd $HOME

source $(n-include cloud_init_functions.sh)
source $(n-include tool_installers.sh)

source $(n-include aws_tools.sh)
source $(n-include ebs-functions.sh)
source $(n-include jenkins_tools.sh)
source $(n-include ssh_tools.sh)
source $(n-include apache_tools.sh)
source $(n-include ssh_tools.sh)

fail () {
    echo "FAIL: $@"
    exit 1
}
usermod -s /bin/bash jenkins
set_region
aws_install_metadata_files
set_timezone
set_hostname

apache_replace_domain_vars
apache_install_certs

jenkins_setup

apache_enable_and_start_service

jenkins_wait_service_up

MOUNT_PATH=/var/lib/docker/devicemapper
ndt volume-from-snapshot ${CF_paramDockerEBSTag} ${CF_paramDockerEBSTag} $MOUNT_PATH ${CF_paramDockerEBSSize}
cat > /etc/cron.d/${CF_paramDockerEBSTag}-snapshot << MARKER
SHELL=/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin:/root/bin

30 * * * * root ndt snapshot-from-volume -w ${CF_paramDockerEBSTag} ${CF_paramDockerEBSTag} $MOUNT_PATH >> /var/log/snapshots.log 2>&1
MARKER

systemctl enable docker
systemctl start docker

ssh_install_hostkeys
ssh_restart_service

aws_ec2_associate_address

source $(n-include cloud_init_footer.sh)
