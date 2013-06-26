#!/usr/bin/env python

from psutil import phymem_usage, virtmem_usage


def get_physmem():
    usage = {}
    fields = list(phymem_usage()._fields)
    mem = phymem_usage()
    for field in fields:
        usage["physical_memory_" + field] = mem.__getattribute__(field)
    return usage


def get_virtmem():
    usage = {}
    fields = list(virtmem_usage()._fields)
    mem = virtmem_usage()
    for field in fields:
        usage["virtual_memory_" + field] = mem.__getattribute__(field)
    return usage
