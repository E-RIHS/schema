#!/usr/bin/env python3

'''
This is a python module that provides a simple interface to the GitHub API.
It contains a single class, GitHub, which provides methods for accessing
the GitHub API. The class contains two methods:
    - get_schemas: returns a list of all the schemas in the GitHub repository
    - get_schema: returns the contents of a specific schema file
'''

import sys

import requests


class GitHub:
    def __init__(self, repo):
        self.repo = repo
        self.api_url = 'https://api.github.com/repos/{}/contents'.format(self.repo)


    '''
    get_schemas: returns a list of all the schemas in the GitHub repository
    '''
    def get_schemas(self):
        response = requests.get(self.api_url)
        if response.status_code != 200:
            print('Error: Unable to retrieve schema list from GitHub')
            sys.exit(1)
        schemas = []
        for item in response.json():
            if item['type'] == 'file' and item['name'].endswith('.schema.json'):
                schemas.append(item['download_url'])
        return schemas


    '''
    get_schema: returns the contents of a specific schema file
    '''
    def get_schema(self, schema):
        response = requests.get(schema)
        if response.status_code != 200:
            print('Error: Unable to retrieve schema from GitHub')
            sys.exit(1)
        try:
            schema_json =  response.json()
        except:
            # filename from schema url
            filename = schema.split('/')[-1]
            print(f'Error: {filename} -> Invalid JSON:!')
            sys.exit(1)
        return response.json()
    

if __name__ == '__main__':
    print('This is a module, not a script!')
