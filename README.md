aws-monitor
===========

Custom AWS Cloudwatch Monitoring for disk and memory usage


Setup
=====

To setup, run the following:

```
$ git clone git://github.com/micahhausler/aws-monitor.git
$ cd aws-monitor 
$ sudo python setup.py install
```

Usage
------
aws-monitor sends custom metrics such as disk and memory statistics to Cloudwatch

[envdir](http://cr.yp.to/daemontools/envdir.html) is part of the [daemontools](http://cr.yp.to/daemontools) package, and is great for setting private environment variables.

To set up an envdir directory:

```
# Assumption: the group is trusted to read secret information
$ umask u=rwx,g=rx,o=
$ mkdir -p /etc/aws-monitor/env
$ echo "secret-key-content" > /etc/aws-monitor/env/AWS_SECRET_ACCESS_KEY
$ echo "access-key" > /etc/aws-monitor/env/AWS_ACCESS_KEY_ID
$ echo 'DEBUG|INFO|ERROR|OFF' > /etc/aws-monitor/env/LOGLEVEL
$ chown -R root:TRUSTEDGROUP /etc/aws-monitor
```

The log level and aws_acces_key_id may also be passed via command line. If both command line and environment variable are provided, the command line parameter is used. The default log level is INFO:

```
envdir /etc/aws-monitor/env aws-monitor -k AWS_ACCESS_KEY_ID -l LOG_LEVEL
or
envdir /etc/aws-monitor/env aws-monitor --aws-access-key-id=AWS_ACCESS_KEY_ID  --log-level=LOG_LEVEL
```


It is intended to use the script in a cron job every minute:

```
# Cron file
# every minute
* * * * * envdir /etc/aws-monitor/env aws-monitor
```

Log
---

A logfile is automatically created at /var/log/aws-monitor.log
