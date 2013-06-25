aws\_monitor
===========

Custom AWS Cloudwatch Monitoring for disk and memory usage


Setup
=====

To setup, run the following:

```
$ git clone git://github.com/micahhausler/aws_monitor.git
$ cd aws_monitor 
$ sudo python setup.py install
```

Usage
------
aws_monitor sends custom metrics such as disk and memory statistics to Cloudwatch


[envdir](http://cr.yp.to/daemontools/envdir.html) is part of the [daemontools](http://cr.yp.to/daemontools) package, and is great for setting private environment variables.

To set up an envdir directory:

```
# Assumption: the group is trusted to read secret information
$ umask u=rwx,g=rx,o=
$ mkdir -p /etc/aws_monitor/env
$ echo "secret-key-content" > /etc/aws_monitor/env/AWS_SECRET_ACCESS_KEY
$ echo "access-key" > /etc/aws_monitor/env/AWS_ACCESS_KEY_ID
$ echo 'DEBUG|INFO|ERROR|OFF' > /etc/aws_monitor/env/LOGLEVEL
$ chown -R root:TRUSTEDGROUP /etc/aws_monitor
```

It is intended to use the script in a cron job, maybe every 1 or 5 minuets:

```
# Cron file
# every 5 minuets
*/5 * * * * envdir /etc/aws_monitor/env aws_monitor
# every minuet
* * * * * envdir /etc/aws_monitor/env aws_monitor
```
