
import json
import string
import sys
import os
import re
from configparser import SafeConfigParser
from connectionchecks import is_valid_hostname


def get_config_params(config_file):
  try:
    with open(config_file) as f:
      try:
        parser = SafeConfigParser()
        parser.readfp(f)
      except (ConfigParser.Error) as  err:
        print('Could not parse: {} '.format(err))
        return False
  except IOError as e:
    print("Unable to access %s. Error %s \nExiting" % (config_file, e))
    sys.exit(1)

  ambari_server_host = parser.get('ambari_config', 'ambari_server_host')
  ambari_server_port = parser.get('ambari_config', 'ambari_server_port')
  ambari_user = parser.get('ambari_config', 'ambari_user')
  ambari_pass = parser.get('ambari_config', 'ambari_pass')
  ambari_server_timeout = parser.get('ambari_config', 'ambari_server_timeout')
  cluster_name = parser.get('ambari_config', 'cluster_name')

  if not ambari_server_port.isdigit():
    print("Invalid port specified for Ambari Server. Exiting")
    sys.exit(1)
  if not is_valid_hostname(ambari_server_host):
    print("Invalid hostname provided for Ambari Server. Exiting")
    sys.exit(1)
  if not ambari_server_timeout.isdigit():
    print("Invalid timeout value specified for Ambari Server. Using default of 30 seconds")
    ambari_server_timeout = 30

  # Prepare dictionary object with config variables populated
  config_dict = {}
  config_dict["ambari_server_host"] = ambari_server_host
  config_dict["ambari_server_port"] = ambari_server_port
  config_dict["ambari_server_timeout"] = ambari_server_timeout

  if re.match(r'^[A-Za-z0-9_]+$', cluster_name):
    config_dict["cluster_name"] = cluster_name
  else:
    print("Invalid Cluster name provided. Cluster name should have only alphanumeric characters and underscore. Exiting")
    return False

  if re.match(r'^[a-zA-Z0-9_.-]+$', ambari_user):
    config_dict["ambari_user"] = ambari_user
  else:
    print("Invalid Username provided. Exiting")
    return False

  config_dict["ambari_pass"] = ambari_pass

  return config_dict

