#!/usr/bin/env python3

import os
import sys
import json

import requests


'''
Default configuration for the tools
'''
default_config = {
    "cordra_url": "https://data.e-rihs.io",
    "cordra_user": "admin",
    "cordra_pass": None,
    "github_repo": "e-rihs/schema",
    "github_branch": "main",
    "cl_techniques_full_url": "http://hdl.handle.net/21.11158/0002-d6f1-f86f-d248?urlappend=%26full%26refresh"
}




''' read and update configuration from config.json'''
def get_config():
    # create copy of default config
    config = default_config.copy()
    # read config from file
    if os.path.isfile('config.json'):
        with open('config.json', 'r') as f:
            # update config with the values from config.json
            config.update(json.load(f))
    return config


''' get country list from the CL Techniques URL '''
def get_countries():
    url = "https://hdl.handle.net/21.11158/0002-a36b-9f90-6c16"
    response = requests.get(url)
    if response.status_code != 200:
        print('!! Error: Unable to retrieve country list !!')
        print(f' - response from Cordra: {response.text}')
        sys.exit(1)
    return response.json()['list']


if __name__ == '__main__':
    print('This is a module, not a script!')