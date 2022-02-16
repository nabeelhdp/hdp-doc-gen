import re


def get_component_config(master_config):
    '''

    :param master_config: The full dictionary object returned by top level call to Ambari based on the url below :
    base_url = "http://{}:{}/api/v1/clusters/{}".format(
        str(ambconf['ambari_server_host']),
        ambconf['ambari_server_port'],
        ambconf['cluster_name']
    )
    :return:
    Returns a nested dictionary, where
        1) first level of keys is the component . Eg. HDFS
        2) second level is the tag-type, filename equivalent in Ambari's internal format. Eg - hdfs-site
        3) third level is the individual keys, and their values. Eg. dfs.blocksize
        So value of the last object would be master_config['HDFS']['hdfs-site']['dfs.blocksize']

    '''

    component_config = {}

    for items in master_config['items']:
        href = items['href'].split("/")[-1]
        component_name = re.search("service_config_versions\?service_name=(.+?)&.*", href).group(1)
        if component_name != None:
            component_config[component_name] = {}
            for sub_items in items['configurations']:
                tag_name = sub_items['type']
                component_config[component_name][tag_name] = {}
                for k, v in sub_items['properties'].items():
                    component_config[component_name][tag_name][k] = v
    return component_config

def filter_parameters(component_config_full, params_set):
    component_config = {}
    for component_name, component_value in params_set.items():
        component_config[component_name] = {}
        for tag_name, tag_value in component_value.items():
            component_config[component_name][tag_name] = {}
            try:
                for key, value in tag_value.items():
                    component_config[component_name][tag_name][key] = component_config_full[component_name][tag_name][key]
            except KeyError as e:
                pass 
    return component_config


def main():
    pass


if __name__ == "__main__":
    main()
