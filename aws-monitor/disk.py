#!/usr/bin/env python

from psutil import disk_partitions, disk_usage


def disk_stats():
    usage = {}
    mountpoints = [disk.mountpoint for disk in disk_partitions()]
    for mp in mountpoints:
        usage[mp] = {}
        usage[mp]['disk_percent'] = disk_usage(mp).percent
        usage[mp]['disk_total'] = disk_usage(mp).total
        usage[mp]['disk_used'] = disk_usage(mp).used
        usage[mp]['disk_free'] = disk_usage(mp).free

    ret = {}
    for k, v in usage.iteritems():
        ret["disk " + k] = v
    return ret
