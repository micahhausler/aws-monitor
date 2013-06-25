#!/usr/bin/env python

from psutil import disk_partitions, disk_usage


def disk_stats():
    usage = {}
    mountpoints = [disk.mountpoint for disk in disk_partitions()]
    for mp in mountpoints:
        usage[mp] = {}
        usage[mp]['percent'] = disk_usage(mp).percent
        usage[mp]['total'] = disk_usage(mp).total
        usage[mp]['used'] = disk_usage(mp).used
        usage[mp]['free'] = disk_usage(mp).free
    return usage
