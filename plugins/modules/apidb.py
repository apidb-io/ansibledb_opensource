from ansible.module_utils.basic import *
from multiprocessing import Pool
from contextlib import closing
from functools import partial
import os
import json
import requests
import subprocess


def sanitiseDict(d):

    sankeys = open("collections/ansible_collections/apidb/ansibledb_opensource/roles/apidb_post/library/keys_to_sanitise.json", 'r').read()
    keys = json.loads(sankeys)
    keys_to_sanitise = keys['keys_to_sanitise']
    for k in keys_to_sanitise:
        if k in d.keys():
            d.update({k: 'EXCLUDED'})
    for v in d.values():
        if isinstance(v, dict):
            sanitiseDict(v)
    return d


def apidb(directory,p,apiendpoint,filename):
    API_ENDPOINT = p["ansibledb_server"] + "/api/" + apiendpoint
        'Content-Type': 'text/json',
        'Accept':'application/json'
     }
    data = open(directory + filename, 'rb').read()
    jdata = sanitiseDict(json.loads(data))
    r = requests.post(url = API_ENDPOINT, headers=headers, data=json.dumps(jdata),verify=False)
    result = r.text
    statuscode = r.status_code
    meta = {"statuscode" : statuscode, "keys_to_sanitise" : 'key', "endpoint": API_ENDPOINT}
    return statuscode

def postdata(p):
    statuscode = ''
    result = ''
    is_error = False
    has_changed = False
    meta = {"statuscode" : statuscode, "response" : result}
    directory='/tmp/facts/'
    agents = p["threads"] # How many instances to run
    chunksize = p["chunksize"]  # How many servers per agents
    apiendpoint = "ansiblefacts"
    filename = os.listdir(directory)
    with closing(Pool(processes=agents)) as pool:
        func = partial(apidb, directory, p, apiendpoint)
        result = pool.map(func,filename,chunksize)
        pool.terminate()
    return is_error, has_changed, meta


def main():
    fields = {
        "ansibledb_server": {"default": "test", "type": "str"},
        "threads": {"default": 3, "type": "int"},
        "chunksize": {"default": 10, "type": "int"},
    }

    module = AnsibleModule(argument_spec=fields)
    is_error, has_changed, result = postdata(module.params)

    if not is_error:
        module.exit_json(changed=has_changed, meta=result)
    else:
        module.fail_json(msg="Error", meta=result)

if __name__ == '__main__':
    main()
