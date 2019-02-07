
#!/usr/bin/python

import subprocess
import os
import sys
import socket
import re
import base64
import json
import time
import ConfigParser
from ConfigParser import SafeConfigParser
import urllib2
from urllib2 import URLError
from readconfig import get_config_params
from connectionchecks import is_valid_hostname,test_socket

# Print response from new Ambari server
def send_ambari_request(url_suffix="",service_type="services"):
    config_file = os.path.join(os.path.dirname(__file__),"config.ini")
    config_dict = {}
    config_dict = get_config_params(config_file)
    ambari_server_host = str(config_dict['ambari_server_host'])
    ambari_server_port = str(int(config_dict['ambari_server_port']))
    ambari_server_timeout = float(config_dict['ambari_server_timeout'])
    cluster_name = str(config_dict['cluster_name'])
    ambari_user = config_dict['ambari_user']
    ambari_pass = config_dict['ambari_pass']

    # Test socket connectivity to Ambari server port
    test_socket(ambari_server_host,ambari_server_port,"Ambari server")

    # Construct URL request for metrics data. This needs to be changed when moving to JMX
    base_url = "http://"+ ambari_server_host +":" + ambari_server_port + "/api/v1/clusters/" + cluster_name
    url = ""
    if service_type == "services":
        url = base_url + "/services/" + url_suffix
    if service_type == "configuration" :
        url = base_url + "/configurations/service_config_versions?service_name=" + url_suffix + "&is_current=true"
    auth_string = "%s:%s" % (ambari_user, ambari_pass)
    auth_encoded = 'Basic %s' % base64.b64encode(auth_string).strip()
    req = urllib2.Request(url)
    req.add_header('Authorization', auth_encoded)

    httpHandler = urllib2.HTTPHandler()
    #httpHandler.set_http_debuglevel(1)
    opener = urllib2.build_opener(httpHandler)

    try:
      response = opener.open(req,timeout=ambari_server_timeout)
      return json.load(response)
    except (urllib2.URLError, urllib2.HTTPError) as e:
      print 'Requested URL not found. Error:', e

#def validate_ambari_json(json_file):
#    try:
#        with open(json_file) as f:
#          property_file = json.load(f)
#          property_type = property_file['Clusters']['desired_config']['type']
#          property_entries = property_file['Clusters']['desired_config']['properties']
#          if (property_type == "capacity-scheduler"):
#            for k,v in property_entries.iteritems():
#              if not (k.startswith('yarn.scheduler.capacity.')):
#                print "Capacity Scheduler entries should begin with yarn.scheduler.capacity.XXX. Please remove other entries unrelated to Capacity Scheduler"
#                return False
#            return property_file
#          else:
#            print "Incorrect syntax for Capacity Scheduler configuration json file. No type capacity_scheduler specified."
#            return False
#    except ValueError as e:
#        print('Invalid json file provided. Error : %s' % e)
#        return False

def main():

  #scheduler_file = sys.argv[1] if len(sys.argv) >= 2 else os.path.join(os.path.dirname(__file__),"scheduler.json")
  service_list = send_ambari_request()
  print('<h5><span style=\"color: rgb(0,112,224);\">{}</span></h5>'.format('Component Host nodes'))
  for services in service_list['items']:
    #print(services['ServiceInfo']['service_name']," : ",services['href'])
    service_components_response = send_ambari_request(services['href'].split('/')[-1])
    start_table(service_components_response['ServiceInfo']['service_name'])
    for components in service_components_response['components']:
        print('<tr>')
        if not components['ServiceComponentInfo']['component_name'].endswith('_CLIENT'):
            print("<td colspan=\"1\">{}</td>".format(components['ServiceComponentInfo']['component_name']))
            component_name = components['ServiceComponentInfo']['component_name']
            component_response = send_ambari_request(service_components_response['ServiceInfo']['service_name'] + "/components/" + component_name)
            print("<td colspan=\"1\">")
            for sections in component_response['host_components']:
                print("{} ".format(sections['HostRoles']['host_name']))
            print("</td>")
        print("</tr>")
    print('</tbody></table>')



def start_table(title):
    print('<h4><span style=\"color: rgb(0,112,224);\">{}</span></h4>'.format(title))
    print('<table class=\"relative-table wrapped\" style=\"width: 99.9451%;\"><colgroup><col style=\"width: 20%;\"/><col style=\"width: 80%;\"/></colgroup>')
    print('<tbody><tr><th>Component</th><th>Host</th></tr>')

    #if component_name == 'HBASE_MASTER':
    #    print("\tZookeeperQuorum : {}".format(component_response['metrics']['hbase']['master']['ZookeeperQuorum']))
    #if component_name == 'HIVE_SERVER':
    #    hs2_config_response = send_ambari_request("HIVE","configuration")
    #    for config_types in hs2_config_response['items'][1]['configurations']:
    #        if config_types['type'] == 'hive-site':
    #            print("\tJDBC URL : {}".format(config_types['properties']['javax.jdo.option.ConnectionURL']))


if __name__ == "__main__":
  main()
