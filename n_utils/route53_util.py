import time
from threadlocal_aws.clients import route53


def upsert_record(dns_name, record_type, value, ttl=300, wait=True):
    zone_id, change = get_record_change(dns_name, record_type, value, hosted_zones(), ttl=ttl)
    request = route53().change_resource_record_sets(HostedZoneId=zone_id,
                                                    ChangeBatch={
                                                        'Changes': [change]
                                                    })['ChangeInfo']
    if wait:
        status = route53().get_change(Id=request['Id'])['ChangeInfo']['Status']
        while not status == 'INSYNC':
            print("Waiting for request to sync - " + str(request['Id']) + "(" + dns_name + ") status: " + status)
            time.sleep(2)
            status = route53().get_change(Id=request['Id'])['ChangeInfo']['Status']


def hosted_zones():
    pages = route53().get_paginator('list_hosted_zones')
    for page in pages.paginate():
        for hosted_zone in page.get('HostedZones', []):
            yield hosted_zone

def longest_matching_zone(alias, hosted_zones):
    ret = {'Name': ''}
    for zone in hosted_zones:
        if (alias + ".").endswith(zone['Name']) and len(zone['Name']) > len(ret['Name']):
            ret = zone
    return ret

def get_record_change(dns_name, record_type, value, hosted_zones, ttl=300):
    zone = longest_matching_zone(dns_name, hosted_zones)
    if zone:
        print(dns_name + " => " + "(" + record_type + ") '" + value + "' in " + zone['Name'])
        change = {
            'Action': 'UPSERT',
            'ResourceRecordSet': {
                'Name': dns_name,
                'Type': record_type,
                'TTL': ttl,
                'ResourceRecords': [{ 'Value': value }]}
        }
        return zone['Id'], change
