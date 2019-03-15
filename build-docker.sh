#!/bin/bash -x

NEW_VERSION=$1

docker build -t ndt docker
set +x
docker login -u "$(git config docker.username)" -p "$(lpass show --password docker.com)"
set -x
docker tag ndt:latest nitor/ndt:$NEW_VERSION
docker push nitor/ndt:$NEW_VERSION
if ! echo "$NEW_VERSION" | grep "a" > /dev/null; then
  docker tag ndt:latest nitor/ndt:latest
  docker push nitor/ndt:latest
fi

