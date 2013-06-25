#!/usr/bin/env python

import boto
import requests
from requests.exceptions import ConnectionError


def get_ec2_instance_id():
    try:
        response = requests.get(
            "http://169.254.169.254/latest/meta-data/instance-id/")
        return response.text
    except ConnectionError, e:
        print e
        import os
        return os.uname()[1]


def setup_cw_connection(key_id=None, secret_key=None, region="us-east-1"):
    """
    Returns an ec2 connection

    Either pass in a key_id and secret_key, or it picks up the OS variables
    AWS_ACCESS_KEY_ID
    AWS_SECRET_ACCESS_KEY
    """
    cw = boto.connect_cloudwatch()
    return cw
