from threadlocal_aws.clients import iam


def _aggregate_role_permissions(role_name):
    iam_client = iam()
    all_permissions = []

    # Aggregate managed policies
    managed_policies = iam_client.list_attached_role_policies(RoleName=role_name)["AttachedPolicies"]
    for policy in managed_policies:
        policy_version = iam_client.get_policy_version(
            PolicyArn=policy["PolicyArn"],
            VersionId=iam_client.get_policy(PolicyArn=policy["PolicyArn"])["Policy"]["DefaultVersionId"],
        )["PolicyVersion"]["Document"]
        all_permissions.extend(_extract_permissions(policy_version))

    # Aggregate inline policies
    inline_policies = iam_client.list_role_policies(RoleName=role_name)["PolicyNames"]
    for policy_name in inline_policies:
        policy_document = iam_client.get_role_policy(RoleName=role_name, PolicyName=policy_name)["PolicyDocument"]
        all_permissions.extend(_extract_permissions(policy_document))

    return all_permissions


def _extract_permissions(policy_document):
    permissions = []
    for statement in policy_document.get("Statement", []):
        if statement["Effect"] == "Allow":
            actions = statement.get("Action", [])
            if isinstance(actions, list):
                permissions.extend(actions)
            else:
                permissions.append(actions)
    return permissions


def _check_required_permissions(all_permissions, required_actions):
    return set(required_actions).issubset(set(all_permissions))


def check_role_permissions(role_name, required_actions):
    all_permissions = _aggregate_role_permissions(role_name)
    return _check_required_permissions(all_permissions, required_actions)
