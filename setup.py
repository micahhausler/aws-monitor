
#!/usr/bin/env python

import os
from setuptools import setup

try:
    from setuptools import setup, find_packages

    # Silence pyflakes
    assert setup
    assert find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

os.system("pip install -r requirements.txt")

VERSION = read(os.path.join('aws_monitor', 'VERSION')).strip()

install_requires = [
        l for l in read('requirements.txt').split('\n')
        if l and not l.startswith('#')]

setup(
    name="aws-monitor",
    version=VERSION,
    packages=find_packages(),
    author="Micah Hausler",
    author_email="micah.hausler@akimbo.io",
    description=(
        "An Amazon Web services system library that is used at Akimbo LLC"),
    license="BSD",
    keywords="AWS CloudWatch monitoring",
    url="http://getfireplug.com",
    long_description=read('README.md'),
    dependency_links = [],
    install_requires=install_requires,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Topic :: System :: Monitoring",
        "License :: OSI Approved :: Closed",
    ],
    package_data={'aws_monitor': ['VERSION']},
    entry_points={'console_scripts': ['aws-monitor=aws_monitor.push:main']}
)
