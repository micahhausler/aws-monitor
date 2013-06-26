#!/usr/bin/env python

import requests
from requests.exceptions import ConnectionError, Timeout


def get_ec2_instance_id(logger):
    try:
        response = requests.get(
            "http://169.254.169.254/latest/meta-data/instance-id/", timeout=10)
        return response.text
    except (ConnectionError, Timeout), e:
        logger.error(msg=e.message)
        logger.error(msg="Could not get ec2 InstanceID, using hostname")
        import os
        return os.uname()[1]


def bytes_to_best_unit(byte):
    units = ['Bytes', 'Kilobytes', 'Megabytes', 'Gigabytes', 'Terabytes']
    metric = byte
    counter = 0
    while metric > 1024 and counter < 4:
        metric = metric / 1024
        counter += 1
    return (metric, units[counter])


def bytes_to_unit(byte, unit):
    units = ['Bytes', 'Kilobytes', 'Megabytes', 'Gigabytes', 'Terabytes']
    if unit not in units:
        return False
