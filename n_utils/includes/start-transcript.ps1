$ErrorActionPreference="SilentlyContinue"
Stop-Transcript | out-null
$ErrorActionPreference = "Continue"
Start-Transcript -path C:\nameless\cloud-init-output.log
$selfOutput = Start-Job {logs-to-cloudwatch 'C:\nameless\cloud-init-output.log'}
$cfnOutput = Start-Job {logs-to-cloudwatch 'C:\cfn\log\cfn-init.log'}
$ec2configOutput = Start-Job {logs-to-cloudwatch 'C:\Program Files\Amazon\Ec2ConfigService\Logs\Ec2ConfigLog.txt'}
$ec2UserDataOutput = Start-Job {logs-to-cloudwatch 'C:\ProgramData\Amazon\EC2-Windows\Launch\Log\UserdataExecution.log'}
