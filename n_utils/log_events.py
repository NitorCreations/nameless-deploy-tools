from __future__ import division
# Copyright 2017 Nitor Creations Oy
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

from past.utils import old_div
from botocore.exceptions import ClientError
from collections import deque
from datetime import datetime
from dateutil import tz
from termcolor import colored
from threading import Event, Thread
import boto3
import locale
import os
import sys
import time
import re
from botocore.config import Config


def millis2iso(millis):
    return fmttime(datetime.utcfromtimestamp(old_div(millis,1000.0)))

def timestamp(tstamp):
    return (tstamp.replace(tzinfo=None) - datetime(1970, 1, 1, tzinfo=None))\
                                                 .total_seconds() * 1000

def fmttime(tstamp):
    return tstamp.replace(tzinfo=tz.tzlocal()).isoformat()[:23]

def uprint(message):
    sys.stdout.write((message + os.linesep)\
                        .encode(locale.getpreferredencoding()))

class LogEventThread(Thread):

    def __init__(self, log_group_name, start_time=None, end_time=None, filter_pattern=None):
        Thread.__init__(self)
        self.log_group_name = log_group_name
        self.start_time = int(start_time) * 1000 if start_time else \
                          int((time.time() - 60) * 1000)
        self.end_time = int(end_time) * 1000 if end_time else None
        self.filter_pattern = filter_pattern
        self._stopped = Event()

    def list_logs(self):
        return

    def stop(self):
        self._stopped.set()

    def run(self):
        self.list_logs()

class CloudWatchLogsGroups():
    def __init__(self, log_filter='', log_group_filter='', start_time=None, end_time=None):
        self.client = boto3.client('logs')
        self.log_filter = log_filter
        self.log_group_filter = log_group_filter
        self.start_time = start_time
        self.end_time = end_time

    def filter_groups(self, log_group_filter, groups):
        filtered = []
        for group in groups:
            if re.search(log_group_filter, group['logGroupName']):
                filtered.append(group['logGroupName'])
        return filtered

    def get_filtered_groups(self, log_group_filter):
        resp = self.client.describe_log_groups()
        filtered_group_names = []
        filtered_group_names.extend(self.filter_groups(self.log_group_filter, resp['logGroups']))
        while resp.get('nextToken'):
            resp = self.client.describe_log_groups(nextToken=resp['nextToken'])
            filtered_group_names.extend(self.filter_groups(self.log_group_filter, resp['logGroups']))
        return filtered_group_names

    def get_logs(self):
        groups = self.get_filtered_groups(self.log_group_filter)
        print("Found log groups: %s" % (groups))
        log_threads = []
        for group_name in groups:
            cwlogs = CloudWatchLogs(
                group_name,
                start_time=self.start_time,
                end_time=self.end_time,
                filter_pattern=self.log_filter
            )
            cwlogs.start()
            log_threads.append(cwlogs)
        while True:
            try:
                time.sleep(1)
            except KeyboardInterrupt:
                print('Closing...')
                for thread in log_threads:
                    thread.stop()
                return

class CloudWatchLogs(LogEventThread):
    def __init__(self, log_group_name, start_time=None, end_time=None, filter_pattern=None):
        LogEventThread.__init__(
            self,
            log_group_name,
            start_time=start_time,
            end_time=end_time,
            filter_pattern=filter_pattern
        )
        config = Config(
            retries = {
                'max_attempts': 10
            }
        )     
        self.client = boto3.client('logs', config=config)

    def list_logs(self):
        do_wait = object()
        interleaving_sanity = deque(maxlen=10000)

        def generator():
            streams = list(self.get_streams())
            while True:
                if len(streams) > 0:
                    kwargs = {'logGroupName': self.log_group_name,
                              'interleaved': True,
                              'logStreamNames': streams,
                              'startTime': self.start_time,
                              'filterPattern': self.filter_pattern if self.filter_pattern else ""}
                    if self.end_time: kwargs['endTime'] = self.end_time
                    response = self.client.filter_log_events(**kwargs)
                    for event in response.get('events', []):
                        if event['eventId'] not in interleaving_sanity:
                            interleaving_sanity.append(event['eventId'])
                            yield event

                    if 'nextToken' in response:
                        kwargs['nextToken'] = response['nextToken']
                    else:
                        streams = list(self.get_streams())
                        if 'nextToken' in kwargs:
                            kwargs.pop('nextToken')
                        yield do_wait
                else:
                    streams = list(self.get_streams())
                    yield do_wait


        for event in generator():
            if event is do_wait and not self._stopped.wait(1.0):
                continue
            elif self._stopped.is_set():
                return

            output = []
            output.append(colored(millis2iso(event['timestamp']), 'yellow'))
            output.append(colored(self.log_group_name, 'green'))
            output.append(colored(event['logStreamName'], 'cyan'))
            output.append(event['message'])
            uprint(' '.join(output))
            sys.stdout.flush()

    def get_streams(self):
        """Returns available CloudWatch logs streams in for stack"""
        kwargs = {'logGroupName': self.log_group_name}
        paginator = self.client.get_paginator('describe_log_streams')
        try:
            for page in paginator.paginate(**kwargs):
                for stream in page.get('logStreams', []):
                    if not 'lastEventTimestamp' in stream or \
                       stream['lastEventTimestamp'] > self.start_time:
                        yield stream['logStreamName']
        except ClientError:
            return

class CloudFormationEvents(LogEventThread):
    def __init__(self, log_group_name, start_time=None):
        LogEventThread.__init__(self, log_group_name, start_time=start_time)
        self.client = boto3.client('cloudformation')

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
                    response = self.client.describe_stack_events(**kwargs)
                except ClientError:
                    pass
                for event in response.get('StackEvents', []):
                    event_timestamp = timestamp(event['Timestamp'])
                    if  event_timestamp < max(self.start_time,
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
