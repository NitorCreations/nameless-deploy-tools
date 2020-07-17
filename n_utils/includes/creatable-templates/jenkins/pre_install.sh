#!/bin/bash -ex

yum install -y https://rpm.nodesource.com/pub_8.x/el/7/x86_64/nodesource-release-el7-1.noarch.rpm
curl http://pkg.jenkins-ci.org/redhat-stable/jenkins.repo > /etc/yum.repos.d/jenkins.repo
rpm --import http://pkg.jenkins-ci.org/redhat-stable/jenkins-ci.org.key
yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo