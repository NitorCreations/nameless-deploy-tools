# Template pre-processing

For `ndt deploy-stack`, `ndt deploy-serverless`, `ndt yaml-to-json` and `ndt yaml-to-yaml` there
is a template pre-processing step that is fairly important. The pre-processing implements some
client side functionality that greatly improves the usability and modularisation of stacks and
serverless projects. The flow of the prosessing is roughly as follows:

* Resolve ndt parameters from `*.properties` files along the path to the template. The
  properties files are processed in the following order starting at the root of the workspace
  and continuing to the component level and subcomponent:
    - `branch.properties`
    - `[current-branch].properties`
    - `infra.properties`
    - `infra-[current-branch].properties`
* Properties resolved later in the process override ones resolved earlier
* Expand and resolve the parameter section for the template to get all the parameters
  actually in use in the template
* Expand the rest of the template verifying all parameter references
* All values that use a dynamic parameter notation will be filled in as the template is pre-procesed.
    * There are three types of dynamic parameter notation: `((parameter))`, `$parameter` and `${parameter}`
    * Parameter replacement will not go into CloudFormation function objects (things starting `Fn::`) to
      avoid replacing runtime parameters in included scripts. The double paranthesis `((parameter))` notation
      is the exception to this. Parameters in that notation will be replaced at any level of the template
      including inside functions.
* `Ref: parameter` references will be posted to CloudFormation as-is

Easiest way to test your parameter processing is to run `ndt yaml-to-yaml my/stack-awesome/template.yaml`

## Pre-processing functions

There are a few usefull fuction you can insert and use in the pre-processing phase

### `Fn::ImportYaml`

Imports an external yaml file into the place occupied with this function. Here is an example:

```yaml
Parameters:
  { 'Fn::ImportYaml': ../../common-params.yaml,
      ssh-key: my-key,
      dns: myinstence.example.com,
      zone: example.com.,
      instance: m4.large }

```

The fields in the same object as the function will be used to fill in references with the
notation `((parameter))` in the target yaml. Here is an example of the target:

```yaml
paramSshKeyName:
  Description: SSH key for AMIBakery
  Type: String
  Default: ((ssh-key))
paramDnsName:
  Description: DNS name for AMIBakery
  Type: String
  Default: ((dns))
paramHostedZoneName:
  Description: Route 53 hosted zone name
  Type: String
  Default: ((zone))
paramInstanceType:
  Description: Instance type for AMIBakery
  Type: String
  Default: ((instance))
```

The filename of the import may contain parameters in the form `${parameter}` and that will be resolved
before include.

### `Fn::Merge`

Often you will want to merge an imported yaml snippet into an existing list and this function does that.
Here is an example:

```yaml
Parameters:
  'Fn::Merge':
  - { 'Fn::ImportYaml': ../../common-params.yaml,
      ssh-key: my-key,
      dns: myinstance.example.com,
      zone: nitor.zone.,
      instance: m3.large,
      eip: 51.51.111.91 }
  - paramJenkinsGit:
      Description: git repo for AMIBakery
      Type: String
      Default: ''
```
### `Fn::ImportFile`

Imports a file in place of the function. Useful for files you want to manage externally to the
template as for example userdata shell scripts or AppSync schemas or the like. Importing
does a few useful tricks:

* Resolves parameter references with a few different notations to fit into different scripting files
* Encodes the result into a list of json strings, one string per line and adds in the appropriate escapes

#### Parameter notations

Shell scripts usually most simply can define environment variables with the prefix `CF_` and the
rest of the name will be the name of the parameter that will be inserted as a reference to the value.

Here is an example:
```bash
CF_AWS__StackName=
CF_AWS__Region=
CF_paramAmiName=
CF_paramAdditionalFiles=
CF_paramAmi=
CF_paramDeployToolsVersion=
CF_paramDnsName=
CF_paramEip=
CF_extraScanHosts=`#optional`
CF_paramMvnDeployId=`#optional`
```

This is transformed into
```json
[
  "#!/bin/bash -x\n",
  "\n",
  "CF_AWS__StackName='",
  {
    "Ref": "AWS::StackName"
  },
  "'\n",
  "CF_AWS__Region='",
  {
    "Ref": "AWS::Region"
  },
  "'\n",
  "CF_paramAmiName='",
  {
    "Ref": "paramAmiName"
  },
  "'\n",
  "CF_paramAdditionalFiles='",
  {
    "Ref": "paramAdditionalFiles"
  },
  "'\n",
  "CF_paramAmi='",
  {
    "Ref": "paramAmi"
  },
  "'\n",
  "CF_paramDeployToolsVersion='",
  {
    "Ref": "paramDeployToolsVersion"
  },
  "'\n",
  "CF_paramDnsName='",
  {
    "Ref": "paramDnsName"
  },
  "'\n",
  "CF_paramEip='",
  {
    "Ref": "paramEip"
  },
  "'\n",
  "CF_extraScanHosts='",
  "",
  "'\n",
  "CF_paramMvnDeployId='",
  "",
  "'\n"
]
```

Note how CloudFormation internal parameters are avaible via `CF_AWS__StackName` to `"Ref": "AWS::StackName"`
type transformation. Suffixing a parameter with `#optional` will result in no error being thrown if the
parameter is not present in the stack and in that case the value will simply be empty or the value
given in the script file instead of a reference.

Raw cloudformation json can be inserted with the notation `#CF{ myContent }`. Here is a powershell example:

```powershell
$Env = #CF{ Ref: paramEnvId }
```

Which will be translated when imported into the stack into:
```json
"Fn::Join": [
  "",
  [
    "$Env = '",
    {
      "Ref": "paramEnvId"
    },
    "'\r\n"
  ]
]
```

Also works with javascript type comments:
```javascript
const stackName = //CF{ "Ref": "AWS::StackName" }
```

The third way to insert parameters is via a notation of the type `$CF{parameterName|defaultVal}#optional`. This
references will simply be replaced with a reference to the parameter in place, leaving everything around
it intact. This is handy for example when importing variables into json, where the above comment based
syntax would break json syntax.

An example would be:
```json
{
  "Reference": "$CF{MyLambdaArn}",
  "Name": "MyLambda"
}
```

Which will be translated when imported into the stack into:
```json
"Fn::Join": [
  "",
  [
    "{\n",
    "    \"Reference\": \"",
    {
      "Ref": "MyLambdaArn"
    },
    "\",",
    "    \"Name\": \"MyLambda\"\n",
    "}"
  ]
]
```
### `StackRef`

Gets either a input or output parameter or logical resource of another stack as the value to substitute the
function. Neither parameter nor resources need to be exported to be available, which makes this somewhat
more flexible that CloudFormation native Export/Import. The substitution is completely client-side so
referencing stacks will not be modified in any way if referenced staks change. Later there will be tooling to
manage changes across several stacks in the same repository that refer to eachother. You can run
`ndt show-stack-params-and-outputs [stack-name]` to see the parameters and resources that are available
in each stack.

Here is an example:
```yaml
StackRef:
  region: {Ref: 'AWS::Region'}
  stackName: common-policies-$paramEnvId
  paramName: KMSPolicy
```

You can also insert a StackRef as a value into `infra*.properties` file as yaml on a single line.

### `TFRef`

Gets a value from a terraform state json. Parameters can be addressed through a flattened map that you
can view with the command `ndt show-terraform-params [component] [terraform]` or with a [JMESPath](http://jmespath.org/)
expression.

Here is an example:
```yaml
TFRef:
  component: azure
  terraform: eventhub
  branch: master
  paramName: demo_sa.primary_connection_string
```

`branch` is optional and defaults to the current branch.
You need to specify either `paramName` for the flat map or `jmespath` to use an expression. You can see
the extracted state json with `ndt terraform-pull-state [component] [terraform]`.

You can also insert a TFRef as a value into `*.properties` file as yaml on a single line. An example of that
would be:
```properties
paramAzureVNetCIDR={TFRef: { component: azure-vpn, terraform: azure, paramName: vnet.address_space }}
```

### `AzRef`

Gets a value from an Azure deployment. Parameters can be addressed through a flattened map that you
can view with the command `ndt show-azure-params [component] [azure]`.

Here is an example:
```yaml
AzRef:
  component: vision
  azure: vision
  branch: master
  paramName: paramVisionAPIKey
```

`branch` is optional and defaults to the current branch.

You can also insert a AzRef as a value into `*.properties` file as yaml on a single line. An example of that would be:
```properties
VISION_API_KEY={AzRef: {component: vision, azure: vision, paramName: visionApiKey}}
```

### `Encrypt`

Encrypts the value with a vault key. Can be configured to use a specific vault stack or a specific KMS key. Useful
for example when you want to include sensitive data from Terraform stacks or environment variables.

Here is an example:
```yaml
Encrypt:
  value:
    TFRef:
      component: azure
      terraform: eventhub
      branch: master
      paramName: demo_sa.primary_connection_string
  vault_stack: secret-vault-stack
```

You can also insert a Encrypt as a value into `infra*.properties` file as yaml on a single line.

### Tags

For CloudFormation templates you can add a top level entry `Tags` and that will be given to CloudFormation API
as tags for the stack and all possible resources will be tagged with those tags. Serverless template has
a similar entry `stackTags` under `provider` that functions the same way.

Here is an example (CloudFormation):
```yaml
Tags
  - Key: Environment
    Value: $paramEnvId
```

and serverless:
```yaml
provider:
  name: aws
  runtime: nodejs8.10
  stage: ${opt:stage}
  region: eu-central-1
  stackTags:
    Environment: $paramEnvId
```

## Automatically resolved parameters

There are some parameters that get resolved automatically for CloudFormation stacks and Serverless services.
Please see [the parameters documentation](parameters.md#automatically-resolved-parameters) for details.
