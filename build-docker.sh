#!/bin/bash -x

NEW_VERSION=$1

docker build -t ndt docker
set +x
bw get item hub.docker.com | jq -r '.fields[]|select(.name == "Access Token").value' | docker login -u "$(bw get username hub.docker.com)" --password-stdin
set -x
docker tag ndt:latest nitor/ndt:$NEW_VERSION
docker push nitor/ndt:$NEW_VERSION
if ! echo "$NEW_VERSION" | grep "a" > /dev/null; then
  docker tag ndt:latest nitor/ndt:latest
  docker push nitor/ndt:latest
fi

