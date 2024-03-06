# Base image

CentOS 8 doesn't (yet) have an AWS marketplace product so we need to get the latest by owner and name (probably in /infra-dev.properties)

```diff
-AMIID_centos=ProductAmi: aw0evgkw8e5c1q413zgy5pjce
+AMIID_centos=OwnerNamedAmi: { owner: "125523088429", name: "CentOS 8.*x86_64" }
+VOLUME_SIZE=10

```

Also the root volume needs to be 10G now instead of the old 8G

# Rocky linux

Support for CentOS 8 will end abruptly at the end of 2021, so a fully compatible version with a stable future is Rocky linux. You simply switch the image type to rocky and define a new base image:

```diff
-IMAGETYPE=centos
+IMAGETYPE=rocky
+AMIID_rocky=ProductAmi: cotnnspjrsi38lfn8qo4ibnnm
```

The only significant difference is that the default user will be `rocky` instead of `centos`.

# Packages

Places will have different package repos for CentOS 8. They are pretty well available already. Here's an example for node (also upgrade node to current version while you are at it)

```diff
-safe_download https://rpm.nodesource.com/pub_12.x/el/7/x86_64/nodejs-12.14.1-1nodesource.x86_64.rpm 34ec81a11d752eb9f52db9dbc4349102e890f11d3a53239f596c5ec1277cd210 nodejs.rpm &
+safe_download https://rpm.nodesource.com/pub_16.x/el/8/x86_64/nodejs-16.8.0-1nodesource.x86_64.rpm e0cf02059f46b06c0f1ef919b37326b17f4222215631fc7427f5b128c2457979 nodejs.rpm & &

```

dnf no longer accepts non-signed packages by default - so can't mix those in packages.txt. You can use dnf command in pre\_install.sh or post\_install.sh instead:

```diff
+dnf install -y https://s3.amazonaws.com/ec2-downloads-windows/SSMAgent/latest/linux_amd64/amazon-ssm-agent.rpm
+dnf install -y https://github.com/NitorCreations/aws-ec2-instance-connect-config/releases/download/v1.1-10/ec2-instance-connect-1.1-10.noarch.rpm
```

# Docker

Docker packages for CentOS don't pull containderd.io

```diff
+safe_download https://download.docker.com/linux/centos/7/x86_64/stable/Packages/containerd.io-1.2.6-3.3.el7.x86_64.rpm 90679e91563f72708b5fe9c21acb2d1788b7fddbc796b86d55d67a04aad2278b containerd.io.rpm
+dnf install -y containerd.io.rpm
+rm -f containerd.io.rpm
```

Docker interaction with firewalld is broken [https://github.com/docker/for-linux/issues/957](https://github.com/docker/for-linux/issues/957)

Fix is to enable masquerade for the docker network interface

```diff
+firewall-cmd --zone=public --add-masquerade --permanentfirewall-cmd --reload

```

You can do that in either post\_install.sh or userdata.sh. If you do it in post\_install.sh, make sure firewalld is running

```diff
+systemctl start --now firewalld
```

# Python

The bake installs python3 by default and makes that the default via alternatives. The following packages are no longer needed nor available:

```diff
-python-pip
-python-crypto
-python-devel
-python3
```

pip is also python 3.6 by default so no need to use pip3 for some packages. Everything should now install to the system default python 3.6

# Jenkins

The init scripts for jenkins use /etc/init.d/functions to start and the default PATH that is used there is now different and doesn't include /usr/local/bin, which is where python installs all shell hooks. An easy fix is to let runuser (which is used in the end to start jenkins) set the path to it's default that includes /usr/local/bin.

```diff
+echo "ALWAYS_SET_PATH=yes" > /etc/default/runuser
```

You can alse set ENV\_PATH in the same file if you want jenkins process to have a different PATH

# The template

The only difference to the template that uses this image is that the root volume need to be bumped to 10G and you probably want to now prefer the cheaper and faster gp3 volume type.

```diff
-          Ebs: {VolumeSize: 8, VolumeType: gp2}
+          Ebs: {VolumeSize: 10, VolumeType: gp3}
```

# Volume mounting

Likewise whereever you mount volumes from snahsphots, you probably want to default to gp3 volumes

```diff
-ndt volume-from-snapshot jenkinsdocker jenkinsdocker $MOUNT_PATH 32
+ndt volume-from-snapshot --gp3 jenkinsdocker jenkinsdocker $MOUNT_PATH 32
```
