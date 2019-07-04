from datetime import datetime

from n_utils.cloudfront_utils import distributions, distribution_comments

DISTRIBUTION = {
    'DistributionList': {
        'Marker': 'string',
        'NextMarker': 'string',
        'MaxItems': 123,
        'IsTruncated': False,
        'Quantity': 123,
        'Items': [
            {
                'Id': 'id1',
                'ARN': 'arn1',
                'Status': 'status1',
                'LastModifiedTime': datetime(2015, 1, 1),
                'DomainName': 'string',
                'Comment': 'comment1',
            },
            {
                'Id': 'id2',
                'ARN': 'arn2',
                'Status': 'status2',
                'LastModifiedTime': datetime(2016, 1, 1),
                'DomainName': 'string',
                'Comment': 'comment2',
            }
        ]
    }
}


def test_distributions(mocker, cloudfront_paginator):
    cloudfront_paginator.paginate.return_value = [DISTRIBUTION]
    assert list(distributions()) == ['id1', 'id2']


def test_distribution_comments(mocker, cloudfront_paginator):
    cloudfront_paginator.paginate.return_value = [DISTRIBUTION]
    assert list(distribution_comments()) == ['comment1', 'comment2']
