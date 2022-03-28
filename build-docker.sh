#!/bin/bash -ex

NEW_VERSION=$(grep nameless-deploy-tools docker/Dockerfile | cut -d "=" -f 3)

docker buildx build --platform linux/amd64 --tag ndt-amd64 docker
docker buildx build --platform linux/arm64 --tag ndt-arm64 docker
set +x
bw get item hub.docker.com | jq -e -r '.fields[]|select(.name == "Access Token").value' | docker login -u "$(bw get username hub.docker.com)" --password-stdin
set -x
docker tag ndt-amd64:latest nitor/ndt:amd64-$NEW_VERSION
docker tag ndt-arm64:latest nitor/ndt:arm64-$NEW_VERSION
docker push nitor/ndt:amd64-$NEW_VERSION
docker push nitor/ndt:arm64-$NEW_VERSION

docker manifest create nitor/ndt:$NEW_VERSION nitor/ndt:amd64-$NEW_VERSION nitor/ndt:arm64-$NEW_VERSION
docker manifest annotate --arch amd64 nitor/ndt:$NEW_VERSION nitor/ndt:amd64-$NEW_VERSION
docker manifest annotate --arch arm64 nitor/ndt:$NEW_VERSION nitor/ndt:arm64-$NEW_VERSION
docker manifest push nitor/ndt:$NEW_VERSION

if ! echo "$NEW_VERSION" | grep "a" > /dev/null; then
  docker manifest rm nitor/ndt:latest || true
  docker manifest create nitor/ndt:latest nitor/ndt:amd64-$NEW_VERSION nitor/ndt:arm64-$NEW_VERSION
  docker manifest annotate --arch amd64 nitor/ndt:latest nitor/ndt:amd64-$NEW_VERSION
  docker manifest annotate --arch arm64 nitor/ndt:latest nitor/ndt:arm64-$NEW_VERSION
  docker manifest push nitor/ndt:latest
fi
