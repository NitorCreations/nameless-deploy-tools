#!/bin/bash -e

cp n_utils/includes/install_tools.sh docker-base/
set +x
bw get item hub.docker.com | jq -e -r '.fields[]|select(.name == "Access Token").value' | docker login -u "$(bw get username hub.docker.com)" --password-stdin
set -x
docker buildx build --platform linux/amd64 -t docker-base-amd64 docker-base
docker buildx build --platform linux/arm64 -t docker-base-arm64 docker-base
docker tag docker-base-arm64:latest nitor/docker-base:latest-arm64
docker tag docker-base-amd64:latest nitor/docker-base:latest-amd64
docker push nitor/docker-base:latest-arm64
docker push nitor/docker-base:latest-amd64
docker manifest rm nitor/docker-base:latest || true
docker manifest create nitor/docker-base:latest nitor/docker-base:latest-arm64 nitor/docker-base:latest-amd64
docker manifest annotate --arch amd64 nitor/docker-base:latest nitor/docker-base:latest-arm64
docker manifest annotate --arch arm64 nitor/docker-base:latest nitor/docker-base:latest-amd64
docker manifest push nitor/docker-base:latest
