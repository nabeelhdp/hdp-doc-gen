def get_hdfs_mapping(config):
    hdfsconfigmap = {
        "CategoryName" : 'HDFS',
        "Namenode URL": config['service_config_versions'][0]['configurations'][0]['properties'][
            'fs.defaultFS'],
        "Namenode Heapsize": config['service_config_versions'][0]['configurations'][1]['properties'][
            'namenode_heapsize'],
        "HDFS Blocksize(MB)": int(config['service_config_versions'][0]['configurations'][11]['properties'][
                'dfs.blocksize']) / 1024 / 1024,
        "Datanode HDFS Data Dir": config['service_config_versions'][0]['configurations'][11]['properties'][
            'dfs.datanode.data.dir'],
        "JournalNode Edits Dir": config['service_config_versions'][0]['configurations'][11]['properties'][
            'dfs.journalnode.edits.dir'],
        "Namenode HDFS Data Dir": config['service_config_versions'][0]['configurations'][11]['properties'][
            'dfs.namenode.name.dir'],
        "HDFS Replication factor": config['service_config_versions'][0]['configurations'][11]['properties'][
            'dfs.replication'],
        "Namenode Handler count": config['service_config_versions'][0]['configurations'][11]['properties'][
            'dfs.namenode.handler.count']
    }
    return hdfsconfigmap
    pass


def get_hive_mapping(config):

    hiveconfigmap = {
        "CategoryName" : 'Hive',
        "Hive Execution mode": config['service_config_versions'][1]['configurations'][1]['properties'][
            'hive.execution.mode'],
        "Hive LLAP Executor count": config['service_config_versions'][1]['configurations'][1]['properties'][
            'hive.llap.daemon.num.executors'],
        "Hive LLAP Daemon Queue": config['service_config_versions'][1]['configurations'][1]['properties'][
            'hive.llap.daemon.queue.name'],
        "Hive LLAP Execution mode": config['service_config_versions'][1]['configurations'][1]['properties'][
            'hive.llap.execution.mode'],
        "Hive Impersonation Enabled": config['service_config_versions'][1]['configurations'][1]['properties'][
            'hive.server2.enable.doAs'],
        "Tez pre-create sessions": config['service_config_versions'][1]['configurations'][1]['properties'][
            'hive.server2.tez.initialize.default.sessions'],
        "Hive Heapsize": config['service_config_versions'][1]['configurations'][2]['properties'][
            'hive.heapsize'],
        "Hive ZK namespace": config['service_config_versions'][1]['configurations'][2]['properties'][
            'hive.server2.zookeeper.namespace'],
        "Hive ZK quorum": config['service_config_versions'][1]['configurations'][2]['properties'][
            'hive.zookeeper.quorum'],
        "Hive metastore heapsize": config['service_config_versions'][1]['configurations'][6]['properties'][
            'hive.metastore.heapsize'],
        "Hive DB name": config['service_config_versions'][1]['configurations'][6]['properties'][
            'hive_database_name'],
        "Hive DB type": config['service_config_versions'][1]['configurations'][6]['properties'][
            'hive_database_type'],
        "Hive Security Authorization": config['service_config_versions'][1]['configurations'][6]['properties'][
            'hive_security_authorization'],
        "Hive DB Schema name": config['service_config_versions'][1]['configurations'][2]['properties'][
            'ambari.hive.db.schema.name'],
        "Number of LLAP nodes": config['service_config_versions'][1]['configurations'][8]['properties'][
            'num_llap_nodes'],
        "Hive LLAP Enabled": config['service_config_versions'][1]['configurations'][8]['properties'][
            'enable_hive_interactive']
    }
    return hiveconfigmap
    pass


def get_yarn_mapping(config):
    yarnconfigmap = {
        "CategoryName" : 'YARN',
        "MapReduce local directory": config['service_config_versions'][3]['configurations'][1]['properties'][
            'mapred.local.dir'],
        "MapReduce jobhistory server": config['service_config_versions'][3]['configurations'][1]['properties'][
            'mapreduce.jobhistory.address'],
        "MapReduce Map memory": config['service_config_versions'][3]['configurations'][1]['properties'][
            'mapreduce.map.memory.mb'],
        "MapReduce Reduce memory": config['service_config_versions'][3]['configurations'][1]['properties'][
            'mapreduce.reduce.memory.mb'],
        "MapReduce AM memory": config['service_config_versions'][3]['configurations'][1]['properties'][
            'mapreduce.reduce.memory.mb'],
        "MapReduce io.sort.mb": config['service_config_versions'][3]['configurations'][1]['properties'][
            'yarn.app.mapreduce.am.resource.mb'],
        "YARN NodeManager Heap": config['service_config_versions'][5]['configurations'][7]['properties'][
            'nodemanager_heapsize'],
        "YARN ResourceManager Heap": config['service_config_versions'][5]['configurations'][7]['properties'][
            'resourcemanager_heapsize'],
        "YARN CGroups enabled": config['service_config_versions'][5]['configurations'][7]['properties'][
            'yarn_cgroups_enabled'],
        "YARN ATS Heap size": config['service_config_versions'][5]['configurations'][7]['properties'][
            'apptimelineserver_heapsize'],
        "YARN Log Aggregation enabled": config['service_config_versions'][5]['configurations'][13]['properties'][
            'yarn.log-aggregation-enable'],
        "YARN Log Server URL": config['service_config_versions'][5]['configurations'][13]['properties'][
            'yarn.log.server.url'],
        "YARN Log Server Web Service URL": config['service_config_versions'][5]['configurations'][13]['properties'][
            'yarn.log.server.web-service.url'],
        "YARN Nodemanager Local Dir": config['service_config_versions'][5]['configurations'][13]['properties'][
            'yarn.nodemanager.local-dirs'],
        "YARN Nodemanager Log Dir": config['service_config_versions'][5]['configurations'][13]['properties'][
            'yarn.nodemanager.log-dirs'],
        "YARN Nodemanager log retention hours":int(config['service_config_versions'][5]['configurations'][13][
             'properties']['yarn.nodemanager.log.retain-seconds'])/ 3600,
        "YARN NM allocated memory": config['service_config_versions'][5]['configurations'][13]['properties'][
            'yarn.nodemanager.resource.memory-mb'],
        "YARN NM allocated vcpu": config['service_config_versions'][5]['configurations'][13]['properties'][
            'yarn.nodemanager.resource.cpu-vcores'],
        "YARN RM address": config['service_config_versions'][5]['configurations'][13]['properties'][
            'yarn.resourcemanager.address'],
        "YARN RM HA enabled": config['service_config_versions'][5]['configurations'][13]['properties'][
            'yarn.resourcemanager.ha.enabled'],
        "YARN RM ZK address": config['service_config_versions'][5]['configurations'][13]['properties'][
            'yarn.resourcemanager.zk-address'],
        "YARN RM state-store ZK path": config['service_config_versions'][5]['configurations'][13]['properties'][
            'yarn.resourcemanager.zk-state-store.parent-path']
    }
    return yarnconfigmap
    pass


def get_kafka_mapping(config):
    kafkaconfigmap = {
        "CategoryName" : 'Kafka',
        "Kafka auto create topics": config['service_config_versions'][2]['configurations'][1]['properties'][
            'auto.create.topics.enable'],
        "Kafka default replication factor": config['service_config_versions'][2]['configurations'][1]['properties'][
            'default.replication.factor'],
        "Kafka delete topic enabled": config['service_config_versions'][2]['configurations'][1]['properties'][
            'delete.topic.enable'],
        "Kafka Log retention hours": config['service_config_versions'][2]['configurations'][1]['properties'][
            'log.retention.hours'],
        "Kafka max message size": config['service_config_versions'][2]['configurations'][1]['properties'][
            'message.max.bytes'],
        "Kafka zk connect": config['service_config_versions'][2]['configurations'][1]['properties'][
            'zookeeper.connect']
    }
    return kafkaconfigmap
    pass


def get_zk_mapping(config):
    zkconfigmap = {
        "CategoryName" : 'Zookeeper',
        "Zookeeper autopurge Interval": config['service_config_versions'][6]['configurations'][0]['properties'][
            'autopurge.purgeInterval'],
        "Zookeeper Snapshot retain count": config['service_config_versions'][6]['configurations'][0]['properties'][
            'autopurge.snapRetainCount'],
        "Zookeeper Data Dir": config['service_config_versions'][6]['configurations'][0]['properties']['dataDir'],
        "Zookeeper Log Directory": config['service_config_versions'][6]['configurations'][1]['properties'][
            'zk_log_dir'],
        "Zookeeper Heap Size": config['service_config_versions'][6]['configurations'][1]['properties'][
            'zk_server_heapsize'],
        "Zookeeper Log Max backup size": config['service_config_versions'][6]['configurations'][2]['properties'][
            'zookeeper_log_max_backup_size'],
        "Zookeeper Log backup file count": config['service_config_versions'][6]['configurations'][2]['properties'][
            'zookeeper_log_number_of_backup_files']
    }
    return zkconfigmap
    pass


def get_cluster_mapping(config):

    clusterconfigmap = {
        "CategoryName" : 'Cluster',
        "Cluster version": config['Clusters']['version']
    }

    return clusterconfigmap


def main():
    pass


if __name__ == "__main__":
    main()
