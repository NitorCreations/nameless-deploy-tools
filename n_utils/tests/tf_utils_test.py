from n_utils.tf_utils import flat_state, jmespath_var
import json

state = json.loads(
    """
{
  "version": 4,
  "terraform_version": "0.13.2",
  "serial": 1,
  "lineage": "d05c7d4d-c56f-1cf4-91fc-414db0a3bf77",
  "outputs": {
    "sns_platform_app_arn": {
      "value": "arn:aws:sns:eu-central-1:00000000:app/GCM/EhMobileDev",
      "type": "string"
    }
  },
  "resources": [
    {
      "mode": "data",
      "type": "aws_secretsmanager_secret_version",
      "name": "fb_key",
      "provider": "provider[\\"registry.terraform.io/hashicorp/aws\\"]",
      "instances": [
        {
          "schema_version": 0,
          "attributes": {
            "arn": "arn:aws:secretsmanager:eu-central-1:00000000:secret:dev/mobile-backend/firebase-server-key-ZxJf9U",
            "id": "dev/mobile-backend/firebase-server-key|AWSCURRENT",
            "secret_binary": "",
            "secret_id": "dev/mobile-backend/firebase-server-key",
            "secret_string": "FOOBAR",
            "version_id": "9f45c930-aef6-46f2-8c1a-444a9553b93c",
            "version_stage": "AWSCURRENT",
            "version_stages": [
              "AWSCURRENT"
            ]
          }
        }
      ]
    },
    {
      "mode": "managed",
      "type": "aws_sns_platform_application",
      "name": "sns_gcm_application",
      "provider": "provider[\\"registry.terraform.io/hashicorp/aws\\"]",
      "instances": [
        {
          "schema_version": 0,
          "attributes": {
            "arn": "arn:aws:sns:evu-central-1:00000000:app/GCM/EhMobileDev",
            "event_delivery_failure_topic_arn": null,
            "event_endpoint_created_topic_arn": null,
            "event_endpoint_deleted_topic_arn": null,
            "event_endpoint_updated_topic_arn": null,
            "failure_feedback_role_arn": null,
            "id": "arn:aws:sns:eu-central-1:00000000:app/GCM/EhMobileDev",
            "name": "EhMobileDev",
            "platform": "GCM",
            "platform_credential": "FOOBAR",
            "platform_principal": null,
            "success_feedback_role_arn": null,
            "success_feedback_sample_rate": null
          },
          "private": "bnVsbA==",
          "dependencies": [
            "data.aws_secretsmanager_secret_version.fb_key"
          ]
        }
      ]
    }
  ]
}

"""
)


def test_flat_state(mocker):
    state_doc = flat_state(state)
    assert (
        state_doc["sns_platform_app_arn"]
        == "arn:aws:sns:eu-central-1:00000000:app/GCM/EhMobileDev"
    )
    assert state_doc["sns_gcm_application.platform_credential"] == "FOOBAR"


def test_jmespath_var(mocker):
    assert (
        jmespath_var(
            state,
            "resources[?name == 'sns_gcm_application'].instances[0].attributes.arn",
        )
        == "arn:aws:sns:evu-central-1:00000000:app/GCM/EhMobileDev"
    )
