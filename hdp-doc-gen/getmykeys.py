import json
from six import iteritems

def get_all_keys(dictionary):
    """
        Method to get all keys from a nested dictionary as a List
        Args:
            dictionary: Nested dictionary
        Returns:
            List of keys in the dictionary
    """
    result_list = []

    def recursion(dictionary,keypath=""):
        for key, value in iteritems(dictionary):
            if isinstance(value, dict):
                result_list.append(key)
                keypath = keypath + "{ " + key + " }"
                recursion(keypath=keypath,dictionary=value)
            elif isinstance(value, list):
                result_list.append(key)
                keypath = keypath + "[ " + key + " ]"
                for list_items in value:
                    # Make sure the items inside the list is iterable
                    if hasattr(list_items, 'items'):
                        recursion(keypath=keypath,dictionary=list_items)
            else:
                keypath += key + " : " + str(value) + " "
                result_list.append(keypath)

    recursion(dictionary=dictionary)
    return result_list

def get_each_key(wantedkey,fullkeylist):

    for key in fullkeylist:
        items = key.split()
        if wantedkey in items:
            return (wantedkey +": "+items[-1])
            break

def main():

    fullkeylist = get_all_keys(json.load(open('json/cluster.json')))
    wantedkeys = [
        'fs.defaultFS',
        'namenode_heapsize',
        'dfs.blocksize',
        'security_type'
    ]
    for wantedkey in wantedkeys:
        print(get_each_key(wantedkey,fullkeylist = fullkeylist))

if __name__ == "__main__":
  main()
