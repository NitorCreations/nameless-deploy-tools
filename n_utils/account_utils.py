from __future__ import print_function
from __future__ import absolute_import
import os
import boto3
from time import time, sleep
from ec2_utils.clients import region
from n_utils import utils
from n_utils import cf_deploy
from n_utils.ndt import find_include

def create_account(email, account_name, role_name="OrganizationAccountAccessRole",
                   trust_role="TrustedAccountAccessRole",
                   access_to_billing=True, trusted_accounts=None, mfa_token=None):
    if access_to_billing:
        access = "ALLOW"
    else:
        access = "DENY"
    timeout = 300

    if trusted_accounts:
        trusted_roles = {}
        for trusted_account in trusted_accounts:
            role_arn = find_role_arn(trusted_account)
            if not role_arn:
                raise Exception("Failed to resolve trusted account " + trusted_account)
            trusted_roles[trusted_account] = role_arn

    client = boto3.client('organizations')
    response = client.create_account(Email=email, AccountName=account_name,
                                     RoleName=role_name, IamUserAccessToBilling=access)
    if 'CreateAccountStatus' in response and 'Id' in response['CreateAccountStatus']:
        create_account_id = response['CreateAccountStatus']['Id']
        startTime = time()
        status = response['CreateAccountStatus']['State']
        while time() - startTime < timeout and not status == "SUCCEEDED":
            if response['CreateAccountStatus']['State'] == "FAILED":
                raise Exception("Account creation failed: " + response['CreateAccountStatus']['FailureReason'])
            print("Waiting for account creation to finish")
            sleep(2)
            response = client.describe_create_account_status(CreateAccountRequestId=create_account_id)
            status = response['CreateAccountStatus']['State']
        if time() - startTime > timeout and not status == "SUCCEEDED":
            raise Exception("Timed out waiting to create account " + response['CreateAccountStatus']['State'])
        account_id = response['CreateAccountStatus']['AccountId']

    os.environ['paramManagedAccount'] = account_id
    os.environ['paramManageRole'] = role_name
    template = find_include("manage-account.yaml")
    cf_deploy.deploy("managed-account-" + account_name + "-" + account_id, template, region())

    if trusted_accounts:
        role_arn = "arn:aws:iam::" + account_id + ":role/" + role_name
        assumed_creds = utils.assume_role(role_arn, mfa_token_name=mfa_token)
        session = boto3.session.Session(aws_access_key_id=assumed_creds['AccessKeyId'],
                                        aws_secret_access_key=assumed_creds['SecretAccessKey'],
                                        aws_session_token=assumed_creds['SessionToken'])
        for trusted_account in trusted_accounts:
            os.environ['paramTrustedAccount'] = trusted_roles[trusted_account].split(":")[4]
            os.environ['paramRoleName'] = trust_role
            template = find_include("trust-account-role.yaml")
            cf_deploy.deploy("trust-" + trusted_account, template, utils.region(), session=session)
        template = find_include("manage-account.yaml")
        for trusted_account in trusted_accounts:
            role_arn = trusted_roles[trusted_account]
            print("Assuming role " + role_arn)
            session = boto3.session.Session()
            assumed_creds = utils.assume_role(role_arn, mfa_token_name=mfa_token)
            session = boto3.session.Session(aws_access_key_id=assumed_creds['AccessKeyId'],
                                            aws_secret_access_key=assumed_creds['SecretAccessKey'],
                                            aws_session_token=assumed_creds['SessionToken'])
            os.environ['paramManagedAccount'] = account_id
            os.environ['paramRoleName'] = trust_role
            cf_deploy.deploy("managed-account-" + account_name + "-" + account_id,
                             template, region(), session=session)


def find_role_arn(trusted_account):
    cf_stacks = boto3.client("cloudformation").get_paginator('describe_stacks')
    for page in cf_stacks.paginate():
        for stack in page["Stacks"]:
            if stack["StackName"].endswith(trusted_account) or \
               "-" + trusted_account + "-" in stack["StackName"]:
                for output in stack["Outputs"]:
                    if output["OutputKey"] == "ManageRole":
                        return output["OutputValue"]
    return None


def list_created_accounts():
    cf_stacks = boto3.client("cloudformation").get_paginator('describe_stacks')
    for page in cf_stacks.paginate():
        for stack in page["Stacks"]:
            if stack["StackName"].startswith("managed-account-"):
                yield "-".join(stack["StackName"].split("-")[2:-1])
