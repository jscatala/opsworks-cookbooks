#
# Cookbook Name:: haproxy_marathon_bridge
# Recipe:: default
#

include_recipe "python"
include_recipe "python::pip"

python_pip "requests"

template '/opt/haproxy_marathon_bridge' do
  source 'haproxy_marathon_bridge.py'
  owner 'root'
  group 'root'
  mode 0744
end

template '/etc/cron.d/haproxy_marathon_bridge' do
  source 'crontab.erb'
  owner 'root'
  group 'root'
  mode 0755
end
