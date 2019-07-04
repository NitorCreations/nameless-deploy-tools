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

setup(name='nameless_deploy_tools',
      version='1.91',
      description='Tools for deploying to AWS via CloudFormation and Serverless framework that support a pull request based workflow',
      url='http://github.com/NitorCreations/nameless-deploy-tools',
      download_url='https://github.com/NitorCreations/nameless-deploy-tools/tarball/1.91',
      author='Pasi Niemi',
      author_email='pasi@nitor.com',
      license='Apache 2.0',
      packages=['n_utils'],
      include_package_data=True,
      scripts=PATH_COMMANDS,
      entry_points={
          'console_scripts': CONSOLESCRIPTS,
      },
      setup_requires=[
          'pytest-runner'
      ],
      install_requires=[
          'future',
          'pyaml',
          'awscli',
          'requests',
          'termcolor',
          'ipaddr',
          'argcomplete',
          'nitor-vault',
          'Pygments',
          'pyotp',
          'pyqrcode',
          'six',
          'python-dateutil',
          'pycryptodomex',
          'configparser',
          'scandir',
          'jmespath',
          'ec2-utils==0.13'
      ] + ([
          'win-unicode-console',
          'wmi',
          'pypiwin32'
          ] if sys.platform.startswith('win') else []),
      tests_require=[
          'pytest',
          'pytest-mock',
          'pytest-cov',
          'coverage'
      ],
      zip_safe=False)
