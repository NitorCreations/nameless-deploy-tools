#!/usr/bin/env python


# Copyright 2023 Nitor Creations Oy
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

import signal
import time

from subprocess import Popen
from typing import Union

from botocore.exceptions import ClientError
from threadlocal_aws.clients import ecs

from n_utils.iam_utils import check_role_permissions


def ecs_describe_clusters():
    """list clusters with service and task count"""
    clusters = ecs().list_clusters()
    clusters = ecs().describe_clusters(clusters=clusters["clusterArns"])

    return clusters["clusters"]


def ecs_describe_services(cluster: str):
    """describe single cluster with list of services and task count"""
    try:
        services = ecs().list_services(cluster=cluster)
    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code == "ClusterNotFoundException":
            print(f"Error: Cluster {cluster} not found")
            return []
        else:
            raise e
    services = ecs().describe_services(cluster=cluster, services=services["serviceArns"])
    return services["services"]


def ecs_describe_tasks(cluster: str, service: str):
    """list tasks for a service"""
    try:
        tasks = ecs().list_tasks(cluster=cluster, serviceName=service)["taskArns"]
    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code == "ClusterNotFoundException":
            print(f"Error: Cluster {cluster} not found")
            return []
        elif error_code == "ServiceNotFoundException":
            print(f"Error: Service {service} not found")
            return []
        else:
            raise e
    tasks: list[dict] = ecs().describe_tasks(cluster=cluster, tasks=tasks)["tasks"]
    tasks.sort(key=lambda x: x["createdAt"])
    return tasks


def ecs_cluster_has_exec_capability(cluster: str):
    """check if ecs cluster has container-instance that has platform attribute ecs.capability.execute-command"""
    attributes = ecs().list_attributes(
        cluster=cluster, targetType="container-instance", attributeName="ecs.capability.execute-command"
    )["attributes"]
    for attribute in attributes:
        if attribute["name"] == "ecs.capability.execute-command":
            return True
    return False


def _get_task_list(
    cluster: str, service: str, filter_task: Union[str, None] = None, filter_execute_command: bool = False
):
    task_list = ecs_describe_tasks(cluster, service)
    if filter_task is not None:
        task_list = [t for t in task_list if t["taskArn"].split("/")[-1] == filter_task]
    if filter_execute_command:
        task_list = [t for t in task_list if t["enableExecuteCommand"]]
    task_list.sort(key=lambda x: x["enableExecuteCommand"], reverse=True)
    return task_list


def _check_ssm_messages_permissions(task_iam_role: str):
    """check if task has permissions to read ssm messages"""
    return check_role_permissions(
        task_iam_role,
        [
            "ssmmessages:CreateControlChannel",
            "ssmmessages:CreateDataChannel",
            "ssmmessages:OpenControlChannel",
            "ssmmessages:OpenDataChannel",
        ],
    )


def ecs_execute_command(cluster: str, service: str, command: str, task_str: Union[str, None], interactive: bool = True):
    provided_own_task = task_str is not None
    try:
        task_list = _get_task_list(cluster, service, task_str)
    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code == "ClusterNotFoundException":
            print(f"Error: Cluster {cluster} not found")
            return
        elif error_code == "ServiceNotFoundException":
            print(f"Error: Service {service} not found")
            return
        else:
            raise e

    if len(task_list) == 0:
        print(
            f"Error: No running task found for service {service}"
            + (f" and task {task_str}" if task_str is not None else "")
        )
        return

    task = task_list[0]
    if task["launchType"] == "EC2":
        task_definition = ecs().describe_task_definition(taskDefinition=task["taskDefinitionArn"])["taskDefinition"]
        if not _check_ssm_messages_permissions(task_definition["taskRoleArn"].split("/")[-1]):
            print(
                f"Error task {task['taskArn'].split('/')[-1]} does not have required SSM permissions.\n"
                "See https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-iam-roles.html#ecs-exec-required-iam-permissions"  # noqa: E501
            )
            return

    if not task["enableExecuteCommand"]:
        print(f"Error: Task {task['taskArn']} does not have execute command enabled")
        if task["launchType"] == "EC2" and not ecs_cluster_has_exec_capability(cluster):
            print(
                f"Error: Cluster {cluster} does not have ecs.capability.execute-command capability, "
                "please make sure that your cluster has a container instance with this capability"
            )
            return

        if input("Do you want to enable it? This will make a redeployment (y/N)") == "y":
            ecs().update_service(cluster=cluster, service=service, enableExecuteCommand=True, forceNewDeployment=True)
            print("Service updated, waiting for deployment to finish")
            time.sleep(5)
            waiter = ecs().get_waiter("services_stable")
            waiter.wait(cluster=cluster, services=[service])
            if provided_own_task:
                print("New task started, ignoring provided task as it is no longer valid")
            task = _get_task_list(cluster, service, None, True)[0]
            if len(task_list) == 0:
                print(
                    f"Error: No running task found for service {service}"
                    + (f" and task {task_str}" if task_str is not None else "")
                )
                return
        else:
            return

    print(f"Executing command {command} on task {task['taskArn'].split('/')[-1]}")
    command = [
        "aws",
        "ecs",
        "execute-command",
        "--cluster",
        cluster,
        "--task",
        task["taskArn"],
        "--command",
        command,
    ]
    if interactive:
        command.append("--interactive")

    p = Popen(command)
    # while process is open, catch CTRL-C signals and pass those through to the SSM
    while p.poll() is None:
        try:
            p.communicate()
        except KeyboardInterrupt:
            p.send_signal(signal.SIGINT)
