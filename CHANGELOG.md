# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)


## [Unreleased]
### Added
* Update rustup-init checksum

## [1.299] - 2023-04-24
### Fixed
* Fix nexus systemd unit file

## [1.298] - 2023-04-21
### Added
* Add rocky 9 packages

## [1.297] - 2023-04-15
### Added
* Create subdirectory for github runners to enable making that an ebs volume

## [1.296] - 2023-04-15
### Added
* Enable installing multiple github runners

## [1.293] - 2023-04-06
### Fixed
* Rust installation fix

## [1.291] - 2023-03-21
### Fixed
* Release process fix

## [1.290] - 2023-03-21
### Fixed
* Release process fix

## [1.289] - 2023-03-21
### Fixed
* update gpg keyservers

## [1.287] - 2023-03-17
### Fixed
* Gitrunner fixes

## [1.285] - 2023-03-17
### Fixed
* Fix github runner install

## [1.284] - 2023-03-17
### Added
* Code cleanup, dependency upgrades and github runner installer

## [1.283] - 2023-02-21
### Added
* Python tooling improvements and improved AWS SSO support

## [1.282] - 2023-02-15
### Added
* Nexus cargo plugin and code formatting improvements

## [1.281] - 2023-01-12
### Fixed
* Fix tool installers

## [1.280] - 2023-01-04
### Removed
* Deprecate Phantomjs installation
### Added
* disable-rollback for Cloudformation stack deployment

## [1.279] - 2022-11-11
### Fixed
* Bugfix for azure arm and bicep typed parameter passing

## [1.278] - 2022-11-10
### Fixed
* Fix azure arm and bicep parameter typing

## [1.277] - 2022-10-29
### Fixed
* Fix bicep parameter handling

## [1.276] - 2022-10-05
### Fixed
* Downgrade default python to 3.8.10 because netifaces doesn't work on newer

## [1.275] - 2022-10-04
### Fixed
* Fix ansible changes from ansible_ssh_pass to ansible_password to fix Windows bakes

## [1.274] - 2022-09-06
### Fixed
* Session-to-env bugfix

## [1.273] - 2022-09-01
### Added
* Verify maven download with gpg

## [1.272] - 2022-08-23
### Added
* azure, adfs, lastpass and sso support for session_to_env

## [1.271] - 2022-06-24
### Fixed
* Minor android bugfix

## [1.270] - 2022-06-24
### Added
* Add androidsdk and flutter installers

## [1.269] - 2022-06-01
### Fixed
* Don't require aws sso cache dir to exist

## [1.268] - 2022-06-01
### Fixed
* Fix various places where aws sso profile support was lacking

## [1.267] - 2022-05-20
### Fixed
* Make yaml conversion safer

## [1.266] - 2022-05-17
### Added
* Add sso support for automatic profile enabling

## [1.265] - 2022-05-17
### Added
* Add support for AWS SSO profiles

## [1.264] - 2022-04-21
### Fixed
* Typo

## [1.263] - 2022-04-21
### Fixed
* IMAGE_WAIT not set if SECURITY_GROUP is set

## [1.262] - 2022-04-21
### Added
* Make image creation timeout configurable and increase linux timout default to 20 minutes

## [1.261] - 2022-04-14
### Fixed
* Openvpn tweaks

## [1.260] - 2022-04-14
### Fixed
* Mistaken sg edit revert

## [1.259] - 2022-04-13
### Fixed
* Openvpn bugfix

## [1.258] - 2022-04-13
### Fixed
* Fix missing curve for openvpn

## [1.257] - 2022-04-13
### Fixed
* Openvpn tweaks

## [1.256] - 2022-04-13
### Added
* Add openvpn utilities

## [1.255] - 2022-03-29
### Added
* Make jenkins start timeout a parameter

## [1.254] - 2022-03-29
### Fixed
* Increase jenkins startup timeout to 5mins since 1.5min is not enough for jenkins instances with larger histories

## [1.253] - 2022-03-28
### Added
* Az bicep commands removed and integrated into az tool

## [1.252] - 2022-03-28
### Fixed
* Multiarchitecture docker bake fix

## [1.251] - 2022-03-28
### Added
* Adapt jenkins tools to the new native systemd setup

## [1.250] - 2022-03-25
### Added
* Use old platformless build if PLATFORM is not defined

## [1.249] - 2022-03-25
### Added
* Iterate multiple architectures in PLATFORM if needed

## [1.248] - 2022-03-25
### Added
* Use buildx for different architechture support

## [1.247] - 2022-03-24
### Added
* Add PLATFORM parameter to build-docker for enabling arm64 platform containers

## [1.246] - 2022-03-21
### Added
* Add AzRef and related utils

## [1.245] - 2022-03-02
### Added
* Add --profile for profiling executions. Prints statistics to stderr

## [1.244] - 2022-02-13
### Added
* Fix Windows bake issues

## [1.243] - 2022-02-08
### Added
* Add a few missing region parameters still for image baking tasks

## [1.242] - 2022-02-08
### Added
* Add region for terminating old instances in baking

## [1.241] - 2022-02-04
### Fixed
* Fix typo in NO_PULL parameter handling

## [1.240] - 2022-01-24
### Added
* Add NO_PULL parameter to avoid pulling docker base images in cases where they are only locally available

## [1.239] - 2022-01-06
### Removed
* Drop python2 support

## [1.238] - 2021-12-31
### Added
* Add --pull to docker bake

## [1.237] - 2021-12-30
### Fixed
* Working AMI baking without legacy boto dependencies

## [1.236] - 2021-12-30
### Fixed
* Fix missing import

## [1.235] - 2021-12-30
### Added
* Work on removing awscli v1 and modernizing ansible aws modules.

## [1.234] - 2021-12-29
### Added
* Upgrade to awscli v2 and ubuntu 20.04 for the docker image base

## [1.233] - 2021-12-15
### Added
* Drop awscli as dependency to switch to aws cli 2

## [1.232] - 2021-12-01
### Fixed
* Windows bake fixes

## [1.231] - 2021-10-02
### Added
* Switch from eap (for enable aws profile) to nep (ndt enable profile) because it can also enable azure subscriptions

## [1.230] - 2021-10-02
### Added
* Add a bash function for enabling profiles quickly with full command completion

## [1.229] - 2021-09-28
### Fixed
* Minor maven auth bugfix

## [1.228] - 2021-09-21
### Added
* Add aws-config-to-json

## [1.227] - 2021-09-21
### Added
* Add a few profile utilities

## [1.226] - 2021-09-06
### Added
* Allow newer ec2-utils

## [1.225] - 2021-09-01
### Fixed
* Baking tweaks

## [1.224] - 2021-09-01
### Added
* Combine Rocky, RHEL and CentOS baking rules and switch to python 3.9 for default python for all

## [1.223] - 2021-08-31
### Fixed
* Rocky linux tweaks

## [1.222] - 2021-08-31
### Fixed
* Rocky linux support

## [1.221] - 2021-08-31
### Fixed
* Rocky linux support

## [1.220] - 2021-08-30
### Added
* Add rocky linux support

## [1.219] - 2021-08-16
### Added
* Upgrade ec2-utils

## [1.218] - 2021-08-14
### Fixed
* Bugfix to empty string property loading

### Added
* systemd portforward selinux module

## [1.217] - 2021-08-10
### Fixed
* Bugfix for resolve connect instance id
### Added
* harmonize connect deploy command name

## [1.216] - 2021-08-03
### Added
* Black formatting
* bitwarden tweaks

## [1.215] - 2021-07-30
### Added
* Upgrade ec2-utils to get the upgraded threadlocal-aws

## [1.214] - 2021-07-24
### Added
* Add capability to deploy AWS Connect contact flows

## [1.213] - 2021-07-22
### Added
* Minor bugfixes

## [1.212] - 2021-06-07
### Added
* Add note about ARM and Bicep

## [1.211] - 2021-06-07
### Fixed
* Tweak release process

## [1.210] - 2021-05-28
### Added
* Upgrade dehydrated and Add MongoDB 4.2 and 4.4 repos

## [1.209] - 2021-05-18
### Added
* Add dynatrace oneagent and activegate installations

## [1.208] - 2021-05-17
### Fixed
* Tweak pyenv virtualenv support

## [1.207] - 2021-05-17
### Added
* Add pyenv-virtualenv support for project utils

## [1.206] - 2021-05-11
### Added
* Newer pyaml for newer pythons

## [1.205] - 2021-05-10
### Fixed
* Compact log printing bugfix

## [1.204] - 2021-05-10
### Added
* Print logs in Insertion order for events with same nanosecond

## [1.203] - 2021-05-09
### Fixed
* Tweaks to compact log printing

## [1.202] - 2021-05-09
### Added
* Upgrade ec2-utils for fixed timezone handling in log printing

## [1.201] - 2021-05-09
### Added
* Upgrade ec2-utils for improved log short format printing

## [1.200] - 2021-05-08
### Added
* Uprade ec2-utils to get compact log format

## [1.199] - 2021-05-06
### Added
* Rest of gp2 -> gp3 transition

## [1.198] - 2021-05-06
### Added
* Switch to gp3 in templates

## [1.197] - 2021-05-06
### Added
* Upgrade ec2-utils to get volume type arguments

## [1.196] - 2021-05-04
### Added
* Add initial support for bicep templates https://github.com/Azure/bicep/

## [1.195] - 2021-05-04
### Added
* Add bw-store-aws-cli-creds

## [1.194] - 2021-05-04
### Added
* Minor Bitwarden MFA improvement

## [1.193] - 2021-04-28
### Added
* Safer quoting for *_DEFAULT_PASSWORD

## [1.192] - 2021-04-23
### Added
* Add also TOTP for lastpass if included in bitwarden entry

## [1.191] - 2021-04-22
### Added
* Add lastpass-aws-login support

## [1.190] - 2021-04-08
### Added
* Upgrade ec2-utils to create encrypted volumes by default

## [1.189] - 2021-03-31
### Added
* Ansible task deprecation and varnish repo upgrade

## [1.188] - 2021-03-03
### Added
* Fix ndt project property file writing

## [1.187] - 2021-03-03
### Added
* Fix ndt project property file writing

## [1.186] - 2021-02-28
### Added
* Avoid variables in parameter values for terraform

## [1.185] - 2021-02-25
### Added
* Upgrade ec2-utils

## [1.184] - 2021-01-23
### Added
* Codebuild project improvements

## [1.183] - 2021-01-23
### Added
* Codebuild project improvements

## [1.182] - 2021-01-11
### Added
* Upgrade ec2-utils

## [1.181] - 2020-12-31
### Added
* Zsh enable profile fixes

## [1.180] - 2020-12-28
### Added
* Azure Resource Manager support and route53 dns record upsert

## [1.179] - 2020-12-10
### Added
* Add Azure CLI subscription handling support

## [1.178] - 2020-12-09
### Added
* Dragging along older OpenSSL breaks aws cli so adding a dependency

## [1.177] - 2020-12-07
### Added
* Bitwarden password bugfix

## [1.176] - 2020-11-19
### Added
* Add mfa tokens backed by bitwarden entry totp secrets

## [1.175] - 2020-11-14
### Added
* Add bitwarden integration for adfs and azure profiles

## [1.174] - 2020-11-08
### Added
* Fix mfa backup functions

## [1.173] - 2020-11-08
### Added
* possible bug fix for mfa-tokens on WSL

## [1.172] - 2020-10-28
### Added
* Full path for ndt in jenkins setup since /usr/local/bin is no longer always on the PATH

## [1.171] - 2020-10-28
### Added
* Remove python2 syntax from letsencrypt hooks

## [1.170] - 2020-10-22
### Added
* Updated repositories for CentOS 8

## [1.169] - 2020-10-13
### Added
* Setuptools fixes for CentOS 7

## [1.168] - 2020-09-16
### Added
* Python2 dependency for Pygments that dropped support

## [1.167] - 2020-09-13
### Added
* Fix nexus3 url

## [1.166] - 2020-09-11
### Added
* Add get-docker.sh and remove deprecated nexus module install

## [1.165] - 2020-09-10
### Added
* Pip installing setuptools breaks platform setuptools

## [1.164] - 2020-09-09
### Added
* No longer ship with lpass. Leave runuser path setup to individual bakes

## [1.163] - 2020-09-09
### Added
* Better default for handling paths in init.d scripts

## [1.162] - 2020-09-09
### Added
* Make sure /usr/local/bin is on PATH

## [1.161] - 2020-09-09
### Added
* Consistent python-devel (3.6) for CentOS 8 bakes

## [1.160] - 2020-09-09
### Added
* Working Centos8 bake

## [1.159] - 2020-09-08
### Added
* Start working on Centos8 baking support

## [1.158] - 2020-09-04
### Added
* Add UNSAFE_NPM -parameter so that you can run unsafe scripts from package.json in serverless framework subcomponents

## [1.157] - 2020-09-03
### Added
* Fix terraform jmespath references

## [1.156] - 2020-09-03
### Added
* Update terraform support to match 0.13.x

## [1.155] - 2020-09-01
### Added
* Terraform and python3 fixes

## [1.154] - 2020-08-28
### Added
* Upgrade nitor-vault to make sure we get threadlocal-aws==0.8

## [1.153] - 2020-08-28
### Added
* In reference checking ignore serverless framework default resource that is secretly created by the framework

## [1.152] - 2020-08-26
### Added
* Handle components in different regions for upsert-codebuild-projects

## [1.151] - 2020-08-06
### Added
* Never convert parameter values to number objects. May actually be version strings and not numbers

## [1.150] - 2020-08-06
### Added
* Fix handling empty parameter values

## [1.149] - 2020-08-06
### Added
* Fix embdedded yaml processing for values where parameter replacement needs to be done before yaml parsing

## [1.148] - 2020-07-31
### Added
* Conditional python2/3 dependencies to manage some dependencies dropping python2 support

## [1.147] - 2020-07-31
### Added
* Remove unnecessary include at the end of install_tools.sh

## [1.146] - 2020-07-24
### Added
* Remove binary mode for python3 compatibility.

## [1.145] - 2020-07-03
### Added
* Allow compound valies in properties files (arrays and objects in yaml or json)

## [1.144] - 2020-06-30
### Added
* Get rid of f"" -syntax since it breaks python2

## [1.143] - 2020-06-10
### Added
* Add parameters to skip creating some codebuild jobs

## [1.142] - 2020-06-10
### Added
* Add --version flag

## [1.141] - 2020-06-10
### Added
* Add resovling ndt version for codebuild projects and clarify documentation

## [1.140] - 2020-06-09
### Added
* Bettter documentation for upsert-codebuild-projects and add CODEBUILD_EVENT_FILTER

## [1.139] - 2020-06-09
### Added
* Extra properties files for better handling of paramEnvId and codebuild project autogeneration

## [1.138] - 2020-06-01
### Added
* Add branch specific project settings

## [1.137] - 2020-05-27
### Added
* Always conceal secrets in serverless deployments

## [1.136] - 2020-05-27
### Added
* Upgrade nitor vault

## [1.135] - 2020-05-27
### Added
* Add Varnish 6.4 repo

## [1.133] - 2020-04-10
### Added
* Remove dateutil version requirements

## [1.132] - 2020-04-08
### Added
* Upgrade ec2-utils

## [1.131] - 2020-03-18
### Added
* Include SecureStrings in ssmrefs

## [1.130] - 2020-03-13
### Added
* Upgrade ec2-utils to 0.20

## [1.129] - 2020-03-12
### Added
* Make windows python version configurable with WIN_PYTHON_VERSION variable in infra.properties

## [1.128] - 2020-03-03
### Added
* Improve apache cipher suite

## [1.127] - 2020-03-03
### Added
* Improve SSL settings in apache_tools.sh

## [1.126] - 2020-03-02
### Added
* Minor bug fixes

## [1.125] - 2020-02-27
### Added
* Move to python 3.7.6 on windows

## [1.124] - 2020-02-26
### Added
* Switch to netifaces library in ec2-utils to interate network iterfaces

## [1.123] - 2020-02-06
### Added
* Allow aws_expiration credentials settings flag

## [1.122] - 2020-02-06
### Added
* Allow aws_expiration credentials settings flag

## [1.121] - 2020-02-06
### Added
* Allow aws_expiration credentials settings flag

## [1.120] - 2020-02-06
### Added
* Allow aws_expiration credentials settings flag

## [1.119] - 2020-02-06
### Added
* Allow aws_expiration credentials settings flag

## [1.118] - 2020-01-30
### Added
* Add ssm policy and remove deprecated ansible task from baking

## [1.117] - 2020-01-13
### Added
* Add support for aws-azure-login gui mode

## [1.116] - 2019-12-31
### Added
* Upgrade default maven

## [1.115] - 2019-12-31
### Added
* Ignore installed to upgrade things like pyyaml

## [1.114] - 2019-12-31
### Added
* Improve json dumps and nail PyYALM to a released version

## [1.113] - 2019-12-19
### Added
* Improve yaml-to-yaml robustness

## [1.112] - 2019-11-21
### Added
* Recursively import yaml

## [1.111] - 2019-11-13
### Added
* Fix botocore <-> pyton-dateutil version conflict. May be transient and need to be undone.

## [1.110] - 2019-11-05
### Added
* Fix python 2/3 compat issue

## [1.109] - 2019-11-02
### Added
* Add OwnerNamedAmi for resolving base ami images by an owner with a namimg convention (e.g. ubuntu by canonical)

## [1.108] - 2019-10-31
### Added
* Add ProductAmi for referring to an ami via a product code

## [1.107] - 2019-10-30
### Added
* Add SsmRef for referring to values in Ssm directly in properties files and Client-Side in templates

## [1.106] - 2019-10-29
### Added
* Harmonize ansible group names

## [1.104] - 2019-10-11
### Added
* ADFS login support

## [1.103] - 2019-10-10
### Added
* Fixed tests

## [1.102] - 2019-10-10
### Added
* Add YamlRef to properties files to be able to reference values in yaml files and a jmespath parameter to Fn::ImportYaml to import a specific part of a yaml document (say, a single value)

## [1.101] - 2019-10-03
### Added
* Upgrade ec2-utils

## [1.100] - 2019-10-03
### Added
* Upgrade ec2-utils with a couple of new commands

## [1.99] - 2019-09-30
### Added
* Maven install fixes and account creation tweaks

## [1.98] - 2019-09-13
### Added
* Add selinux tools to ubuntu

## [1.97] - 2019-09-06
### Added
* Add post-deploy script that is run after deployments and upgrade dehydrated, the letsencrypt script

## [1.96] - 2019-07-25
### Added
* Fix share images

## [1.95] - 2019-07-24
### Added
* Upgrade ec2-utils to address socket problem with python 2.7 on Windows

## [1.94] - 2019-07-08
### Added
* Fix #3

## [1.93] - 2019-07-08
### Added
* Fix docker bake

## [1.92] - 2019-07-05
### Added
* Add vault version requirement. Fixes #1

## [1.91] - 2019-07-05
### Added
* Fix imports

## [1.90] - 2019-07-05
### Added
* Fix import into threadlocal-aws

## [1.89] - 2019-07-05
### Added
* Tweak ec2-utils reference

## [1.88] - 2019-06-27
### Added
* Add lerna to docker image

## [1.87] - 2019-06-26
### Added
* Fixes to ec2-utils

## [1.86] - 2019-06-25
### Added
* Python3 compatibility fix

## [1.85] - 2019-06-20
### Added
* Fail baking if directory does not exist. Fix signal-cf-status

## [1.84] - 2019-06-19
### Added
* Fix logs-to-cloudwatch

## [1.83] - 2019-06-17
### Added
* Refactored ec2 specific code to ec2-utils pypi package. Template fixes.

## [1.82] - 2019-06-12
### Added
* ec2-utils fixes

## [1.81] - 2019-06-12
### Added
* Named image fix and move most logging code to ec2-utils

## [1.80] - 2019-05-23
### Added
* Small fixes

## [1.79] - 2019-05-15
### Added
* Add serverless verbose mode

## [1.78] - 2019-05-07
### Added
* Describe images missing region

## [1.77] - 2019-05-06
### Added
* Baked image cleanup now skips images that are in use on running instances or launch configurations

## [1.76] - 2019-04-26
### Added
* Minor unicode fix

## [1.75] - 2019-03-20
### Added
* Safe load and dump for mfa yaml (alredy safe everywhere else)

## [1.74] - 2019-03-19
### Added
* Bytes vs. str tweaks

## [1.73] - 2019-03-15
### Added
* Add aws credentials from the baking entity to be available during baking

## [1.72] - 2019-03-15
### Added
* Upgraded dehydrated.io and give AWS session to docker baking

## [1.71] - 2019-03-07
### Added
* Add simple mount script for ephermal current gen ephermal disks that have hardware encryption

## [1.70] - 2019-03-07
### Added
* Add chained cert storing to ensure-letsencrypt-certs.sh

## [1.69] - 2019-03-06
### Added
* MFA and private DNS tweaks

## [1.68] - 2019-03-01
### Added
* Minor tweaks

## [1.67] - 2019-03-01
### Added
* TFRef and Encrypt dynamic variables

## [1.66] - 2019-02-25
### Added
* Bake image tag fix

## [1.65] - 2019-02-25
### Added
* Terraform improvements

## [1.64] - 2019-02-25
### Added
* Terraform fixes

## [1.63] - 2019-02-21
### Added
* Fix windows reboot condition after bake installs updates

## [1.62] - 2019-02-21
### Added
* Subcomponent name resolution bugfix

## [1.61] - 2019-02-17
### Added
* First renamed release

## [1.60] - 2019-02-14
### Added
* Add mongodb 4.0 repo

## [1.59] - 2019-02-13
### Added
* Fixes for list-jobs

## [1.57] - 2019-02-05
### Added
* Add SKIP_NPM property to skip npm for serverless projects

## [1.56] - 2019-02-01
### Added
* Refactored the whole of project data reading from list-jobs.sh to python

## [1.55] - 2019-01-30
### Added
* Jenkins parameter resolving fix

## [1.54] - 2019-01-30
### Added
* Ami resolving bugfixes

## [1.53] - 2019-01-30
### Added
* Refactor ami id resolving. Now there is a way to mark a selected ami build into git: set param paramAmi
## [image-name]Build to the build you wish to resolve. This will override other ami resolving mechanisms

## [1.52] - 2019-01-29
### Added
* Parameter loading needs to resolve region for docker and ami resolving

## [1.51] - 2019-01-28
### Added
* Docker and ami resolving need region - list-jobs broken

## [1.50] - 2019-01-28
### Added
* Improve docker uri cacheing

## [1.49] - 2019-01-28
### Added
* Python 3 fixes

## [1.48] - 2019-01-28
### Added
* Improve StackRef resolving

## [1.47] - 2019-01-27
### Added
* StackRefs in parameter expansion for easy access in terraform subcomponents

## [1.46] - 2019-01-27
### Added
* Named AWS AMI image subcomponets. Initial CDK and Terraform integration

## [1.45] - 2018-12-18
### Added
* Fix windows non-clean images

## [1.44] - 2018-12-17
### Added
* Add reboot for windows bakes is windows updates require reboot

## [1.43] - 2018-12-10
### Added
* Cert management fix

## [1.42] - 2018-11-25
### Added
* Minor tweaks to parameter import

## [1.41] - 2018-11-24
### Added
* New type of file import parameter replacement

## [1.40] - 2018-11-13
### Added
* Ignore feature brances for listing jobs

## [1.39] - 2018-11-04
### Added
* Configparser requirement

## [1.38] - 2018-11-02
### Added
* Enable profile functionality

## [1.37] - 2018-10-20
### Added
* Improve job listing for job generation

## [1.36] - 2018-10-18
### Added
* Improve parameter replacement so that parameters in double paranthesis will be replaced also inside functions

## [1.35] - 2018-10-14
### Added
* Harmonized parameter use accross AMI and docker baking

## [1.34] - 2018-10-12
### Added
* Fix parameter expansion regression

## [1.33] - 2018-10-12
### Added
* Docker sudo fix

## [1.32] - 2018-10-12
### Added
* Fix for over-eager parameter expansion. Fixes #29

## [1.31] - 2018-10-12
### Added
* Remove sudo from docker use. Fixes #27

## [1.30] - 2018-10-08
### Added
* Make expiry epoc variable name profile specific

## [1.29] - 2018-10-08
### Added
* Improve aws profile tools for automated SAML login

## [1.28] - 2018-09-27
### Added
* Add missing dependency

## [1.26] - 2018-09-26
### Added
* Fix module for allow_authorizedkeyscommand

## [1.25] - 2018-09-26
### Added
* Add allow_authorizedkeyscommand

## [1.24] - 2018-09-26
### Added
* Fix dateutil dependency

## [1.23] - 2018-09-26
### Added
* Switch pytz to dateutil and add AWS_SESSION_EXPIRATION_EPOC if aws_session_expiration is defined for profile

## [1.22] - 2018-09-26
### Added
* Remove pycrypto

## [1.21] - 2018-09-24
### Added
* Minor python2 fix

## [1.20] - 2018-09-16
### Added
* Missing dependency

## [1.19] - 2018-09-14
### Added
* Required commands for automating aws-azure-login

## [1.18] - 2018-09-14
### Added
* Jenkins and nexus tooling fixes related to snapshotting on new generation instances

## [1.17] - 2018-09-13
### Added
* snapshotting fix

## [1.16] - 2018-09-13
### Added
* snapshotting, documentation and default repository fixes

## [1.15] - 2018-09-10
### Added
* Add command to wait for metadata service

## [1.14] - 2018-09-10
### Added
* Windows snapshotting fix

## [1.12] - 2018-09-06
### Added
* Tags for volumes and snapshots

## [1.11] - 2018-08-30
### Added
* Windows changes for new generation instance volume handling

## [1.10] - 2018-08-30
### Added
* Fix bug in bake tag handling

## [1.9] - 2018-08-30
### Added
* Fix pip upgrade for ubuntu

## [1.8] - 2018-08-30
### Added
* Fix volume opertions for new instance generation on linux

## [1.7] - 2018-08-29
### Added
* Fix is_ec2 for new t3 generation instances

## [1.6] - 2018-08-29
### Added
* Add customizable tags for bake image instances

## [1.5] - 2018-08-24
### Added
* Windows needs certifi for pytest

## [1.4] - 2018-08-24
### Added
* Windows pip upgrade fixes and python 3 fix for undeploy-stack

## [1.3] - 2018-08-23
### Added
* Resolve stackrefs earlier for them to be available in parameter expansion

## [1.2] - 2018-08-23
### Added
* Make sure PARAM_NOT_AVAILABLE is never repalaced into parameter expansion

## [1.1] - 2018-08-22
### Added
* Param import fix

## [1.0] - 2018-08-22
### Added
* Major version release, see documentation and RELEASE_NOTES.md

## [1.0a57] - 2018-08-22
### Added
* Parameter expansion improvements

## [1.0a56] - 2018-08-21
### Added
* Improved parameter expansion

## [1.0a55] - 2018-08-21
### Added
* Fix docker resolving

## [1.0a54] - 2018-08-21
### Added
* Fix docker resolving

## [1.0a53] - 2018-08-17
### Added
* Fix variable expansion

## [1.0a52] - 2018-08-16
### Added
* Minor fixes and documentation improvements

## [1.0a51] - 2018-08-16
### Added
* Minor compatibility fixes

## [1.0a50] - 2018-08-16
### Added
* Minor compatibility fixes

## [1.0a49] - 2018-08-16
### Added
* Minor compatibility fixes

## [1.0a48] - 2018-08-16
### Added
* Add parameter expansion to the whole template as a part of preprocessing

## [1.0a47] - 2018-08-12
### Added
* Fix command help printing

## [0.229] - 2018-08-02
### Added
* Make volume size configurable

## [0.228] - 2018-07-26
### Added
* Add pyqrcode

## [0.227] - 2018-07-25
### Added
* Add logstash repo

## [1.0a44] - 2018-07-24
### Added
* MFA documentation and improved backup

## [1.0a43] - 2018-07-02
### Added
* Retry logic tweaking

## [1.0a42] - 2018-07-01
### Added
* Retry logic tweaking

## [1.0a41] - 2018-07-01
### Added
* Log sending retry improvements

## [1.0a40] - 2018-07-01
### Added
* Syntax fix

## [1.0a39] - 2018-06-30
### Added
* Improve instance data retry logic

## [1.0a38] - 2018-06-30
### Added
* Add retries for instance info data

## [1.0a37] - 2018-06-29
### Added
* Versioning fix

## [1.0a35] - 2018-06-29
### Added
* Documentation formatting

## [1.0a34] - 2018-06-29
### Added
* Add template pre-processing documentation and make stack resources available for stackrefs

## [1.0a32] - 2018-06-08
### Added
* Minor fixes

## [1.0a31] - 2018-06-01
### Added
* Encrypted backup for mfa tokens

## [1.0a30] - 2018-05-29
### Added
* Log analysis fixes

## [1.0a29] - 2018-05-29
### Added
* Cloudwatch log analysis command and cleanup

## [1.0a28] - 2018-05-18
### Added
* Python3 fixes

## [1.0a27] - 2018-05-10
### Added
* Python3 compatibility removers str.decode

## [1.0a26] - 2018-05-08
### Added
* Removed eval set by modernize as unsafe on both pythons. Input unsafe only on python 2

## [1.0a25] - 2018-05-07
### Added
* Docker release fix

## [1.0a24] - 2018-05-07
### Added
* Python 3 output buffering fix

## [1.0a23] - 2018-05-03
### Added
* Upgrade docker infra

## [1.0a21] - 2018-04-18
### Added
* Change repos to use https

## [0.226] - 2018-04-18
### Added
* Change repos and keys to use https

## [1.0a20] - 2018-04-17
### Added
* Switch short argument to -i to save -d for potential future 'dryrun'

## [1.0a19] - 2018-04-16
### Added
* Add imagedefinitions option for codepipeline

## [1.0a18] - 2018-04-13
### Added
* Fix parameter quoting

## [1.0a17] - 2018-04-12
### Added
* Support for baking in alpa versions for testing on deployable infra

## [1.0a16] - 2018-04-11
### Added
* Docker entrypoint fix

## [1.0a15] - 2018-04-11
### Added
* Upgrade docker infrastructure to support docker-in-docker

## [1.0a14] - 2018-04-11
### Added
* Release testing

## [1.0a13] - 2018-04-11
### Added
* Release testing

## [1.0a12] - 2018-04-11
### Added
* Tweak docker relase process

## [1.0a11] - 2018-04-10
### Added
* Template generation fix

## [1.0a10] - 2018-04-10
### Added
* Job generation fixes

## [1.0a9] - 2018-04-10
### Added
* Job generation fixes

## [1.0a8] - 2018-04-10
### Added
* Template processing fixes

## [1.0a7] - 2018-04-10
### Added
* Quick alpha fixes for stack deployment

## [1.0a6] - 2018-04-10
### Added
* Quick alpha fixes for stack deployment

## [1.0a5] - 2018-04-10
### Added
* Quick alpha fixes for stack deployment

## [1.0a4] - 2018-04-10
### Added
* Quick alpha fixes for docker baking

## [1.0a3] - 2018-04-10
### Added
* Quick alpha fixes for docker baking

## [1.0a2] - 2018-04-10
### Added
* Quick alpha fixes for python3

## [1.0-alpha1] - 2018-04-10
### Added
* Major release, notes in git RELEASE_NOTES.md

## [0.225] - 2018-04-06
### Added
* Fix another case for setting a checksum into userdata for more reliably replacing instances on changes

## [0.224] - 2018-04-06
### Added
* Fix another case for setting a checksum into userdata for more reliably replacing instances on changes

## [0.223] - 2018-03-06
### Added
* Fix sudo handling

## [0.222] - 2018-03-06
### Added
* Always create ami.properties to avoid failing deploys for stacks without images

## [0.221] - 2018-03-02
### Added
* Add encryption to MFA secret. If an unencrypted secret is seen, it is transparently encrypted. They key is a hash using local computer uuid and current username

## [0.220] - 2018-02-28
### Added
* Safe execution of instanceinfo for non-root users

## [0.219] - 2018-02-28
### Added
* Use sudo for docker bake only if available

## [0.218] - 2018-02-28
### Added
* Use sudo for docker bake only if available

## [0.217] - 2018-02-28
### Added
* Use sudo for docker bake only if available

## [0.216] - 2018-02-28
### Added
* Use sudo for docker bake only if available

## [0.215] - 2018-02-28
### Added
* Use sudo for docker bake only if available

## [0.214] - 2018-02-02
### Added
* Fix for parametrized import

## [0.213] - 2018-02-02
### Added
* Fix parametrized import

## [0.212] - 2018-02-02
### Added
* Fix recursive parameter passing

## [0.211] - 2018-01-25
### Added
* Bake fix

## [0.210] - 2018-01-18
### Added
* Enable using parameters in yaml includes

## [0.209] - 2018-01-16
### Added
* Letsencrypt registration fix

## [0.208] - 2018-01-15
### Added
* Cleanup and improve documentation

## [0.207] - 2018-01-15
### Added
* Route53 configuration

## [0.206] - 2018-01-15
### Added
* Finalize 'ndt create-stack network' - it now creates common/network.yaml for easy access to parameters

## [0.205] - 2018-01-13
### Added
* Do also image baking with the deploy role

## [0.204] - 2018-01-09
### Added
* Add selection for vault stack into bakery roles

## [0.203] - 2018-01-09
### Added
* Fix create-stack argument parsing

## [0.202] - 2018-01-09
### Added
* New stack template mechanism, start with network stack and bakery roles stack

## [0.201] - 2017-12-04
### Added
* Fixes related to letsencrypt.sh upgrade

## [0.200] - 2017-12-04
### Added
* Fixes related to letsencrypt.sh upgrade

## [0.199] - 2017-12-04
### Added
* Attempt to upgrade letsencrypt.sh

## [0.198] - 2017-11-14
### Added
* Add mfa support

## [0.197] - 2017-11-09
### Added
* Add libjpeg-turbo repo

## [0.195] - 2017-11-07
### Added
* Add yum repos for MySQL 5.7 and MongoDB 3.4

## [0.194] - 2017-10-06
### Added
* Jenkins refactoring

## [0.193] - 2017-10-06
### Added
* Bring back copy of default jenkins home for empty jenkins-home

## [0.192] - 2017-09-28
### Added
* Fix typo

## [0.191] - 2017-09-26
### Added
* Try and ensure logging more

## [0.190] - 2017-09-26
### Added
* Fix ndt undeploy-stack

## [0.189] - 2017-09-24
### Added
* Fix upsert alias records

## [0.188] - 2017-09-23
### Added
* Only get keys for baking if not already found

## [0.187] - 2017-09-21
### Added
* Sync (upsert) cloudfront distribution aliases as DNS records into route53

## [0.186] - 2017-09-18
### Added
* Hopefully a reliable way to wait for a successful connection

## [0.185] - 2017-09-18
### Added
* File system error handling

## [0.184] - 2017-09-18
### Added
* Resize print bugfix

## [0.183] - 2017-09-18
### Added
* Logging conf tweaks

## [0.182] - 2017-09-18
### Added
* Add a prepare script for linux images - for now tries to make sure we get cloud-init output

## [0.181] - 2017-09-17
### Added
* Jenkins init fix

## [0.180] - 2017-09-13
### Added
* Make sure file exists before starting polling

## [0.179] - 2017-09-13
### Added
* Make timeout configurable

## [0.178] - 2017-09-12
### Added
* Make instance type configurable

## [0.177] - 2017-09-12
### Added
* Fix collision in base_ami parameter name

## [0.176] - 2017-09-12
### Added
* Attempt to fix windows base image functionality

## [0.174] - 2017-09-12
### Added
* Base image support for windows

## [0.173] - 2017-09-06
### Added
* Wrong branch for resolving docker name

## [0.172] - 2017-09-05
### Added
* Varnish 4.1 repo moved

## [0.171] - 2017-09-03
### Added
* Parameter documentation improvements

## [0.170] - 2017-08-31
### Added
* Fix interpolation bug

## [0.169] - 2017-08-24
### Added
* Run pre_build.sh in the docker folder fix

## [0.168] - 2017-08-24
### Added
* Run pre_build.sh in the docker folder

## [0.167] - 2017-08-24
### Added
* pre_build.sh script run before docker build for e.g. downloading files neded in the image

## [0.166] - 2017-08-23
### Added
* Add delete on termination as default

## [0.165] - 2017-08-23
### Added
* Assume role needs to happen before resolving ecr repos

## [0.164] - 2017-08-21
### Added
* Fix bug in parameter replacement interacting with intrisinc functions

## [0.163] - 2017-08-21
### Added
* Fix bug in parameter replacement interacting with intrisinc functions

## [0.162] - 2017-08-18
### Added
* CloudFormation does not allow underscores

## [0.161] - 2017-08-18
### Added
* Intrisinc function fix

## [0.160] - 2017-08-18
### Added
* Fix for yaml intrisinc functions

## [0.159] - 2017-08-18
### Added
* Suppor yaml versions of intrisinc functions and bugfix

## [0.158] - 2017-08-17
### Added
* Docker - stack integration

## [0.157] - 2017-08-16
### Added
* Working docker support

## [0.156] - 2017-08-16
### Added
* More docker tweaks

## [0.155] - 2017-08-16
### Added
* Docker tweak

## [0.154] - 2017-08-16
### Added
* Initial docker support

## [0.153] - 2017-08-15
### Added
* Fix ndt volume-from-snapshot

## [0.152] - 2017-08-15
### Added
* Switch to ndt for volume-from-snapshot

## [0.151] - 2017-08-10
### Added
* Add named iam to capabilities to be able to make named managed policies

## [0.150] - 2017-08-08
### Added
* Fix interpolate on windows

## [0.149] - 2017-08-06
### Added
* Jenkins userdata fix

## [0.148] - 2017-08-03
### Added
* Snapshot bugfixes

## [0.147] - 2017-08-03
### Added
* Wait parameter for snapshot-from-volume, refactor region resolving and remove git references from jenkins setup

## [0.146] - 2017-08-02
### Added
* Increase wait timeout for image creation

## [0.145] - 2017-07-28
### Added
* Add parameter name for stack parameters if only one needed

## [0.144] - 2017-07-18
### Added
* Resolve image before assume role so that cross account image sharing works

## [0.143] - 2017-07-17
### Added
* Delete tmp dir on success

## [0.142] - 2017-07-16
### Added
* Delete tmp dir on success

## [0.141] - 2017-07-16
### Added
* Add env variable DEPLOY_ROLE_ARN to be able to specify a role to assume per stack

## [0.140] - 2017-07-16
### Added
* Add env variable DEPLOY_ROLE_ARN to be able to specify a role to assume per stack

## [0.139] - 2017-07-16
### Added
* Add env variable DEPLOY_ROLE_ARN to be able to specify a role to assume per stack

## [0.138] - 2017-07-03
### Added
* Fix account resolving to resolve the effective account from sts and thus fix cross account snapshot deletion

## [0.137] - 2017-06-14
### Added
* Fix tag lookup failures

## [0.136] - 2017-06-14
### Added
* Make cf-init more flexible

## [0.135] - 2017-06-14
### Added
* Fix ec2-get-tag output typo

## [0.134] - 2017-06-14
### Added
* Fix ec2-get-tag output typo

## [0.133] - 2017-06-14
### Added
* Add ec2-get-tag

## [0.132] - 2017-06-13
### Added
* Write ami.properties on image promote

## [0.131] - 2017-06-13
### Added
* Promote job fixes

## [0.130] - 2017-06-12
### Added
* Fetch secrets vault bugfix

## [0.129] - 2017-06-12
### Added
* Lastpass fetch notes bugfix

## [0.128] - 2017-06-12
### Added
* Improve optional get handling (do not leave ghost files)

## [0.127] - 2017-06-08
### Added
* Get rid of delete snapshots lambda, because ndt ec2-clean-snapshots in a jenkins job is preferred

## [0.126] - 2017-06-06
### Added
* Add register-private-dns

## [0.125] - 2017-05-31
### Added
* Another attempt at ubuntu locale fix

## [0.124] - 2017-05-31
### Added
* Ubuntu fix

## [0.123] - 2017-05-30
### Added
* Request syntax fix for image sharing

## [0.122] - 2017-05-30
### Added
* Fix for RequestLimitExceeded wheh copying to another region

## [0.121] - 2017-05-30
### Added
* First working version of jenkins job generation script

## [0.120] - 2017-05-29
### Added
* Write ami properties for autopromoting

## [0.119] - 2017-05-29
### Added
* Fix for stack references to stacks without parameters

## [0.118] - 2017-05-27
### Added
* Fix

## [0.117] - 2017-05-27
### Added
* Functions for getting ami lists for promote jobs, promotes images between branches and brought back ami sharing

## [0.116] - 2017-05-26
### Added
* Append \r\n to embedded CF parameters in ps1 files instead of \n

## [0.115] - 2017-05-26
### Added
* Rewrite show-stack-params-and-outputs.sh in python to get around problems that script has with older jq versions

## [0.114] - 2017-05-26
### Added
* Rewrite show-stack-params-and-outputs.sh in python to get around problems that script has with older jq versions

## [0.113] - 2017-05-23
### Added
* list jobs property generation fix

## [0.112] - 2017-05-23
### Added
* list jobs property generation fix

## [0.111] - 2017-05-23
### Added
* list jobs property generation fix

## [0.110] - 2017-05-23
### Added
* Properties generation bugfix

## [0.109] - 2017-05-23
### Added
* Usage bugfix

## [0.107] - 2017-05-21
### Added
* Job listing bugfix

## [0.106] - 2017-05-20
### Added
* Job listing bugfix

## [0.105] - 2017-05-20
### Added
* Job listing checkouts without side affects

## [0.104] - 2017-05-20
### Added
* Job listing support for older git

## [0.103] - 2017-05-20
### Added
* Job listing adds more info

## [0.102] - 2017-05-19
### Added
* Add list-jobs script to list buildable jobs from a nitor-deploy-tools targeted repo

## [0.101] - 2017-05-19
### Added
* Fixed ndt usage printing

## [0.100] - 2017-05-19
### Added
* Add colorize option for json-to-yaml and yaml-to-json

## [0.99] - 2017-05-18
### Added
* Minor output coloring tweaks

## [0.98] - 2017-05-18
### Added
* Deploy fix and colored output for final stack and changeset in deploy

## [0.97] - 2017-05-18
### Added
* Improve shell autocomplete

## [0.96] - 2017-05-11
### Added
* Jenkins key access rights fix

## [0.95] - 2017-05-09
### Added
* Some windows volume function improvements

## [0.94] - 2017-05-09
### Added
* Implemented volume operations as cross-platform python functions

## [0.93] - 2017-05-09
### Added
* Implemented volume operations as cross-platform python functions

## [0.92] - 2017-05-02
### Added
* Working python cli command completion for many functions

## [0.91] - 2017-04-29
### Added
* OSX fixes

## [0.90] - 2017-04-29
### Added
* OSX fixes

## [0.89] - 2017-04-27
### Added
* More command completion work and print proposed changeset for updates with deploy dryrun

## [0.88] - 2017-04-26
### Added
* Maven configuration fixes

## [0.87] - 2017-04-26
### Added
* Require argcomplete

## [0.86] - 2017-04-26
### Added
* Started work on ndt tool that would collect all scripts and provide command completion. Added ec2 instance detection to some commands

## [0.85] - 2017-04-20
### Added
* Path separator fix

## [0.84] - 2017-04-07
### Added
* Setup fixes and a timeout for instance metadata for running outside aws

## [0.83] - 2017-04-04
### Added
* Add dry-run argument to deploy-stack.sh

## [0.82] - 2017-04-03
### Added
* Minor fix

## [0.81] - 2017-03-27
### Added
* InstanceInfo bugfix

## [0.80] - 2017-03-27
### Added
* Try to make sure we have instance data

## [0.79] - 2017-03-27
### Added
* Instance data loading bugfix

## [0.78] - 2017-03-13
### Added
* default to v4 signatures for s3 and move region setting to common tools

## [0.77] - 2017-03-07
### Added
* Fix nexus-userdata script

## [0.76] - 2017-03-06
### Added
* Make an option for using private subnets for baking

## [0.75] - 2017-02-27
### Added
* Allow exit values 0, 1 and 2 from e2fsck

## [0.74] - 2017-02-27
### Added
* Allow exit values 0, 1 and 2 from e2fsck

## [0.73] - 2017-02-16
### Added
* More fail2ban fixes

## [0.72] - 2017-02-16
### Added
* More fail2ban fixes

## [0.71] - 2017-02-16
### Added
* More fail2ban fixes

## [0.70] - 2017-02-16
### Added
* Fail2ban fix

## [0.69] - 2017-02-16
### Added
* Add setup-network bootstrap command

## [0.68] - 2017-02-14
### Added
* Bake fix

## [0.67] - 2017-02-14
### Added
* Fixes

## [0.66] - 2017-02-13
### Added
* Add setup-cli command

## [0.65] - 2017-02-11
### Added
* A few utility shell functions

## [0.64] - 2017-02-08
### Added
* cli doc fix

## [0.63] - 2017-02-08
### Added
* Add region handling for ec2-clean-snapshot

## [0.62] - 2017-02-08
### Added
* Add ec2-clean-snapshots command

## [0.61] - 2017-02-07
### Added
* More fixes for fetch and store secret scripts

## [0.60] - 2017-02-07
### Added
* Enable lpass fetch secrets outside of a stack

## [0.59] - 2017-02-07
### Added
* lpass link fix

## [0.58] - 2017-02-07
### Added
* Deploy role fix

## [0.57] - 2017-02-07
### Added
* Log tailing fix

## [0.56] - 2017-02-06
### Added
* More windows scaffolding

## [0.55] - 2017-02-06
### Added
* Add jq as a default package into bake

## [0.54] - 2017-02-06
### Added
* Add missing ephermal storage script

## [0.53] - 2017-02-06
### Added
* Include selinux config

## [0.52] - 2017-02-06
### Added
* Fix secrets scripts

## [0.51] - 2017-02-06
### Added
* Fix secrets scripts

## [0.50] - 2017-02-04
### Added
* Add missing nexus_tools.sh

## [0.49] - 2017-02-01
### Added
* Finalize migration from aws-utils

## [0.48] - 2017-01-28
### Added
* Ansible.cfg fix

## [0.47] - 2017-01-28
### Added
* Fix windows bake

## [0.46] - 2017-01-28
### Added
* Add yml files

## [0.45] - 2017-01-28
### Added
* Move baking over from aws-utils

## [0.44] - 2017-01-27
### Added
* Backwards compatibility fix

## [0.43] - 2017-01-27
### Added
* Backwards compatibility fix

## [0.42] - 2017-01-27
### Added
* Backwards compatibility fix

## [0.41] - 2017-01-26
### Added
* Move utility scripts from aws-utils

## [0.40] - 2017-01-26
### Added
* Move a most utility scripts into includes with this python package

## [0.39] - 2017-01-25
### Added
* Move template snippets over from aws-utils

## [0.38] - 2017-01-20
### Added
* Optionally use s3 for template deployment if CF_BUCKET environment variable is defined

## [0.37] - 2017-01-18
### Added
* ec2-get-userdata function and small bugfixes

## [0.36] - 2017-01-16
### Added
* Userid util fix

## [0.35] - 2017-01-10
### Added
* Logging improvements

## [0.34] - 2017-01-10
### Added
* Stop cf_events thread

## [0.33] - 2017-01-10
### Added
* Doc fixes

## [0.32] - 2017-01-10
### Added
* An attempt to fix encoding problems

## [0.31] - 2017-01-10
### Added
* Moved a handful of utilities from aws-utils

## [0.30] - 2017-01-10
### Added
* Logging improvements

## [0.29] - 2017-01-09
### Added
* Logging fix

## [0.28] - 2017-01-09
### Added
* Time calculation bugfix

## [0.27] - 2017-01-09
### Added
* Logging fix

## [0.26] - 2017-01-09
### Added
* Logging improvements

## [0.25] - 2017-01-09
### Added
* Missing dependency fix

## [0.24] - 2017-01-09
### Added
* Logging improvements

## [0.23] - 2017-01-05
### Added
* Logging improvements and cf-delete-stack

## [0.22] - 2017-01-04
### Added
* Allow missing log group and cleanup

## [0.21] - 2017-01-04
### Added
* Allow stacks without parameters or outputs

## [0.20] - 2017-01-04
### Added
* Fixes for encoding and newly created stacks

## [0.19] - 2017-01-01
### Added
* CloudFormation functions moved to get better logging

## [0.18] - 2016-12-24
### Added
* Add cli utilities for getting simple pieces of instanec info

## [0.17] - 2016-12-24
### Added
* Adds 'n-utils-init' to make sure data has been fetched

## [0.16] - 2016-12-22
### Added
* Fixed log sending

## [0.15] - 2016-12-22
### Added
* Bugfix release

## [0.14] - 2016-12-22
### Added
* Fix eip allocation defaults

## [0.13] - 2016-12-22
### Added
* Batching for log sending

## [0.12] - 2016-12-21
### Added
* CloudFormation signal bugfix

## [0.11] - 2016-12-21
### Added
* Add missing package

## [0.10] - 2016-12-21
### Added
* Bugfix release

## [0.9] - 2016-12-21
### Added
* Next release

## [0.8] - 2016-12-18
### Added
* Start moving functionality from aws-utils - just lift and shift for now

## [0.7] - 2016-12-15
### Added
* Add overwrite protection and fix dependencies

## [0.6] - 2016-12-13
### Added
* Prepare for release

## [0.5] - 2016-12-07
### Added
* Next release

## [0.4] - 2016-12-07
### Added
* New release

## [0.3] - 2016-12-07
### Added
* New release

## [0.1] - 2016-12-07
### Added
* Prepare for first release
