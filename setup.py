# Copyright 2016-2017 Nitor Creations Oy
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
import sys
from setuptools import setup
from n_utils import PATH_COMMANDS, CONSOLESCRIPTS

win_deps = ["win-unicode-console", "wmi", "pypiwin32"]

with open("README.md") as f:
    long_description = f.read()

setup(
    name="nameless-deploy-tools",
    version="1.272",
    description="Tools for deploying to AWS via CloudFormation and Serverless framework that support a pull request based workflow",
    url="http://github.com/NitorCreations/nameless-deploy-tools",
    download_url="https://github.com/NitorCreations/nameless-deploy-tools/tarball/1.157",
    author="Pasi Niemi",
    author_email="pasi@nitor.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="Apache 2.0",
    packages=["n_utils"],
    include_package_data=True,
    scripts=PATH_COMMANDS,
    entry_points={
        "console_scripts": CONSOLESCRIPTS,
    },
    install_requires=[
        "pyaml",
        "boto3",
        "requests",
        "termcolor",
        "ipaddr",
        "argcomplete",
        "nitor-vault>=0.41",
        "pyqrcode",
        "six",
        "python-dateutil",
        "pycryptodomex",
        "configparser",
        "scandir",
        "jmespath",
        "ec2-utils>=0.38",
        "cloudformation-utils==0.0.2",
        "pyOpenSSL>=19.1.0",
        "pyotp",
        "Pygments",
        "PyYAML>=5.2",
    ]
    + (win_deps if sys.platform.startswith("win") else []),
    tests_require=[
        "pytest",
        "pytest-cov",
        "coverage",
        "pytest-mock",
        "mock",
        "tomli<2.0.0",
    ],
    zip_safe=False,
)
