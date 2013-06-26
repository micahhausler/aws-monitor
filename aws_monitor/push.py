#!/usr/bin/env python

import json
import os
import sys

import argparse
import logging

from utils import get_ec2_instance_id
from disk import disk_stats
from memory import get_physmem, get_virtmem

import boto


logging.basicConfig(
    filename="/var/log/aws-monitor.log",
    format='%(asctime)-8s %(name)-12s %(levelname)-8s %(message)s')
logger = logging.getLogger('aws-monitor')


def send_disk_stats(connection, data, instance_id):
    namespace = "CustomMetric"

    for disk, stats in data.iteritems():

        logger.debug(msg="{}: {}".format(disk, json.dumps(data[disk])))

        if 'disk_percent' in stats.keys():
            connection.put_metric_data(
                namespace=namespace,
                unit='Percent',
                name="percent_disk_used",
                value=int(stats['disk_percent']),
                dimensions={
                    "disk": disk,
                    "InstanceID": instance_id})
            stats.pop('disk_percent')

        stat_keys = stats.keys()
        stat_values = [int(stats[m]) for m in stat_keys]

        connection.put_metric_data(
            namespace=namespace,
            unit='Bytes',
            name=stat_keys,
            value=stat_values,
            dimensions={
                "disk": disk,
                "InstanceID": instance_id})
    logger.debug(msg="Sent disk stats successfully")
    return True


def send_mem_stats(connection, data, instance_id):
    namespace = "CustomMetric"

    logger.debug(msg=json.dumps(data))

    for k, v in data.iteritems():
        if "physical_memory_percent" in v.keys():
            connection.put_metric_data(
                namespace=namespace,
                unit='Percent',
                name="physical_memory_percent",
                value=int(v['physical_memory_percent']),
                dimensions={"InstanceID": instance_id})
            v.pop('physical_memory_percent')
        if "virtual_memory_percent" in v.keys():
            connection.put_metric_data(
                namespace=namespace,
                unit='Percent',
                name="virtual_memory_percent",
                value=int(v['virtual_memory_percent']),
                dimensions={"InstanceID": instance_id})
            v.pop('virtual_memory_percent')
        stat_keys = v.keys()
        stat_values = [int(v[m]) for m in stat_keys]
        connection.put_metric_data(
            namespace=namespace,
            unit='Bytes',
            name=stat_keys,
            value=stat_values,
            dimensions={"InstanceID": instance_id})
    logger.debug(msg="Sent mem stats successfully")
    return True


def main(argv=None):
    if argv is None:
        argv = sys.argv

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=__doc__)

    parser.add_argument(
        '-k', '--aws-access-key-id',
        help='public AWS access key. Can also be defined in '
        'an environment variable. If both are defined, '
        'the one defined in the programs arguments takes '
        'precedence.')

    parser.add_argument(
        '-l', '--loglevel',
        help='The level of log verbosity. Can also be set as the '
        'environment variable LOGLEVEL. Available levels are '
        'DEBUG | INFO | ERROR | OFF. The default is ERROR')

    args = parser.parse_args()

    levels = ['DEBUG', 'INFO', 'ERROR', 'OFF']
    if args.loglevel is None:
        level = os.getenv("LOGLEVEL")
        if level is None:
            logger.debug(msg="LOGLEVEL is not set, defaulting to INFO")
            level = "INFO"
    else:
        level = args.loglevel

    if level in levels:
        logging.root.setLevel(level)
    else:
        logger.error(
            msg="Log level '{}' is not a valid level".format(level),
            hint="Please ensure LOGLEVEL is one of {}".format(", ".join(levels)))
        sys.exit(1)

    secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')

    if secret_key is None:
        logger.error(
            msg='no AWS_SECRET_ACCESS_KEY defined',
            hint='Define the environment variable AWS_SECRET_ACCESS_KEY.')
        sys.exit(1)

    if args.aws_access_key_id is None:
        aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
        if aws_access_key_id is None:
            logger.error(
                msg='no storage prefix defined',
                hint=('Either set the --aws-access-key-id option or define '
                    'the environment variable AWS_ACCESS_KEY_ID.'))
            sys.exit(1)
    else:
        aws_access_key_id = args.aws_access_key_id

    conn = boto.connect_cloudwatch(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=secret_key)

    instance_id = get_ec2_instance_id(logger)
    logger.info(msg="Instanceid = {}".format(instance_id))

    phys_mem = {'physical_mem': get_physmem()}
    logger.info(msg=json.dumps(phys_mem))

    virt_mem = {'virtual_mem': get_virtmem()}
    logger.info(msg=json.dumps(virt_mem))

    dstats = disk_stats()
    logger.info(msg=json.dumps(dstats))

    send_disk_stats(conn, dstats, instance_id)
    send_mem_stats(conn, phys_mem, instance_id)
    send_mem_stats(conn, virt_mem, instance_id)

    logger.debug(msg="exited successfully")
    return 0


if __name__ == '__main__':
    sys.exit(main())
