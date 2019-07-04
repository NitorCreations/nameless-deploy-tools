#!/usr/bin/env python

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
# limitations under the License
from builtins import str
import time
from threadlocal_aws.clients import cloudfront, route53

def distributions():
    pages = cloudfront().get_paginator('list_distributions')
    print(pages.paginate())
    for page in pages.paginate():
        print(page)
        distribution_list = page.get('DistributionList')
        for distribution in distribution_list['Items']:
            yield distribution['Id']


def distribution_comments():
    pages = cloudfront().get_paginator('list_distributions')
    for page in pages.paginate():
        distribution_list = page.get('DistributionList')
        for distribution in distribution_list['Items']:
            yield distribution['Comment']


def get_distribution_by_id(distribution_id):
    ret = cloudfront().get_distribution(Id=distribution_id)['Distribution']
    ret['DistributionConfig']['Id'] = distribution_id
    ret['DistributionConfig']['DomainName'] = ret['DomainName']
    return [ret['DistributionConfig']]


def get_distribution_by_comment(comment):
    pages = cloudfront().get_paginator('list_distributions')
    ret = []
    for page in pages.paginate():
        distribution_list = page.get('DistributionList')
        for distribution in distribution_list['Items']:
            if comment == distribution['Comment']:
                ret.append(distribution)
    if not ret:
        raise Exception("Failed to find distribution with comment " + comment)
    else:
        return ret


def hosted_zones():
    pages = route53().get_paginator('list_hosted_zones')
    for page in pages.paginate():
        for hosted_zone in page.get('HostedZones', []):
            yield hosted_zone


def upsert_cloudfront_records(args):
    distributions = None
    if args.distribution_id:
        distributions = get_distribution_by_id(args.distribution_id)
    else:
        distributions = get_distribution_by_comment(args.distribution_comment)
    zones = list(hosted_zones())
    changes = {}
    for distribution in distributions:
        if 'Aliases' in distribution:
            print("Upserting records for " + distribution['Id'] + " (" + distribution['Comment'] + ")")
            for alias in distribution['Aliases']['Items']:
                change = get_record_change(alias, distribution['DomainName'], distribution['Id'], zones)
                if not change['HostedZoneId'] in changes:
                    changes[change['HostedZoneId']] = []
                changes[change['HostedZoneId']].append(change['Change'])
    requests = []
    for req in changes:
        requests.append(route53().change_resource_record_sets(HostedZoneId=req,
                                                              ChangeBatch={
                                                                 'Changes': changes[req]
                                                              })['ChangeInfo'])
    if args.wait:
        not_synced_count = 1
        while not_synced_count > 0:
            not_synced_count = 0
            for req in requests:
                if not route53().get_change(Id=req['Id'])['ChangeInfo']['Status'] == 'INSYNC':
                    not_synced_count = not_synced_count + 1
            if not_synced_count > 0:
                print("Waiting for requests to sync - " + str(not_synced_count) + " not synced")
                time.sleep(2)
            else:
                print(str(len(requests)) + " requests INSYNC")


def longest_matching_zone(alias, hosted_zones):
    ret = {'Name': ''}
    for zone in hosted_zones:
        if (alias + ".").endswith(zone['Name']) and len(zone['Name']) > len(ret['Name']):
            ret = zone
    return ret


def get_record_change(alias, dns_name, distribution_id, hosted_zones):
    zone = longest_matching_zone(alias, hosted_zones)
    if zone:
        print(alias + " => " + dns_name + "(" + distribution_id + ") in " + zone['Name'])
        if alias + "." == zone['Name']:
            type = "A"
        else:
            type = "CNAME"
        change = {
            'Action': 'UPSERT',
            'ResourceRecordSet': {
                'Name': alias,
                'Type': type}
        }
        if type == "A":
            change['ResourceRecordSet']['AliasTarget'] = {
                'HostedZoneId': 'Z2FDTNDATAQYW2',
                'DNSName': dns_name,
                'EvaluateTargetHealth': False
            }
        else:
            change['ResourceRecordSet']['ResourceRecords'] = [{
                'Value': dns_name
            }]
            change['ResourceRecordSet']['TTL'] = 300

        return {'HostedZoneId': zone['Id'], 'Change': change}
