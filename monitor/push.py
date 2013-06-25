#!/usr/bin/env python

import json
import sys

from utils import setup_cw_connection, get_ec2_instance_id
from disk import disk_stats
from memory import get_physmem, get_virtmem


def data_packet():
    dstats = disk_stats()
    phys_mem = get_physmem()
    virt_mem = get_virtmem()

    data = {}
    data['InstanceID'] = get_ec2_instance_id()
    data['physical_mem'] = phys_mem
    data['virtual_mem'] = virt_mem
    data['disk'] = dstats

    print json.dumps(data, indent=4)

    return data


def main(argv=None):
    pass


if __name__ == '__main__':
    sys.exit(main())
