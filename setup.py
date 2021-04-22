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

win_deps = []
if sys.version_info[0] == 2:
    python2_or_3_deps = ['pyotp==2.3', 'Pygments==2.5.2', 'importlib-metadata==2.1.1', 'decorator==4.4.2']
    python2_or_3_test_deps = ['pytest==4.6.11', 'pytest-mock==1.13.0', 'mock==3.0.5']
elif sys.version_info[0] == 3:
    python2_or_3_deps = ['pyotp', 'Pygments']
    python2_or_3_test_deps = ['pytest-mock', 'mock']
    if sys.version_info[1] == 5:
        python2_or_3_test_deps.insert(0, "pytest==6.1.2")
        python2_or_3_test_deps.append('importlib-metadata==2.1.1')
    else:
        python2_or_3_test_deps.insert(0, "pytest")
if sys.platform.startswith('win'):
    win_deps = ['win-unicode-console', 'wmi', 'pypiwin32' ]

setup(name='nameless-deploy-tools',
      version='1.191',
      description='Tools for deploying to AWS via CloudFormation and Serverless framework that support a pull request based workflow',
      url='http://github.com/NitorCreations/nameless-deploy-tools',
      download_url='https://github.com/NitorCreations/nameless-deploy-tools/tarball/1.157',
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
          'nitor-vault>=0.41',
          'pyqrcode',
          'six',
          'python-dateutil',
          'pycryptodomex',
          'configparser',
          'scandir',
          'jmespath',
          'ec2-utils==0.25',
          'cloudformation-utils==0.0.2',
          'PyYAML==5.2',
          'pyOpenSSL>=19.1.0'
      ] + python2_or_3_deps + win_deps,
      tests_require=[
          'pytest-cov',
          'coverage'] + python2_or_3_test_deps,
      zip_safe=False)
