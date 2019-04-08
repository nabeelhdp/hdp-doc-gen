#!/usr/bin/python3

import base64
import json
import os
import urllib.request

from configmapping import get_component_config, filter_parameters
from connectionchecks import test_socket
from readconfig import get_config_params


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


def print_config_settings(component_config, params_set):

    print('<h5><span style=\"color: rgb(0,112,224);\">{}</span></h5>'.format(
        'Configuration parameters')
    )

    for component_name, component_value in component_config.items():
        print('<h4><span style=\"color: rgb(0,112,224);\">{}</span></h4>'.format(component_name))
        add_config_items(component_name, component_value, params_set[component_name])
        print("</tbody></table>")


def add_config_items(component_name, component_config, component_params):
    print('<table class=\"relative-table wrapped\" style=\"width: 99.9%;\">'
          '<colgroup>'
          '<col style=\"width: 30%;\"/>'
          '<col style=\"width: 40%;\"/>'
          '<col style=\"width: 10%;\"/>'
          '<col style=\"width: 20%;\"/>'
          '</colgroup>'
          '<tbody>'
          '<tr>'
          '<th align="left">Description</th>'
          '<th align="left">Value</th>'
          '<th align="left">Tag</th>'
          '<th align="left">key</th>'
          '</tr>'
          )

    for tag_name, tag_value in component_config.items():

        for k, v in tag_value.items():
            print('<tr>')
            print("<td colspan=\"1\">{}</td>".format(component_params[tag_name][k]))
            print("<td colspan=\"1\">{}</td>".format(v))
            print("<td colspan=\"1\">{}</td>".format(tag_name))
            print("<td colspan=\"1\">{}</td>".format(k))
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
    print("<html><body>")
    service_list = send_ambari_request(url_suffix="/services/")
    print_service_components(service_list)

    full_config = send_ambari_request(url_suffix="/configurations/service_config_versions?is_current=true")
    component_config_ = get_component_config(full_config)
    paramfile = os.path.join(os.path.dirname(__file__), "../conf/params.json")
    params_set = {}
    with open(paramfile) as f:
        params_set = json.load(f)

    component_config = filter_parameters(
        component_config_,
        params_set
    )

    print_config_settings(component_config, params_set)
    print("</body></html>")

if __name__ == "__main__":
    main()
