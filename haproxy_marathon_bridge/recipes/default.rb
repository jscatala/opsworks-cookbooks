#
# Cookbook Name:: haproxy_marathon_bridge
# Recipe:: default
#

apt_resource 'python-pip' do
end

bash 'requests' do
    code <<-EOH
    pip install --upgrade pip
    pip install requests
    EOH
end

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
