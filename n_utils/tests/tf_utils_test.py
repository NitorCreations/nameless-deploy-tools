from n_utils.tf_utils import flat_state, jmespath_var

state = """{
    "version": 3,
    "terraform_version": "0.11.11",
    "serial": 6,
    "lineage": "456851f3-139e-b8dd-429e-6d2c5ec86b46",
    "modules": [
        {
            "path": [
                "root"
            ],
            "outputs": {
                "connection_string": {
                    "sensitive": true,
                    "type": "string",
                    "value": "Endpoint=sb://demons-master.servicebus.windows.net/;SharedAccessKeyName=demoAuthRule-master;Foo=Bar;EntityPath=demoEH-master"
                }
            },
            "resources": {
                "azurerm_eventhub.demo_eh": {
                    "type": "azurerm_eventhub",
                    "depends_on": [
                        "azurerm_eventhub_namespace.demo_ns",
                        "azurerm_resource_group.demo_rg",
                        "azurerm_storage_account.demo_sa",
                        "azurerm_storage_blob.demo_blob"
                    ],
                    "primary": {
                        "id": "/subscriptions/Dib/resourceGroups/demoRG-master/providers/Microsoft.EventHub/namespaces/demoNS-master/eventhubs/demoEH-master",
                        "attributes": {
                            "capture_description.#": "1",
                            "capture_description.0.destination.#": "1",
                            "capture_description.0.destination.0.archive_name_format": "{Namespace}/{EventHub}/{PartitionId}/{Year}/{Month}/{Day}/{Hour}/{Minute}/{Second}",
                            "capture_description.0.destination.0.blob_container_name": "demo-blob-master",
                            "capture_description.0.destination.0.name": "EventHubArchive.AzureBlockBlob",
                            "capture_description.0.destination.0.storage_account_id": "/subscriptions/Dib/resourceGroups/demoRG-master/providers/Microsoft.Storage/storageAccounts/demosamaster",
                            "capture_description.0.enabled": "true",
                            "capture_description.0.encoding": "AvroDeflate",
                            "capture_description.0.interval_in_seconds": "300",
                            "capture_description.0.size_limit_in_bytes": "314572800",
                            "id": "/subscriptions/Dib/resourceGroups/demoRG-master/providers/Microsoft.EventHub/namespaces/demoNS-master/eventhubs/demoEH-master",
                            "message_retention": "1",
                            "name": "demoEH-master",
                            "namespace_name": "demoNS-master",
                            "partition_count": "2",
                            "partition_ids.#": "2",
                            "partition_ids.2212294583": "1",
                            "partition_ids.4108050209": "0",
                            "resource_group_name": "demoRG-master"
                        },
                        "meta": {},
                        "tainted": false
                    },
                    "deposed": [],
                    "provider": "provider.azurerm"
                },
                "azurerm_eventhub_authorization_rule.demo_auth_rule": {
                    "type": "azurerm_eventhub_authorization_rule",
                    "depends_on": [
                        "azurerm_eventhub.demo_eh",
                        "azurerm_eventhub_namespace.demo_ns",
                        "azurerm_resource_group.demo_rg"
                    ],
                    "primary": {
                        "id": "/subscriptions/Dib/resourceGroups/demoRG-master/providers/Microsoft.EventHub/namespaces/demoNS-master/eventhubs/demoEH-master/authorizationRules/demoAuthRule-master",
                        "attributes": {
                            "eventhub_name": "demoEH-master",
                            "id": "/subscriptions/Dib/resourceGroups/demoRG-master/providers/Microsoft.EventHub/namespaces/demoNS-master/eventhubs/demoEH-master/authorizationRules/demoAuthRule-master",
                            "listen": "true",
                            "manage": "true",
                            "name": "demoAuthRule-master",
                            "namespace_name": "demoNS-master",
                            "primary_connection_string": "Endpoint=sb://demons-master.servicebus.windows.net/;SharedAccessKeyName=demoAuthRule-master;Foo=Bar;EntityPath=demoEH-master",
                            "primary_key": "Bar",
                            "resource_group_name": "demoRG-master",
                            "secondary_connection_string": "Endpoint=sb://demons-master.servicebus.windows.net/;SharedAccessKeyName=demoAuthRule-master;SharedAccessKey=Dob;EntityPath=demoEH-master",
                            "secondary_key": "Dob",
                            "send": "true"
                        },
                        "meta": {},
                        "tainted": false
                    },
                    "deposed": [],
                    "provider": "provider.azurerm"
                },
                "azurerm_eventhub_consumer_group.demo_consumer_group": {
                    "type": "azurerm_eventhub_consumer_group",
                    "depends_on": [
                        "azurerm_eventhub.demo_eh",
                        "azurerm_eventhub_namespace.demo_ns",
                        "azurerm_resource_group.demo_rg"
                    ],
                    "primary": {
                        "id": "/subscriptions/Dib/resourceGroups/demoRG-master/providers/Microsoft.EventHub/namespaces/demoNS-master/eventhubs/demoEH-master/consumergroups/demoCG-master",
                        "attributes": {
                            "eventhub_name": "demoEH-master",
                            "id": "/subscriptions/Dib/resourceGroups/demoRG-master/providers/Microsoft.EventHub/namespaces/demoNS-master/eventhubs/demoEH-master/consumergroups/demoCG-master",
                            "name": "demoCG-master",
                            "namespace_name": "demoNS-master",
                            "resource_group_name": "demoRG-master",
                            "user_metadata": "demo-meta-data"
                        },
                        "meta": {},
                        "tainted": false
                    },
                    "deposed": [],
                    "provider": "provider.azurerm"
                },
                "azurerm_eventhub_namespace.demo_ns": {
                    "type": "azurerm_eventhub_namespace",
                    "depends_on": [
                        "azurerm_resource_group.demo_rg"
                    ],
                    "primary": {
                        "id": "/subscriptions/Dib/resourceGroups/demoRG-master/providers/Microsoft.EventHub/namespaces/demoNS-master",
                        "attributes": {
                            "auto_inflate_enabled": "false",
                            "capacity": "1",
                            "default_primary_connection_string": "Endpoint=sb://demons-master.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=Fob",
                            "default_primary_key": "Fob",
                            "default_secondary_connection_string": "Endpoint=sb://demons-master.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=Bor",
                            "default_secondary_key": "Bor",
                            "id": "/subscriptions/Dib/resourceGroups/demoRG-master/providers/Microsoft.EventHub/namespaces/demoNS-master",
                            "kafka_enabled": "false",
                            "location": "westeurope",
                            "maximum_throughput_units": "0",
                            "name": "demoNS-master",
                            "resource_group_name": "demoRG-master",
                            "sku": "Standard",
                            "tags.%": "1",
                            "tags.environment": "Demo"
                        },
                        "meta": {},
                        "tainted": false
                    },
                    "deposed": [],
                    "provider": "provider.azurerm"
                },
                "azurerm_resource_group.demo_rg": {
                    "type": "azurerm_resource_group",
                    "depends_on": [],
                    "primary": {
                        "id": "/subscriptions/Dib/resourceGroups/demoRG-master",
                        "attributes": {
                            "id": "/subscriptions/Dib/resourceGroups/demoRG-master",
                            "location": "westeurope",
                            "name": "demoRG-master",
                            "tags.%": "0"
                        },
                        "meta": {},
                        "tainted": false
                    },
                    "deposed": [],
                    "provider": "provider.azurerm"
                },
                "azurerm_storage_account.demo_sa": {
                    "type": "azurerm_storage_account",
                    "depends_on": [
                        "azurerm_resource_group.demo_rg"
                    ],
                    "primary": {
                        "id": "/subscriptions/Dib/resourceGroups/demoRG-master/providers/Microsoft.Storage/storageAccounts/demosamaster",
                        "attributes": {
                            "access_tier": "",
                            "account_encryption_source": "Microsoft.Storage",
                            "account_kind": "Storage",
                            "account_replication_type": "LRS",
                            "account_tier": "Standard",
                            "account_type": "Standard_LRS",
                            "enable_blob_encryption": "true",
                            "enable_file_encryption": "true",
                            "enable_https_traffic_only": "false",
                            "id": "/subscriptions/Dib/resourceGroups/demoRG-master/providers/Microsoft.Storage/storageAccounts/demosamaster",
                            "identity.#": "0",
                            "location": "westeurope",
                            "name": "demosamaster",
                            "network_rules.#": "0",
                            "primary_access_key": "Baz",
                            "primary_blob_connection_string": "DefaultEndpointsProtocol=https;BlobEndpoint=https://demosamaster.blob.core.windows.net/;AccountName=demosamaster;AccountKey=Baz",
                            "primary_blob_endpoint": "https://demosamaster.blob.core.windows.net/",
                            "primary_connection_string": "DefaultEndpointsProtocol=https;AccountName=demosamaster;AccountKey=Baz;EndpointSuffix=core.windows.net",
                            "primary_file_endpoint": "https://demosamaster.file.core.windows.net/",
                            "primary_location": "westeurope",
                            "primary_queue_endpoint": "https://demosamaster.queue.core.windows.net/",
                            "primary_table_endpoint": "https://demosamaster.table.core.windows.net/",
                            "resource_group_name": "demoRG-master",
                            "secondary_access_key": "Zab",
                            "secondary_connection_string": "DefaultEndpointsProtocol=https;AccountName=demosamaster;AccountKey=Zab;EndpointSuffix=core.windows.net",
                            "secondary_location": "",
                            "tags.%": "0"
                        },
                        "meta": {
                            "schema_version": "2"
                        },
                        "tainted": false
                    },
                    "deposed": [],
                    "provider": "provider.azurerm"
                },
                "azurerm_storage_blob.demo_blob": {
                    "type": "azurerm_storage_blob",
                    "depends_on": [
                        "azurerm_resource_group.demo_rg",
                        "azurerm_storage_account.demo_sa",
                        "azurerm_storage_container.demo_container"
                    ],
                    "primary": {
                        "id": "https://demosamaster.blob.core.windows.net/demo-container-master/demo-blob-master",
                        "attributes": {
                            "attempts": "1",
                            "content_type": "application/octet-stream",
                            "id": "https://demosamaster.blob.core.windows.net/demo-container-master/demo-blob-master",
                            "name": "demo-blob-master",
                            "parallelism": "8",
                            "resource_group_name": "demoRG-master",
                            "size": "5120",
                            "source_uri": "",
                            "storage_account_name": "demosamaster",
                            "storage_container_name": "demo-container-master",
                            "type": "page",
                            "url": "https://demosamaster.blob.core.windows.net/demo-container-master/demo-blob-master"
                        },
                        "meta": {
                            "schema_version": "1"
                        },
                        "tainted": false
                    },
                    "deposed": [],
                    "provider": "provider.azurerm"
                },
                "azurerm_storage_container.demo_container": {
                    "type": "azurerm_storage_container",
                    "depends_on": [
                        "azurerm_resource_group.demo_rg",
                        "azurerm_storage_account.demo_sa"
                    ],
                    "primary": {
                        "id": "https://demosamaster.blob.core.windows.net/demo-container-master",
                        "attributes": {
                            "container_access_type": "private",
                            "id": "https://demosamaster.blob.core.windows.net/demo-container-master",
                            "name": "demo-container-master",
                            "properties.%": "4",
                            "properties.last_modified": "Wed, 27 Feb 2019 21:11:50 GMT",
                            "properties.lease_duration": "",
                            "properties.lease_state": "available",
                            "properties.lease_status": "unlocked",
                            "resource_group_name": "demoRG-master",
                            "storage_account_name": "demosamaster"
                        },
                        "meta": {
                            "schema_version": "1"
                        },
                        "tainted": false
                    },
                    "deposed": [],
                    "provider": "provider.azurerm"
                }
            },
            "depends_on": []
        }
    ]
}
"""

def test_flat_state(mocker):
    state_doc = flat_state(state)
    assert state_doc["demo_sa.id"] == "/subscriptions/Dib/resourceGroups/demoRG-master/providers/Microsoft.Storage/storageAccounts/demosamaster"
    assert state_doc["connection_string"] == "Endpoint=sb://demons-master.servicebus.windows.net/;SharedAccessKeyName=demoAuthRule-master;Foo=Bar;EntityPath=demoEH-master"

def test_jmespath_var(mocker):
    assert jmespath_var(state, 'modules[].resources."azurerm_eventhub.demo_eh".primary.attributes.name') == "demoEH-master"
