name             "haproxy_marathon_bridge"
description      'Installs and configures haproxy_marathon_bridge script'
maintainer       "AWS OpsWorks"
license          "Apache 2.0"
version          "1.0.0"

recipe 'haproxy_marathon_bridge', 'Install and configure a the HAProxy-Marathon Bridge Python Script'

depends 'python'
