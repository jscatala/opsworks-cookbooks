name             "rsyslog"
description      'Installs and configures rsyslog logging to loggly'
maintainer       "AWS OpsWorks"
license          "Apache 2.0"
version          "1.0.0"

recipe 'rsyslog', 'Install and configures rsyslog to watch nginx logs and send them to loggly'
