#
# Cookbook Name:: rsyslog
# Recipe:: default
#

template '/etc/rsyslog.d/21-nginx-loggly.conf' do
  source 'nginx-loggly.conf.erb'
  owner 'root'
  group 'root'
  mode 0744
end

template '/etc/rsyslog.d/22-loggly.conf' do
  source 'loggly.conf.erb'
  owner 'root'
  group 'root'
  mode 0744
end

template '/etc/rsyslog.conf' do
  source 'rsyslog.conf.erb'
  owner 'root'
  group 'root'
  mode 0644
end

service "rsyslog" do
  action [ :stop, :start ]
end