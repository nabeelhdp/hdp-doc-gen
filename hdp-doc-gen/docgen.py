# !/usr/bin/python3

import os
import re
import base64
import json
import urllib.request
from readconfig import get_config_params
from connectionchecks import test_socket
from getmykeys import get_each_key, get_all_keys
import configmapping

# Print response from the Ambari server
def send_ambari_request(url_suffix=""):
    config_file = os.path.join(os.path.dirname(__file__), "../conf/config.ini")
    ambconf = {}
    ambconf = get_config_params(config_file)

    # Test socket connectivity to Ambari server port
    test_socket(
        str(ambconf['ambari_server_host']),
        int(ambconf['ambari_server_port']),
        "Ambari server"
    )

    # Construct URL request for metrics data
    base_url = "http://{}:{}/api/v1/clusters/{}".format(
        str(ambconf['ambari_server_host']),
        ambconf['ambari_server_port'],
        ambconf['cluster_name']
    )

    url = "{}{}".format(base_url, url_suffix)
    auth_string = "{}:{}".format(ambconf['ambari_user'], ambconf['ambari_pass'])
    auth_encoded = 'Basic {}'.format(
        base64.urlsafe_b64encode(
            auth_string.encode('UTF-8')
        ).decode('ascii')
    )
    req = urllib.request.Request(url)
    req.add_header('Authorization', auth_encoded)

    httpHandler = urllib.request.HTTPHandler()
    # httpHandler.set_http_debuglevel(1)
    opener = urllib.request.build_opener(httpHandler)

    try:
        response = opener.open(req, timeout=int(ambconf['ambari_server_timeout']))
        return json.load(response)
    except (urllib.request.URLError, urllib.request.HTTPError) as e:
        print('Requested URL not found. Error:{}'.format(e))


def print_config_settings():
    # config_url = "/configurations/service_config_versions?service_name=/"
    # url = "{}{}{}&is_current=true".format(base_url, config_url, url_suffix)
    fullconfig = send_ambari_request()
    fullkeylist = get_all_keys(fullconfig)
    print('<h5><span style=\"color: rgb(0,112,224);\">{}</span></h5>'.format(
        'Configuration parameters')
    )
    add_kv_table(
        "Cluster Configuration", 'Parameter', 'Value')
    add_config_items(fullconfig)
    print("</tr></tbody></table>")

    pass


def add_config_items(config):

    configitemslist = [
        configmapping.get_cluster_mapping(config),
        configmapping.get_hdfs_mapping(config),
        configmapping.get_yarn_mapping(config),
        configmapping.get_kafka_mapping(config),
        configmapping.get_zk_mapping(config),
        configmapping.get_hive_mapping(config)
    ]
    for configitems in configitemslist:
        for k, v in configitems.items():
            if k == 'CategoryName':
                print('<tr>')
                print("<td colspan=\"0\"><b>{}</b></td>".format(v))
                print('</tr>')
                continue
            print('<tr>')
            print("<td colspan=\"1\">{}</td>".format(k))
            print("<td colspan=\"1\">{}</td>".format(v))
            print('</tr>')


def print_service_components(service_list):
    print('<h5><span style=\"color: rgb(0,112,224);\">{}</span></h5>'.format(
        'Component Host nodes')
    )

    for services in service_list['items']:

        servicecomponents = send_ambari_request(
            url_suffix="/services/{}".format(services['href'].split('/')[-1])
        )
        component_name = servicecomponents['ServiceInfo']['service_name']
        add_kv_table(
            component_name, 'Component', 'Host')

        for subcomponents in servicecomponents['components']:
            subcomponent_name = subcomponents['ServiceComponentInfo']['component_name']
            print('<tr>')
            if not subcomponent_name.endswith('_CLIENT'):
                print("<td colspan=\"1\">{}</td>".format(
                    subcomponent_name)
                )
                component_response = send_ambari_request(
                    "/services/{}/components/{}".format(
                        component_name,
                        subcomponent_name
                    )
                )
                print("<td colspan=\"1\">")
                for sections in component_response['host_components']:
                    print("{} ".format(sections['HostRoles']['host_name']))
                print("</td>")
            print("</tr>")
        print("</tbody></table>")


def add_kv_table(title, keycol, valcol):
    print('<h4><span style=\"color: rgb(0,112,224);\">{}</span></h4>'.format(title))
    print('<table class=\"relative-table wrapped\" style=\"width: 99.9%;\">'
          '<colgroup><col style=\"width: 20%;\"/><col style=\"width: 80%;\"/></colgroup>'
          '<tbody><tr><th align="left">{}</th><th align="left">{}</th></tr>'.format(keycol, valcol)
          )


def main():
    print_config_settings()
    amb_service_response = send_ambari_request(url_suffix="/services/")
    print_service_components(amb_service_response)


if __name__ == "__main__":
    main()

    # if component_name == 'HBASE_MASTER':
    #    print("\tZookeeperQuorum : {}".format(component_response['metrics']['hbase']['master']['ZookeeperQuorum']))
    # if component_name == 'HIVE_SERVER':
    #    hs2_config_response = send_ambari_request("HIVE","configuration")
    #    for config_types in hs2_config_response['items'][1]['configurations']:
    #        if config_types['type'] == 'hive-site':
    #            print("\tJDBC URL : {}".format(config_types['properties']['javax.jdo.option.ConnectionURL']))
