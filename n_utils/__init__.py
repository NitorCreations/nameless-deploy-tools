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

""" Main module for nameless-deploy-tools
"""
import base64

VERSION="1.191"

PATH_COMMANDS = [
    'bin/create-shell-archive.sh',
    'bin/ensure-letsencrypt-certs.sh',
    'bin/lastpass-fetch-notes.sh',
    'bin/lpssh',
    'bin/encrypt-and-mount.sh',
    'bin/mount-and-format.sh',
    'bin/setup-fetch-secrets.sh',
    'bin/ssh-hostkeys-collect.sh'
]
NDT_AND_CONSOLE = [
    'n-include=n_utils.cli:resolve_include',
    'n-include-all=n_utils.cli:resolve_all_includes',
    'cf-logs-to-cloudwatch=ec2_utils.cli:log_to_cloudwatch',
    'logs-to-cloudwatch=ec2_utils.cli:log_to_cloudwatch',
    'associate-eip=n_utils.cli:associate_eip',
    'signal-cf-status=ec2_utils.cli:cf_signal_status',
    'ec2-associate-eip=n_utils.cli:associate_eip'
]
NDT_ONLY = [
    'account-id=ec2_utils.cli:account_id',
    'add-deployer-server=n_utils.cli:add_deployer_server',
    'assume-role=n_utils.cli:assume_role',
    'assumed-role-name=n_utils.cli:cli_assumed_role_name',
    'azure-ensure-group=n_utils.cli:azure_ensure_group',
    'azure-ensure-management-group=n_utils.cli:azure_ensure_management_group',
    'azure-location=n_utils.cli:azure_location',
    'azure-template-parameters=n_utils.cli:azure_template_parameters',
    'cf-delete-stack=n_utils.cli:delete_stack',
    'cf-follow-logs=n_utils.cli:tail_stack_logs',
    'cf-get-parameter=ec2_utils.cli:cf_get_parameter',
    'cf-logical-id=ec2_utils.cli:cf_logical_id',
    'cf-region=ec2_utils.cli:cf_region',
    'cf-signal-status=ec2_utils.cli:cf_signal_status',
    'cf-stack-name=ec2_utils.cli:cf_stack_name',
    'cf-stack-id=ec2_utils.cli:cf_stack_id',
    'create-account=n_utils.cli:cli_create_account',
    'create-stack=n_utils.cf_bootstrap:create_stack',
    'detach-volume=ec2_utils.cli:detach_volume',
    'ec2-clean-snapshots=n_utils.cli:clean_snapshots',
    'ec2-get-tag=ec2_utils.cli:get_tag',
    'ec2-get-userdata=ec2_utils.cli:get_userdata',
    'ec2-instance-id=ec2_utils.cli:instance_id',
    'ec2-region=ec2_utils.cli:region',
    'ec2-wait-for-metadata=ec2_utils.cli:wait_for_metadata',
    'ecr-ensure-repo=n_utils.cli:cli_ecr_ensure_repo',
    'ecr-repo-uri=n_utils.cli:cli_ecr_repo_uri',
    'enable-profile=n_utils.profile_util:cli_enable_profile',
    'get-images=n_utils.cli:cli_get_images',
    'interpolate-file=n_utils.cli:cli_interpolate_file',
    'json-to-yaml=n_utils.cli:json_to_yaml',
    'latest-snapshot=ec2_utils.cli:latest_snapshot',
    'list-components=n_utils.cli:cli_list_components',
    'list-file-to-json=n_utils.cli:list_file_to_json',
    'list-jobs=n_utils.cli:cli_list_jobs',
    'load-parameters=n_utils.cli:cli_load_parameters',
    'logs=ec2_utils.cli:get_logs',
    'mfa-add-token=n_utils.cli:cli_mfa_add_token',
    'mfa-backup=n_utils.cli:cli_mfa_backup_tokens',
    'mfa-code=n_utils.cli:cli_mfa_code',
    'mfa-delete-token=n_utils.cli:cli_mfa_delete_token',
    'mfa-qrcode=n_utils.cli:cli_mfa_to_qrcode',
    'profile-expiry-to-env=n_utils.profile_util:profile_expiry_to_env',
    'profile-to-env=n_utils.profile_util:profile_to_env',
    'promote-image=n_utils.cli:cli_promote_image',
    'pytail=ec2_utils.cli:read_and_follow',
    'read-profile-expiry=n_utils.profile_util:cli_read_profile_expiry',
    'region=ec2_utils.cli:region',
    'register-private-dns=ec2_utils.cli:register_private_dns',
    'session-to-env=n_utils.cli:session_to_env',
    'setup-cli=n_utils.cli:setup_cli',
    'share-to-another-region=n_utils.cli:cli_share_to_another_region',
    'show-stack-params-and-outputs=n_utils.cli:show_stack_params_and_outputs',
    'show-terraform-params=n_utils.cli:show_terraform_params',
    'snapshot-from-volume=ec2_utils.cli:snapshot_from_volume',
    'upsert-cloudfront-records=n_utils.cli:cli_upsert_cloudfront_records',
    'volume-from-snapshot=ec2_utils.cli:volume_from_snapshot',
    'yaml-to-json=n_utils.cli:yaml_to_json',
    'yaml-to-yaml=n_utils.cli:yaml_to_yaml',
    'upsert-codebuild-projects=n_utils.cli:cli_upsert_codebuild_projects',
    'upsert-dns-record=n_utils.cli:upsert_dns_record'
]
NDT_ONLY_SCRIPT = [
    'bake-docker.sh',
    'bake-image.sh',
    'deploy-stack.sh',
    'undeploy-stack.sh',
    'deploy-serverless.sh',
    'undeploy-serverless.sh',
    'deploy-cdk.sh',
    'undeploy-cdk.sh',
    'deploy-terraform.sh',
    'undeploy-terraform.sh',
    'deploy-azure.sh',
    'undeploy-azure.sh',
    'print-create-instructions.sh',
    'terraform-pull-state.sh'
]
CONSOLE_ONLY = [
    'cf-update-stack=n_utils.cli:update_stack',
    'ndt=n_utils.ndt:ndt',
    'nameless-dt-register-complete=n_utils.project_util:ndt_register_complete',
    'nameless-dt-load-project-env=n_utils.project_util:load_project_env',
    'nameless-dt-enable-profile=n_utils.profile_util:cli_enable_profile'
]
CONSOLESCRIPTS = CONSOLE_ONLY + NDT_AND_CONSOLE
COMMAND_MAPPINGS = {}
for script in NDT_ONLY_SCRIPT:
    name = script
    value = "ndtscript"
    if name.endswith(".sh"):
        name = name[:-3]
        value = "ndtshell"
    COMMAND_MAPPINGS[name] = value
for script in NDT_AND_CONSOLE + NDT_ONLY:
    name, value = script.split("=")
    COMMAND_MAPPINGS[name] = value

def _to_str(data):
    ret = data
    decode_method = getattr(data, "decode", None)
    if callable(decode_method):
        try:
            ret = data.decode()
        except:
            ret = _to_str(base64.b64encode(data))
    return str(ret)

def _to_bytes(data):
    ret = data
    encode_method = getattr(data, "encode", None)
    if callable(encode_method):
        ret = data.encode("utf-8")
    return bytes(ret)