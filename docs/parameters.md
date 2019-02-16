# Common parameters

There are a few parameters that affect how you set up your environments and how you
propagate changes through them. The parameters are the settings in `infra*.properties`
files that will be read before a template is pre-processed. The order of the files
processed is as follows:

* `infra.properties`
* `infra-[branch].properties`
* `[component]/infra.properties`
* `[component]/infra-[branch].properties`
* `[component]/(stack-|serverless-)[subcomponent]/infra.properties`
* `[component]/(stack-|serverless-)[subcomponent]/infra-[branch].properties`

Values later in the chain will override earlier values. As you can see, every
other value has the branch name in it. This means that you can change some
values for different branches so that you can account for the mandatory
differences between your environments.

## Important parameters

I will go through some parameters that effect how stacks work.

### `paramEnvId`

This parameter will be a part of default value for stack names, docker
repository urls and tags that mark baked images. This paremeter sets also
the value for the `stage` parameter on serverless projects. 
The default value is the branch name if not set.

### `STACK_NAME`

You can set stack names to follow a scheme or set for each stack separately. For example
if you want to have the stack names start with the branch and then have the subcomponent
name you would set `STACK_NAME=${GIT_BRANCH}-$ORIG_STACK_NAME` in the root `infra.properties`
file. Defaults to `${COMPONENT}-${ORIG_STACK_NAME}-${paramEnvId}`

### `DOCKER_NAME`

Works the same way as `STACK_NAME` for docker repository urls. Defaults to
`[component]/$paramEnvId-$ORIG_DOCKER_NAME`

### `JENKINS_JOB_PREFIX`

The roots of ndt are in baking and deploying stacks via jenkins jobs, but this
parameter has effects besides jenkins jobs. It is part of the default tag that
baked AMI images are found with, which defaults to `${JENKINS_JOB_PREFIX}_[component]_bake`.
If you are using `generate-jobs.groovy` and [Jenkins DSL plugin](https://github.com/jenkinsci/job-dsl-plugin/wiki)
to create jobs for baking and deployments, this parameter is a part of the job
names as above, but also each unique job prefix is given a view with mathching
jobs in it. Defaults to `aws$paramEnvId`.

### `DEPLOY_ROLE_ARN`

The role to assume to run deployments. If this paremeter is defined, then this
role is assumed for Serverless and CloudFormation deployments. Also if defined
and not overridden for AMI and docker bakes, this role will be assumed.

Another way to define the deploy role is to put `assume-deploy-role.sh` on the
path of the user running the operations and the output of that script will be
`eval`'d to assume the desired role.

Defining this variable properly for different branches will give you the
capability of deploying to different accounts from different branches.

If this parameter or the script are not available, the user or the role in the
environment that is running the script is used.

### `BAKE_IMAGE_BRANCH`

This parameter affects how ECR repo uris are resolved are resolved for deploying
CloudFormation stacks and Serverless services. The resolving will use parameters
from this branch to find the correct ECR repo. Also if you are using ndt
automatic CI job generation, the script will generate AMI promote jobs
in other branches instead of actual baking jobs. Also CloudFormation deployment
jobs will be looking for promotion tags and not the original baking tags for
resolving the latest AMI ID in branches other than the baking branch.

The idea is that AMI's and docker images are baked in one branch, tested and then
promoted to other branches.

## Mandatory Baking Parameters

Some parameters affect the way an AMI gets created. The general way this is done
is that an ansible workbook creates and instance based on a base AMI id that you
set for the type of image you want to bake.

### `IMAGETYPE`

Sets the type of image being baked. The parameter is inherited the way all other
parameters are, so you can set a project-wide default and override that as needed.
The supported types are `ubuntu`, `centos` and `windows`

### `AMIID_ubuntu`, `AMIID_centos` and `AMIID_windows`

These are the base AMI ID's that are used to start baking your images. Again
you can have a project-wide default and override as necessary. So the
ansible playbook that creates the image starts with the AMI ID specified
here for the `IMAGETYPE` being baked and runs pre-install scripts, installs
packages, runs post-install script and then creates the image.

### `paramDeployToolsVersion`

The version of nameless-deploy-tools to install. Use `latest` to always install
the latest one or select a version to stay with a specific one. At times
there are alpha releases out, you can also define `alpha` to get the latest
alpha release.

### `AWS_KEY_NAME`

The name of the ssh key to use for baking. The key needs to be uploaded
with the name set in this parameter into the aws console. See
[import-key-pair](https://docs.aws.amazon.com/cli/latest/reference/ec2/import-key-pair.html)
for an example of how to do it from the command line.
The user doing the baking need to have access to the private key
in one of the following ways:

#### `$HOME/.ssh`

The key needs to be in one of
* `$HOME/.ssh/$AWS_KEY_NAME`
* `$HOME/.ssh/$AWS_KEY_NAME.pem`
* `$HOME/.ssh/$AWS_KEY_NAME.rsa`

#### `fetch-secrets.sh`

The key needs to be available in the secret store accessed by `fetch-secrets.sh`
on the users `$PATH` with one of the following keys:
* `$AWS_KEY_NAME`
* `$AWS_KEY_NAME.pem`
* `$AWS_KEY_NAME.rsa`

Users running from personal computers may want to download the key to be
stored locally in their `.ssh` -folder. CI servers often get the key
as a part of deployment or `fetch-secrets.sh` can be set up to access it.

## Optional Baking Parameters

The following parameters are optional in the sense that if you set up
the stacks that ndt provides with their default naming, everything
will be set up properly. If for some reason you don't want to set up
the stacks provided, you can either use non-standard naming or set
up the needed objects manually and define them separately as defined below.
Regardless, the parameters need to be resolvable to id's that are accessible
via the user or role running the baking.

### `BAKE_ROLE_ARN`

You can have a specific role that your baking can assume before using the
AWS apis. This falls back to the the deploy role explained above.
The deploy role typically has broad access permissions, because it needs
to set up and query all of the infrastructure you want to set up,
but the baking role could have a narrower set of permissions. By default
the user or role defined in the environment running the baking is used.

### `NETWORK_STACK`

CloudFormation stack for looking up subnet id for the baking instance to be
placed in. Defaults to `network`. ndt has an easy template to create this
stack.

### `NETWORK_PARAMETER`

The name of the parameter in the network CloudFormation stack that holds the
subnet id for baking. Defaults to `subnetB` for public subnets and `subnetPrivB`
for private subnets.


### `PRIVATE_SUBNET`

If this variable resolves to `no` (the default), the ansible playbook will
connect to the instance being baked via the public ip address of the instance.
If it resolves to `yes` the private ip is used. In the latter case, the
instance running the playbook will have to be in the same VPC or will
have to have set up some other specific access to the private ip, such as
a vpn or direct connect.

### `SUBNET`

You can fix the subnet to be a specific one by defining this parameter.
CloudFormation lookup is not needed in this case.

### `BAKERY_ROLES_STACK`

The CloudFormation stack that holds roles and security groups to be used
in baking. Defaults to `bakery-roles`. ndt has an easy template to create
this stack.

### `SG_PARAM`

The parameter in the bakery-roles stack that holds the id of the security
group to use for baking. Defaults to `bakeInstanceSg` for `ubuntu` and
`centos` and `bakeWinInstanceSg` for `windows`.

### `SECURITY_GROUP`

The security group to use for the instance being baked. If set, no
CloudFormation lookup is needed.

### `INSTANCE_PROFILE_PARAM`

The parameter to look for the ID of the instance profile to set for the instance
being baked. Defaults to `bakeInstanceInstanceprofile`. Looked up from the
same `bakery-roles` stack defined above.

### `AMIBAKE_INSTANCEPROFILE`

The id of the instance profile to set on the baking instance. If set, no
CloudFormation lookup for this is needed.

## Docker baking parameters

Docker baking doesn't have any mandatory parameters. The role assuming
works analogously to the ami baking, so there is `DOCKER_BAKE_ROLE_ARN`
that works the same way as explained above for `BAKE_ROLE_ARN`.
The parameters that do work are optional.

### `DOCKER_NAME`

The name of the ECR repository to push the image to. Defaults to
`[component]/[paramEnvId]-[orig_docker_name]` where orig_docker_name
is the name of the subcomponent directory following the `docker-` -prefix.


## Automatically resolved parameters

CloudFormation stacks and Serverless services can use parameters that
get automatically resolved from docker and AMI baking. For AMI images
there is `paramAmi` and `paramAmiName` that can be used in launching
instances or defining launch configurations. The AMI id in `paramAmi`
can be given on the command line for deploying the stack or the
tag that marks the set of baked AMIs given on the command line is used
to resolve the latest image with that tag. `ndt deploy-stack` has
command-completion to resolve both. The tag defaults to 
`${JENKINS_JOB_PREFIX}_[component]_bake`. Ami id is not available
for serverless deploys.

All docker ECR repo urls for docker images
in the same component are resolved for both Serverless services
and CloudFormation stacks. The ECS uris that you can used in
ECS TaskDefinitions are found in `paramDockerUri[orig_docker_name]`.
A common convertion is to define another parameter 
`paramDockerTag[orig_docker_name]` and use `latest` as the default
value in development environments and override that to a fixed
build number for pre-production and production.
