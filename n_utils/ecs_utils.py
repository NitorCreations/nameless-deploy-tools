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

import time
from botocore.exceptions import ClientError
from threadlocal_aws.clients import ecs
from typing import Union


def ecs_describe_clusters():
    """list clusters with service and task count"""
    clusters = ecs().list_clusters()
    clusters = ecs().describe_clusters(clusters=clusters["clusterArns"])

    return clusters["clusters"]


def ecs_describe_cluster(cluster: str):
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
    tasks = ecs().describe_tasks(cluster=cluster, tasks=tasks)["tasks"]
    return tasks


