#!/bin/bash -x

# Copyright 2016-2023 Nitor Creations Oy
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

# Check platform
case "$(uname -s)" in
    "Darwin")
        PLATFORM="mac"
        ;;
    "MINGW"*)
        PLATFORM="windows"
        ;;
    *)
        PLATFORM="linux"
        ;;
esac

# BSD sed on MacOS works differently
if [ "$PLATFORM" = mac ]; then
    SED_COMMAND=(sed -i '')
else
    SED_COMMAND=(sed -i)
fi

VERSION=$(grep -E '^VERSION' n_utils/__init__.py | cut -d\" -f 2)
MAJOR=${VERSION//.*/}
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
    MESSAGE="$1"
fi

if [ -z "$MESSAGE" ]; then
  MESSAGE="$NEW_VERSION"
fi

./update-commandlist.sh
"${SED_COMMAND[@]}" "s/$VERSION/$NEW_VERSION/g" setup.cfg
"${SED_COMMAND[@]}" "s/$VERSION/$NEW_VERSION/g" pyproject.toml
"${SED_COMMAND[@]}" "s/## Released version.*/## Released version $NEW_VERSION/g" README.md
"${SED_COMMAND[@]}" "s/nameless-deploy-tools==.*/nameless-deploy-tools==$NEW_VERSION/g" docker/Dockerfile
"${SED_COMMAND[@]}" "s/^VERSION.*=.*/VERSION\ =\ \"$NEW_VERSION\"/" n_utils/__init__.py

git commit -m "$1" setup.cfg pyproject.toml README.md docker/Dockerfile docs/commands.md n_utils/__init__.py
git tag "$NEW_VERSION" -m "$MESSAGE"
git push origin "$NEW_VERSION"

if [ -n "$(command -v python3)" ]; then
    PYTHON=$(which python3)
else
    PYTHON=$(which python)
fi

if [ ! -e "$PYTHON" ]; then
    echo "Python executable not found: $PYTHON"
    exit 1
else
    echo "Using $PYTHON $($PYTHON --version)"
fi

rm -rf dist/*
$PYTHON setup.py sdist bdist_wheel
twine upload dist/*
sleep 30

./build-docker.sh "$NEW_VERSION"
