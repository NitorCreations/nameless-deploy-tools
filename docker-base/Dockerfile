# Copyright 2017-2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Amazon Software License (the "License"). You may not use this file except in compliance with the License.
# A copy of the License is located at
#
#    http://aws.amazon.com/asl/
#
# or in the "license" file accompanying this file.
# This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, express or implied.
# See the License for the specific language governing permissions and limitations under the License.
#

FROM ubuntu:20.04

ENV DOCKER_BUCKET="download.docker.com" \
    DOCKER_VERSION="20.10.14" \
    DOCKER_CHANNEL="stable" \
    DOCKER_SHA256_AMD64="7ca4aeeed86619909ae584ce3405da3766d495f98904ffbd9d859add26b83af5" \
    DOCKER_SHA256_ARM64="ea971edc1179088bfd25edd04a0c12848143d15cb8202ebb93a6a08973464fd0" \
    DIND_COMMIT="52379fa76dee07ca038624d639d9e14f4fb719ff" \
    DOCKER_COMPOSE_VERSION="2.2.2"

RUN set -x && export DEBIAN_FRONTEND=noninteractive && apt update && apt upgrade -qy \
    && apt install -qy --no-install-recommends \
    apt-transport-https gnupg-agent software-properties-common wget \
    python3 python3-dev python3-pip python-is-python3 fakeroot ca-certificates \
    tar gzip zip autoconf automake \
    openjdk-17-jdk git openssh-client unzip chromium-bsu jq gpg parallel dirmngr \
    bzip2 file g++ gcc imagemagick \
    libbz2-dev libc6-dev libcurl4-openssl-dev libdb-dev \
    libevent-dev libffi-dev libgeoip-dev libglib2.0-dev \
    libjpeg-dev libkrb5-dev liblzma-dev \
    libmagickcore-dev libmagickwand-dev libmysqlclient-dev \
    libncurses5-dev libpng-dev libpq-dev libreadline-dev \
    libsqlite3-dev libssl-dev libtool libwebp-dev \
    libxml2-dev libxslt1-dev libyaml-dev make \
    patch xz-utils zlib1g-dev unzip curl \
    e2fsprogs iptables xfsprogs xz-utils \
    less groff liberror-perl \
    && apt clean && apt autoclean \
    && ARCH="$(uname -m)" \
    && curl -fSL "https://${DOCKER_BUCKET}/linux/static/${DOCKER_CHANNEL}/$ARCH/docker-${DOCKER_VERSION}.tgz" -o docker-$ARCH.tgz \
    && (echo "${DOCKER_SHA256_AMD64} *docker-x86_64.tgz" | sha256sum -c - || echo "${DOCKER_SHA256_ARM64} *docker-aarch64.tgz" | sha256sum -c -) \
    && tar --extract --file docker-$ARCH.tgz --strip-components 1  --directory /usr/local/bin/ \
    && rm docker-$ARCH.tgz \
    && docker -v \
    && addgroup dockremap \
    && useradd -g dockremap dockremap \
    && echo 'dockremap:165536:65536' >> /etc/subuid \
    && echo 'dockremap:165536:65536' >> /etc/subgid \
    && wget "https://raw.githubusercontent.com/docker/docker/${DIND_COMMIT}/hack/dind" -O /usr/local/bin/dind \
    && curl -L https://github.com/docker/compose/releases/download/v${DOCKER_COMPOSE_VERSION}/docker-compose-Linux-$ARCH > /usr/local/bin/docker-compose \
    && curl -L https://github.com/docker/compose/releases/download/v${DOCKER_COMPOSE_VERSION}/docker-compose-linux-$ARCH.sha256 | sed "s/docker-compose-linux-$ARCH/\/usr\/local\/bin\/docker-compose/" | sha256sum -c -\
    && chmod +x /usr/local/bin/dind /usr/local/bin/docker-compose \
    # Ensure docker-compose works
    && docker-compose version

# Install dependencies by all python images equivalent to buildpack-deps:jessie
# on the public repos.

RUN python -m pip install -U pip
VOLUME /var/lib/docker

COPY dockerd-entrypoint.sh /usr/bin/dockerd-entrypoint.sh
COPY start-docker.sh /usr/bin/start-docker.sh

ENTRYPOINT ["dockerd-entrypoint.sh"]
