Stop-Job $selfOutput.Id
Stop-Job $cfnOutput.Id
Stop-Job $ec2configOutput.Id
Stop-Job $ec2UserDataOutput.Id
Remove-Job $selfOutput.Id
Remove-Job $cfnOutput.Id
Remove-Job $ec2configOutput.Id
Remove-Job $ec2UserDataOutput.Id
Stop-Transcript
