
#!/usr/bin/env python

import os
from setuptools import setup


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

os.system("pip install -r requirements.txt")

setup(
    name="aws_monitor",
    version="0.0.1",
    author="Micah Hausler",
    author_email="micah.hausler@akimbo.io",
    description=(
        "An Amazon Web services system library that is used at Akimbo LLC"),
    license="Closed",
    keywords="AWS",
    url="http://getfireplug.com",
    packages=['aws_monitor'],
    long_description=read('README.md'),
    dependency_links = [],
    install_requires=[
        "requests==1.2.0",
        "boto==2.9.4",
        "psutil==0.7.1",
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Topic :: System :: Monitoring",
        "License :: OSI Approved :: Closed",
    ],
    entry_points={'console_scripts': ['aws_monitor=monitor.push:main']}
)
