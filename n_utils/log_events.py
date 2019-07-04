# Copyright 2017-2018 Nitor Creations Oy
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
#
# Code used under license:
#
# parse_datetime from https://github.com/jorgebastida/awslogs:
#
# Copyright (c) 2015 Benito Jorge Bastida
# All rights reserved.
#
# Revised BSD License
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#  1. Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer.
#
#  2. Redistributions in binary form must reproduce the above
#     copyright notice, this list of conditions and the following
#     disclaimer in the documentation and/or other materials provided
#     with the distribution.
#
#  3. Neither the name of the author nor the names of other
#     contributors may be used to endorse or promote products derived
#     from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


from builtins import object
from botocore.exceptions import ClientError
from collections import deque
from termcolor import colored
import sys
from ec2_utils.logs import fmttime, millis2iso, timestamp, \
    uprint, validatestarttime, parse_datetime, LogWorkerThread
from threadlocal_aws.clients import cloudformation

class CloudFormationEvents(LogWorkerThread):
    def __init__(self, log_group_name, start_time=None):
        LogWorkerThread.__init__(self)
        self.log_group_name = log_group_name
        self.start_time = validatestarttime(start_time)

    def list_logs(self):
        do_wait = object()
        dedup_queue = deque(maxlen=10000)
        kwargs = {'StackName': self.log_group_name}

        def generator():
            start_seen = False
            seen_events_up_to = 0
            event_timestamp = float("inf")

            while True:
                unseen_events = deque()
                response = {}
                try:
                    response = cloudformation().describe_stack_events(**kwargs)
                except ClientError:
                    pass
                for event in response.get('StackEvents', []):
                    event_timestamp = timestamp(event['Timestamp'])
                    if event_timestamp < max(self.start_time,
                                             seen_events_up_to):
                        break
                    if not event['EventId'] in dedup_queue:
                        dedup_queue.append(event['EventId'])
                        unseen_events.append(event)

                if len(unseen_events) > 0:
                    seen_events_up_to = \
                        int(timestamp(unseen_events[0]['Timestamp']))
                    for event in reversed(unseen_events):
                        yield event

                # If we've seen the start, we don't want to iterate with
                # NextToken anymore
                if event_timestamp < self.start_time or \
                   'NextToken' not in response:
                    start_seen = True
                # If we've not seen the start we iterate further
                if not start_seen and 'NextToken' in response:
                    kwargs['NextToken'] = response['NextToken']
                # Otherwise make sure we don't send NextToken
                elif 'NextToken' in kwargs:
                    kwargs.pop('NextToken')
                yield do_wait

        for event in generator():
            if event is do_wait and not self._stopped.wait(1.0):
                continue
            elif self._stopped.is_set():
                return

            output = []
            output.append(colored(fmttime(event['Timestamp']),
                                  'yellow'))
            target = event['ResourceType'] + ":" + event['LogicalResourceId']
            output.append(colored(target, 'cyan'))
            message = event['ResourceStatus']
            color = 'green'
            if "_FAILED" in message:
                color = 'red'
            output.append(colored(message, color))
            if 'ResourceStatusReason' in event:
                output.append(event['ResourceStatusReason'])
            uprint(' '.join(output))
            sys.stdout.flush()
