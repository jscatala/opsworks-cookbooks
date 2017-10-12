#!/usr/bin/env python
import os
import random
import logging
import argparse
import subprocess

haproxy_conf_file = "/etc/haproxy/haproxy.cfg"
source_script_path = os.path.realpath(__file__)


def cat(content):
    return """cat <<\EOF\n{}\n\EOF""".format(content)


def file_contents(filename=None, content=None):
    '''
    Just return the contents of a file as a string or write if content
    is specified. Returns the contents of the filename either way.
    '''
    logging.debug('file_contents()')
    if content:
        f = open(filename, 'w+')
        f.write(content)
        f.close()
    try:
        f = open(filename, 'r')
        text = f.read()
        f.close()
    except:
        text = None

    return text


def reload_haproxy():
    subprocess.call("service haproxy reload", shell=True)


def header_config():
    config = []
    config.append("global")
    config.append("  daemon")
    config.append("  log 127.0.0.1 local0")
    config.append("  log 127.0.0.1 local1 notice")
    config.append("  maxconn 4096")
    config.append("")
    config.append("defaults")
    config.append("  log global")
    config.append("  retries 3")
    config.append("  maxconn 2000")
    config.append("  timeout connect 25000")
    config.append("  timeout client 50000")
    config.append("  timeout server 50000")
    config.append("")
    return "\n".join(config)


def app_config(marathon_server, app_id, index, port, app):
    protocol = "tcp"
    for health_check in app["healthChecks"]:
        if health_check["portIndex"] == index:
            if health_check["protocol"] == "HTTP":
                protocol = "http"

    config = []

    if protocol == "http":
        config.append("listen {}-{}".format(app_id.replace("/", ""), port))
        config.append("  bind 0.0.0.0:{}".format(port))
        config.append("  log global")
        config.append("  mode http")
        config.append("  option httplog")
        config.append("  option dontlognull")
        config.append("  retries 3")
        config.append("  option redispatch")
        config.append("  timeout connect 25000")
        config.append("  timeout client 60000")
        config.append("  timeout server 60000")

    elif protocol == "tcp":
        config.append("listen {}-{}".format(app_id.replace("/", ""), port))
        config.append("  bind 0.0.0.0:{}".format(port))
        config.append("  mode tcp")
        config.append("  option tcplog")
        config.append("  balance leastconn")
    else:
        return ""

    for task in app['tasks']:
        config.append("  server {}-{} {}:{} check".format(app_id.replace("/", ""), index, task["host"], task["ports"][index]))

    return "\n".join(config)


def apps_config(marathon_server):
    import requests
    apps_response = requests.get("http://{}/v2/apps".format(marathon_server), params={'embed': 'apps.tasks'}).json()

    config = []
    for app in apps_response['apps']:
        app_id = app['id']
        for index, port_mapping in enumerate(app['container']['docker'].get('portMappings', [])):
            elem_config = app_config(marathon_server, app_id, index, port_mapping['servicePort'], app)
            if elem_config:
                config.append(elem_config)

    return "\n\n".join(config)


def generate_config(marathon_server):
    config = [
        header_config(),
        apps_config(marathon_server)
    ]
    return "\n".join(config)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generates a new configuration file for HAProxy \
                                     from the specified Marathon servers, replaces the file in \
                                     /etc/haproxy and restarts the service.")

    parser.add_argument('positional_args', metavar='N', type=str, nargs='+',
                        help='list of marathon servers to be queried')

    args = parser.parse_args()
    marathon_server = random.choice(args.positional_args)

    # Generate the new config from the template.
    print 'Generating configuration for haproxy.'
    new_config = generate_config(marathon_server)

    # See if this new config is different. If it is then restart using it.
    # Otherwise just delete the temporary file and do nothing.
    print 'Comparing to existing configuration.'
    old_config = file_contents(haproxy_conf_file)

    if new_config != old_config:
        print 'Existing configuration is outdated.'

        # Overwite the existing config file.
        print 'Writing new configuration.'
        file_contents(filename=haproxy_conf_file, content=new_config)

        print 'Reloading haproxy.'
        reload_haproxy()

    else:
        print 'Configuration unchanged. Skipping restart.'
