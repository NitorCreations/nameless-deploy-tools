#!/bin/bash -x

# Copyright 2016 Nitor Creations Oy
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

VERSION=$(egrep '\sversion' setup.py | cut -d\' -f 2)
MAJOR=${VERSION//.*}
MINOR=${VERSION##*.}
if [ "$1" = "-m" ]; then
  MAJOR=$(($MAJOR + 1))
  MINOR="0"
  NEW_VERSION=$MAJOR.$MINOR
  shift
elif [ "$1" = "-v" ]; then
  shift
  NEW_VERSION="$1"
  shift
else
  MINOR=$(($MINOR + 1))
  NEW_VERSION=$MAJOR.$MINOR
fi

./update-commandlist.sh
sed -i "s/$VERSION/$NEW_VERSION/g" setup.py
sed -i "s/## Released version.*/## Released version $NEW_VERSION/g" README.md
sed -i "s/nameless-deploy-tools==.*/nameless-deploy-tools==$NEW_VERSION/g" docker/Dockerfile
sed -i "s/^VERSION=.*/VERSION=\"$NEW_VERSION\"/" n_utils/__init__.py
git commit -m "$1" setup.py README.md docker/Dockerfile docs/commands.md n_utils/__init__.py
git tag "$NEW_VERSION" -m "$1"
git push --tags origin master

python setup.py sdist bdist_wheel
gpg -o dist/adfs_aws_login-${NEW_VERSION}-py2.py3-none-any.whl.asc -a -b dist/adfs_aws_login-${NEW_VERSION}-py2.py3-none-any.whl
gpg -o dist/adfs-aws-login-${NEW_VERSION}.tar.gz.asc -a -b dist/adfs-aws-login-${NEW_VERSION}.tar.gz
twine upload dist/*
sleep 30

./build-docker.sh $NEW_VERSION
