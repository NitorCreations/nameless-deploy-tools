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


if [ "$_ARGCOMPLETE" ]; then
  # Handle command completion executions
  unset _ARGCOMPLETE
  source $(n-include autocomplete-helpers.sh)
  case $COMP_CWORD in
    2)
      compgen -W "-h -i $(get_stack_dirs)" -- $COMP_CUR
      ;;
    3)
      compgen -W "$(get_images $COMP_PREV)" -- $COMP_CUR
      ;;
    *)
      exit 1
      ;;
  esac
  exit 0
fi


usage() {
  echo "usage: ndt bake-image [-h] component [image-name]" >&2
  echo "" >&2
  echo "Runs an ansible playbook that  builds an Amazon Machine Image (AMI) and" >&2
  echo "tags the image with the job name and build number." >&2
  echo "" >&2
  echo "positional arguments" >&2
  echo "  component     the component directory where the ami bake configurations are" >&2
  echo "  [image-name]  Optional name for a named image in component/image-[image-name]" >&2
  echo "" >&2
  echo "optional arguments:" >&2
  echo "  -h, --help  show this help message and exit" >&2

  if "$@"; then
    echo "" >&2
    echo "$@" >&2
  fi
  exit 1
}
if [ "$1" = "--help" -o "$1" = "-h" ]; then
  usage
fi

die () {
  usage
}
set -xe

component="$1" ; shift
[ "${component}" ] || die "You must give the component name as argument"

eval "$(ndt load-parameters "$component" -i "$1" -e)"

#If assume-deploy-role.sh is on the path, run it to assume the appropriate role for deployment
if [ -n "$BAKE_ROLE_ARN" ] && [ -z "$AWS_SESSION_TOKEN" ]; then
  eval $(ndt assume-role $BAKE_ROLE_ARN)
elif [ -n "$DEPLOY_ROLE_ARN" ] && [ -z "$AWS_SESSION_TOKEN" ]; then
  eval "$(ndt assume-role "$DEPLOY_ROLE_ARN")"
elif which assume-deploy-role.sh > /dev/null && [ -z "$AWS_SESSION_TOKEN" ]; then
  eval $(assume-deploy-role.sh)
fi

# Set defaults if not customized
if ! [ "$SSH_USER" ]; then
  if [ "$IMAGETYPE" = "windows" ]; then
    SSH_USER="Administrator"
  else
    SSH_USER="$IMAGETYPE"
  fi
fi
[ "$NETWORK_STACK" ] || NETWORK_STACK=network
[ "$PRIVATE_SUBNET" ] || PRIVATE_SUBNET="no"
if ! [ "$NETWORK_PARAMETER" ]; then
  if [ "$PRIVATE_SUBNET" = "yes" ]; then
    NETWORK_PARAMETER=subnetPrivB
  else
    NETWORK_PARAMETER=subnetB
  fi
fi
[ "$SUBNET" ] || SUBNET="$(ndt show-stack-params-and-outputs -r $REGION $NETWORK_STACK -p $NETWORK_PARAMETER)"
[ "$BAKERY_ROLES_STACK" ] || BAKERY_ROLES_STACK=bakery-roles
if ! [ "$SECURITY_GROUP" ]; then
  if [ "$IMAGETYPE" != "windows" ]; then
    [ "$SG_PARAM" ] || SG_PARAM="bakeInstanceSg"
  else
    [ "$SG_PARAM" ] || SG_PARAM="bakeWinInstanceSg"
  fi
  SECURITY_GROUP="$(ndt show-stack-params-and-outputs -r $REGION $BAKERY_ROLES_STACK -p $SG_PARAM)"
fi
if ! [ "$AMIBAKE_INSTANCEPROFILE" ]; then 
  [ "$INSTANCE_PROFILE_PARAM" ] || INSTANCE_PROFILE_PARAM="bakeInstanceInstanceprofile"
  AMIBAKE_INSTANCEPROFILE="$(ndt show-stack-params-and-outputs -r $REGION $BAKERY_ROLES_STACK -p $INSTANCE_PROFILE_PARAM)"
fi
[ "$PAUSE_SECONDS" ] || PAUSE_SECONDS=15
for var in REGION SUBNET SECURITY_GROUP AMIBAKE_INSTANCEPROFILE ; do
  [ "${!var}" ] || die "Could not determine $var automatically. Please set ${var} manually in ${infrapropfile}"
done

for var in AWS_KEY_NAME paramDeployToolsVersion; do
  [ "${!var}" ] || die "Please set ${var} in ${sharedpropfile}"
done

for var in IMAGETYPE APP_USER APP_HOME SSH_USER; do
  [ "${!var}" ] || die "Please set ${var} in ${infrapropfile}"
done

if [ -n "$1" ]; then
  imagedir="${component}/image-$1"
else
  imagedir="${component}/image"
fi

[ -d "$imagedir" ] || die "Imagedir $imagedir does not exist"

VAR_AMI="AMIID_${IMAGETYPE}"
AMI="${!VAR_AMI}"

if aws sts get-caller-identity | grep "Arn\":.*:assumed-role/" > /dev/null; then
  ASSUMED_ROLE="Y"
else
  ASSUMED_ROLE="N"
fi

if [ $ASSUMED_ROLE = "N" ]; then
  eval "$(ndt session-to-env)"
elif [ -z "$AWS_SESSION_TOKEN" ]; then
  eval "$(ndt profile-to-env $AWS_PROFILE)"
fi

cat > $imagedir/bake-credentials << EOF
[bake]
aws_access_key_id=$AWS_ACCESS_KEY_ID
aws_secret_access_key=$AWS_SECRET_ACCESS_KEY
aws_session_token=$AWS_SESSION_TOKEN
EOF

[ "$AMI" ] || die "Please set AMIID_$IMAGETYPE in ${infrapropfile}"

TSTAMP=$(date +%Y%m%d%H%M%S)

cleanup() {
  if [ "$IMAGETYPE" != "windows" ]; then
    eval $(ssh-agent -k)
  fi
}
trap cleanup EXIT
if [ "$IMAGETYPE" != "windows" ]; then
  eval $(ssh-agent)
  if ! [ -e $HOME/.ssh/$AWS_KEY_NAME -o -e $HOME/.ssh/$AWS_KEY_NAME.pem \
         -o -e $HOME/.ssh/$AWS_KEY_NAME.rsa ]; then
    fetch-secrets.sh get 600 --optional "$HOME/.ssh/$AWS_KEY_NAME" \
        "$HOME/.ssh/$AWS_KEY_NAME.pem" "$HOME/.ssh/$AWS_KEY_NAME.rsa" ||:
  fi
  if [ -r "$HOME/.ssh/$AWS_KEY_NAME" ]; then
    ssh-add "$HOME/.ssh/$AWS_KEY_NAME"
  elif [ -r "$HOME/.ssh/$AWS_KEY_NAME.pem" ]; then
    ssh-add "$HOME/.ssh/$AWS_KEY_NAME.pem"
  elif [ -r "$HOME/.ssh/$AWS_KEY_NAME.rsa" ]; then
    ssh-add "$HOME/.ssh/$AWS_KEY_NAME.rsa"
  else
    die "Failed to find ssh private key"
  fi
  extra_args[${#extra_args[@]}]=-e
  extra_args[${#extra_args[@]}]="prepare_script=$(n-include prepare.sh)"
  [ "$VOLUME_SIZE" ] || VOLUME_SIZE=8
else
  WIN_PASSWD="$(tr -cd '[:alnum:]' < /dev/urandom | head -c16)"
  PASSWD_ARG="{\"ansible_ssh_pass\": \"$WIN_PASSWD\","
  PASSWD_ARG="$PASSWD_ARG \"ansible_winrm_operation_timeout_sec\": 60,"
  PASSWD_ARG="$PASSWD_ARG \"ansible_winrm_read_timeout_sec\": 70,"
  PASSWD_ARG="$PASSWD_ARG \"ansible_winrm_server_cert_validation\": \"ignore\","
  PASSWD_ARG="$PASSWD_ARG \"prepare_script\": \"$(n-include prepare.ps1)\"}"
  [ "$VOLUME_SIZE" ] || VOLUME_SIZE=30
fi
if [ -z "$BUILD_NUMBER" ]; then
  BUILD_NUMBER=$TSTAMP
else
  BUILD_NUMBER=$(printf "%04d\n" $BUILD_NUMBER)
fi
if [ -z "$JOB_NAME" ]; then
  if [ -n "$1" ]; then
    JOB_NAME="${JENKINS_JOB_PREFIX}-${component}-bake-$1"
  else
    JOB_NAME="${JENKINS_JOB_PREFIX}-${component}-bake"
  fi
fi
if [ "$IMAGETYPE" != "windows" ]; then
  if ! [ -r $imagedir/pre_install.sh ]; then
    echo -e "#!/bin/bash\n\nexit 0" > $imagedir/pre_install.sh
  fi
  if ! [ -r $imagedir/post_install.sh ]; then
    echo -e "#!/bin/bash\n\nexit 0" > $imagedir/post_install.sh
  fi
else
  if ! [ -r $imagedir/pre_install.ps1 ]; then
    echo -e "exit 0\r" > $imagedir/pre_install.ps1
  fi
  if ! [ -r $imagedir/post_install.ps1 ]; then
    echo -e "exit 0\r" > $imagedir/post_install.ps1
  fi
fi
touch $imagedir/packages.txt
PACKAGES="$(ndt list-file-to-json packages $imagedir/packages.txt)"
touch $imagedir/files.txt
FILES="$(ndt list-file-to-json files $imagedir/files.txt)"
if [ -r "$imagedir/tags.yaml" ]; then
  TAGS="$(ndt yaml-to-json $imagedir/tags.yaml -m $(n-include bake-tags.yaml) -s)"
else
  TAGS="$(ndt yaml-to-json $(n-include bake-tags.yaml) -s)"
fi
if [ "$IMAGETYPE" = "ubuntu" ]; then
  touch $imagedir/repos.txt $imagedir/keys.txt
  REPOS="$(ndt list-file-to-json repos $imagedir/repos.txt)"
  KEYS="$(ndt list-file-to-json keys $imagedir/keys.txt)"
  extra_args[${#extra_args[@]}]=-e
  extra_args[${#extra_args[@]}]="$REPOS"
  extra_args[${#extra_args[@]}]=-e
  extra_args[${#extra_args[@]}]="$KEYS"
else
  extra_args[${#extra_args[@]}]=-e
  extra_args[${#extra_args[@]}]='{"repos": []}'
  extra_args[${#extra_args[@]}]=-e
  extra_args[${#extra_args[@]}]='{"keys": []}'
fi
if [ -n "$BASE_IMAGE_JOB" ]; then
  AMI=$(ndt get-images $BASE_IMAGE_JOB | head -1 | cut -d: -f1)
  extra_args[${#extra_args[@]}]=-e
  extra_args[${#extra_args[@]}]=base_ami_id=$AMI
  extra_args[${#extra_args[@]}]=-e
  extra_args[${#extra_args[@]}]=bake_userdata=win-userdata-unclean.txt.j2
else
  extra_args[${#extra_args[@]}]=-e
  extra_args[${#extra_args[@]}]=base_ami_id=clean
  extra_args[${#extra_args[@]}]=-e
  extra_args[${#extra_args[@]}]=bake_userdata=win-userdata.txt.j2
fi
if [ -n "$INSTANCE_TYPE" ]; then
  extra_args[${#extra_args[@]}]=-e
  extra_args[${#extra_args[@]}]=instance_type=$INSTANCE_TYPE
else
  extra_args[${#extra_args[@]}]=-e
  extra_args[${#extra_args[@]}]=instance_type=t2.medium
fi
if [ -n "$BAKE_TIMEOUT" ]; then
  extra_args[${#extra_args[@]}]=-e
  extra_args[${#extra_args[@]}]=timeout_min=$BAKE_TIMEOUT
else
  extra_args[${#extra_args[@]}]=-e
  extra_args[${#extra_args[@]}]=timeout_min=55
fi

JOB=$(echo $JOB_NAME | sed 's/[^[:alnum:]_]/_/g' | tr '[:upper:]' '[:lower:]')
NAME="${JOB}_$BUILD_NUMBER"
AMI_TAG="$NAME"
echo "$AMI_TAG" > ami-tag.txt
echo "$NAME" > name.txt

export ANSIBLE_FORCE_COLOR=true
export ANSIBLE_HOST_KEY_CHECKING=false

if [ "$IMAGETYPE" = "windows" ]; then
  PLAYBOOK="$(n-include bake-win-image.yml)"
else
  PLAYBOOK="$(n-include bake-image.yml)"
fi
rm -f ami.properties ||:
cat > ansible.cfg << MARKER
[defaults]
retry_files_enabled = False
MARKER
if python -u $(which ansible-playbook) \
  -vvvv \
  --flush-cache \
  $PLAYBOOK \
  -e tools_version=$paramDeployToolsVersion \
  -e ami_tag=$AMI_TAG \
  -e ami_id_file=$(pwd -P)/ami-id.txt \
  -e job_name=$JOB \
  -e aws_key_name=$AWS_KEY_NAME \
  -e app_user=$APP_USER \
  -e app_home=$APP_HOME \
  -e build_number=$BUILD_NUMBER \
  -e private_subnet=$PRIVATE_SUBNET \
  -e "$PACKAGES" \
  -e "$FILES" \
  -e "{\"bake_tags\": $TAGS }" \
  "${extra_args[@]}" \
  -e root_ami=$AMI \
  -e tstamp=$TSTAMP \
  -e aws_region=$REGION \
  -e ansible_ssh_user=$SSH_USER \
  -e imagedir="$(realpath "${imagedir}")" \
  -e subnet_id=$SUBNET \
  -e sg_id=$SECURITY_GROUP \
  -e amibake_instanceprofile=$AMIBAKE_INSTANCEPROFILE \
  -e pause_seconds=$PAUSE_SECONDS \
  -e volume_size=$VOLUME_SIZE \
  -e "$PASSWD_ARG"; then

  echo "AMI_ID=$(cat ami-id.txt)" > ami.properties
  echo "NAME=$(cat name.txt)" >> ami.properties
  echo "WIN_PASSWD=$WIN_PASSWD" >> ami.properties
  echo "Baking complete."
  cat ami.properties
else
  echo "AMI baking failed"
  exit 1
fi

if [ -n "${SHARE_REGIONS}" ]; then
  echo "--------------------- Share to ${SHARE_REGIONS}"
  for region in ${SHARE_REGIONS//,/ } ; do
    var_region_accounts=REGION_${region//-/_}_ACCOUNTS
    if [ ! "${!var_region_accounts}" ]; then
      echo "Missing setting '${var_region_accounts}' in ${infrapropfile}"
      exit 1
    fi
    ndt share-to-another-region $(cat ami-id.txt) ${region} $(cat name.txt) ${!var_region_accounts}
  done
fi
echo "SUCCESS"
