from n_utils.utils import get_images, read_if_readable


def describe_images(Filters=None):
    assert Filters[0]["Name"] == "tag-value"
    assert Filters[0]["Values"] == ["awsdev_centos_jenkins_bake_*"]
    return {
        "Images": [
            {
                "ProductCodes": [
                    {
                        "ProductCodeId": "aw0evgkw8e5c1q413zgy5pjce",
                        "ProductCodeType": "marketplace",
                    }
                ],
                "Description": "",
                "Tags": [
                    {"Value": "awsdev_centos_jenkins_bake_0001", "Key": "Name"},
                    {"Value": "20180410161338", "Key": "Tstamp"},
                    {
                        "Value": "awstest_centos_jenkins_promote_0001",
                        "Key": "awstest_centos_jenkins_promote",
                    },
                ],
                "VirtualizationType": "hvm",
                "Hypervisor": "xen",
                "EnaSupport": True,
                "SriovNetSupport": "simple",
                "ImageId": "ami-03045e7a",
                "State": "available",
                "BlockDeviceMappings": [
                    {
                        "DeviceName": "/dev/sda1",
                        "Ebs": {
                            "Encrypted": False,
                            "DeleteOnTermination": True,
                            "VolumeType": "gp3",
                            "VolumeSize": 8,
                            "SnapshotId": "snap-0a112c2708d4a1d16",
                        },
                    }
                ],
                "Architecture": "x86_64",
                "ImageLocation": "832585949989/awsdev_centos_jenkins_bake_0001",
                "RootDeviceType": "ebs",
                "OwnerId": "832585949989",
                "RootDeviceName": "/dev/sda1",
                "CreationDate": "2018-04-10T13:22:11.000Z",
                "Public": False,
                "ImageType": "machine",
                "Name": "awsdev_centos_jenkins_bake_0001",
            },
            {
                "ProductCodes": [
                    {
                        "ProductCodeId": "aw0evgkw8e5c1q413zgy5pjce",
                        "ProductCodeType": "marketplace",
                    }
                ],
                "Description": "",
                "Tags": [
                    {
                        "Value": "aws_centos_jenkins_promote_0001",
                        "Key": "aws_centos_jenkins_promote",
                    },
                    {"Value": "awsdev_centos_jenkins_bake_0031", "Key": "Name"},
                    {"Value": "20180510103015", "Key": "Tstamp"},
                ],
                "VirtualizationType": "hvm",
                "Hypervisor": "xen",
                "EnaSupport": True,
                "SriovNetSupport": "simple",
                "ImageId": "ami-3fdfe846",
                "State": "available",
                "BlockDeviceMappings": [
                    {
                        "DeviceName": "/dev/sda1",
                        "Ebs": {
                            "Encrypted": False,
                            "DeleteOnTermination": True,
                            "VolumeType": "gp3",
                            "VolumeSize": 8,
                            "SnapshotId": "snap-037ed955e6363bab7",
                        },
                    }
                ],
                "Architecture": "x86_64",
                "ImageLocation": "832585949989/awsdev_centos_jenkins_bake_0031",
                "RootDeviceType": "ebs",
                "OwnerId": "832585949989",
                "RootDeviceName": "/dev/sda1",
                "CreationDate": "2018-05-10T07:41:11.000Z",
                "Public": False,
                "ImageType": "machine",
                "Name": "awsdev_centos_jenkins_bake_0031",
            },
            {
                "ProductCodes": [
                    {
                        "ProductCodeId": "aw0evgkw8e5c1q413zgy5pjce",
                        "ProductCodeType": "marketplace",
                    }
                ],
                "Description": "",
                "Tags": [
                    {"Value": "awsdev_centos_jenkins_bake_0032", "Key": "Name"},
                    {"Value": "20180623181343", "Key": "Tstamp"},
                ],
                "VirtualizationType": "hvm",
                "Hypervisor": "xen",
                "EnaSupport": True,
                "SriovNetSupport": "simple",
                "ImageId": "ami-4dddd2a7",
                "State": "available",
                "BlockDeviceMappings": [
                    {
                        "DeviceName": "/dev/sda1",
                        "Ebs": {
                            "Encrypted": False,
                            "DeleteOnTermination": True,
                            "VolumeType": "gp3",
                            "VolumeSize": 8,
                            "SnapshotId": "snap-06a4decdcb0904550",
                        },
                    }
                ],
                "Architecture": "x86_64",
                "ImageLocation": "832585949989/awsdev_centos_jenkins_bake_0032",
                "RootDeviceType": "ebs",
                "OwnerId": "832585949989",
                "RootDeviceName": "/dev/sda1",
                "CreationDate": "2018-06-23T15:23:51.000Z",
                "Public": False,
                "ImageType": "machine",
                "Name": "awsdev_centos_jenkins_bake_0032",
            },
        ]
    }


CALLER_IDENTITY = {
    "UserId": "BPAIDAJNYSZAKD7QO3N6T",
    "Account": "377074220690",
    "Arn": "arn:aws:iam::377074220690:user/foo@nitor.com",
    "ResponseMetadata": {
        "RequestId": "83592c1a-9494-11e8-a008-4f746bcda707",
        "HTTPStatusCode": 200,
        "HTTPHeaders": {
            "x-amzn-requestid": "83592c1a-9494-11e8-a008-4f746bcda707",
            "content-type": "text/xml",
            "content-length": "422",
            "date": "Tue, 31 Jul 2018 07:37:01 GMT",
        },
        "RetryAttempts": 0,
    },
}


def test_get_images(mocker, ec2):
    ec2.describe_images = describe_images
    images = get_images("awsdev_centos_jenkins_bake")
    assert images[0]["Name"] == "awsdev_centos_jenkins_bake_0032"
    assert images[2]["Name"] == "awsdev_centos_jenkins_bake_0001"


def test_read_if_readble_not_exists():
    assert read_if_readable("foo.txt") == ""


def test_read_if_readble_exists():
    assert "<ns0:project" in read_if_readable("n_utils/tests/pom.xml")
