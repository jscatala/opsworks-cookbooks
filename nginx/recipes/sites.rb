node[:sites].each do |site|
  template "#{node[:nginx][:dir]}/sites-available/#{site[:domains].first()}" do
    source "custom_site.erb"
    owner "root"
    group "root"
    mode 0644
    variables({
      :site => site
    })
  end

  execute "nxensite #{site[:domains].first()}" do
    command "/usr/sbin/nxensite #{site[:domains].first()}"
    notifies :reload, "service[nginx]"
    not_if do File.symlink?("#{node[:nginx][:dir]}/sites-enabled/#{site[:domains].first()}") end
  end
end

include_recipe "nginx::service"

service "nginx" do
  action [ :enable, :start ]
end