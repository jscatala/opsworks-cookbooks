#
# Cookbook:: metrics
# Recipe:: default
#
# Copyright:: 2017, The Authors, All Rights Reserved.


directory '/opt/cloudmonitor' do
    owner 'root'
    group 'root'
    mode '0644'
    action :create
end


apt_package 'python-pip' do
end

bash 'virtualenv and cloudwatchmon' do
    code <<-EOH
    pip install --upgrade pip
    pip install virtualenv
    virtualenv /opt/cloudmonitor/env
    /opt/cloudmonitor/env/bin/pip install cloudwatchmon
    EOH
end


git 'cloudmonitor' do 
    repository 'https://github.com/osiegmar/cloudwatch-mon-scripts-python.git'
    destination '/opt/cloudmonitor/cloudwatch-mon-scripts-python'
end


cron 'cloudwatchmetrics' do
    minute '*/5'
    command "/opt/cloudmonitor/env/bin/python /opt/cloudmonitor/cloudwatch-mon-scripts-python/cloudwatchmon/cli/put_instance_stats.py --mem-util --disk-space-util --disk-path=/"
end
