template "logrotate" do
  path "/etc/logrotate.d/nginx"
  source "logrotate.erb"
  owner "root"
  group "root"
  mode 0644
end
