#!/usr/bin/env python3

import os
import json

'''
Default configuration for the tools
'''
default_config = {
    "cordra_url": "https://data.e-rihs.io",
    "cordra_user": "admin",
    "cordra_pass": None,
    "github_repo": "e-rihs/schema",
    "github_branch": "main",
    "cl_techniques_url": "http://hdl.handle.net/21.11158/0002-d6f1-f86f-d248?urlappend=%26full%26refresh"
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


if __name__ == '__main__':
    print('This is a module, not a script!')