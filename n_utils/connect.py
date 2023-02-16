import os
from collections import OrderedDict

from threadlocal_aws.clients import connect

from n_utils.aws_infra_util import import_scripts, json_load, json_save_small, load_parameters, yaml_save, yaml_to_dict
from n_utils.ndt_project import Project


def deploy_connect_contact_flows(component, contactflowname, dry_run=True):
    subcomponent = Project().get_component(component).get_subcomponent("connect", contactflowname)
    extra_parameters = load_parameters(component=component, connect=contactflowname)
    template = subcomponent.get_dir() + os.sep + "template.yaml"
    flow_defs = yaml_to_dict(template, extra_parameters=extra_parameters)
    if "connectInstanceId" not in flow_defs:
        raise Exception("Missing connect instance id. Define 'connectInstanceId' in the root of your flows template.")

    instance_id = flow_defs["connectInstanceId"]
    flows = get_flows(instance_id)
    if "contactFlows" in flow_defs:
        for flow in flow_defs["contactFlows"]:
            import_scripts(flow, template, extra_parameters=extra_parameters)
            if flow["Name"] in flows:
                flow_id = flows[flow["Name"]]["Id"]
                flow_type = flow["Type"]
                flow_name = flow["Name"]
                flow_tags = flow["Tags"]
                del flow["Name"]
                del flow["Type"]
                del flow["Tags"]
                if "Description" in flow:
                    flow_description = flow["Description"]
                    del flow["Description"]
                flow_content = json_save_small(flow)
                print("Updating flow " + flow_name)
                if not dry_run:
                    try:
                        connect().update_contact_flow_content(
                            InstanceId=instance_id,
                            ContactFlowId=flow_id,
                            Content=flow_content,
                        )
                        connect().update_contact_flow_name(
                            InstanceId=instance_id,
                            ContactFlowId=flow_id,
                            Description=flow_description,
                            Name=flow_name,
                        )
                    except Exception:
                        print("Failed to update flow " + flow_name)
                        print(yaml_save(flow))
            else:
                flow_type = flow["Type"]
                flow_name = flow["Name"]
                flow_tags = flow["Tags"]
                flow_description = None
                del flow["Name"]
                del flow["Type"]
                del flow["Tags"]
                if "Description" in flow:
                    flow_description = flow["Description"]
                    del flow["Description"]
                flow_content = json_save_small(flow)
                print("Creating flow " + flow_name)
                if not dry_run:
                    try:
                        connect().create_contact_flow(
                            InstanceId=instance_id,
                            Name=flow_name,
                            Type=flow_type,
                            Description=flow_description,
                            Content=flow_content,
                            Tags=flow_tags,
                        )
                    except Exception:
                        print("Failed to create flow " + flow_name)
                        print(yaml_save(flow))


def export_connect_contact_flow(instance_id, flowname):
    paginator = connect().get_paginator("list_contact_flows")
    for page in paginator.paginate(InstanceId=instance_id):
        for flow in page["ContactFlowSummaryList"]:
            if flow["Name"] == flowname:
                content = OrderedDict()
                contact_flow = connect().describe_contact_flow(InstanceId=instance_id, ContactFlowId=flow["Id"])[
                    "ContactFlow"
                ]
                content["Name"] = contact_flow["Name"]
                content["Type"] = contact_flow["Type"]
                content["Tags"] = contact_flow["Tags"]
                if "Description" in contact_flow:
                    content["Description"] = contact_flow["Description"]
                content.update(json_load(contact_flow["Content"]))
                return yaml_save(content)


def get_instance_ids():
    ret = []
    paginator = connect().get_paginator("list_instances")
    for page in paginator.paginate():
        for instance in page["InstanceSummaryList"]:
            ret.append(instance["Id"])
    return ret


def get_instance_aliases():
    ret = []
    paginator = connect().get_paginator("list_instances")
    for page in paginator.paginate():
        for instance in page["InstanceSummaryList"]:
            ret.append(instance["InstanceAlias"])
    return ret


def alias_to_id(alias):
    paginator = connect().get_paginator("list_instances")
    for page in paginator.paginate():
        for instance in page["InstanceSummaryList"]:
            if instance["InstanceAlias"] == alias:
                return instance["Id"]
    return None


def get_flows(instance_id):
    existing_flows = OrderedDict()
    paginator = connect().get_paginator("list_contact_flows")
    for page in paginator.paginate(InstanceId=instance_id):
        for flow in page["ContactFlowSummaryList"]:
            existing_flows[flow["Name"]] = flow
    return existing_flows
