#!/usr/bin/env python3

'''
This is a python module that provides a simple interface to the Cordra API.
It contains a single class, Cordra, which provides methods for accessing
and manipulating Cordra objects. The class contains the following methods:
    - get_schemas: returns a list of Cordra objects that match a specific query
    - get: returns the contents of a specific Cordra object
    - create: creates a new Cordra object
    - update: updates an existing Cordra object

    - list_versions: returns a list of versions of a specific Cordra object
    - create_version: creates a new version of an existing Cordra object
'''

import sys

import requests

import libschema


class Cordra:
    def __init__(self, url, username, password):
        self.url = url
        self.username = username
        self.password = password

        # if username and password are provided, get a token
        if self.username and self.password:
            token = self.get_token()
            self.headers = {"Authorization": f"Bearer {token}"}
        else:
            self.headers = {}


    '''
    get_token: gets a token from Cordra
    '''
    def get_token(self):
        response = requests.post('{}/auth/token'.format(self.url), json={'username': self.username, 'password': self.password})
        if response.status_code != 200:
            print('Error: Unable to get token from Cordra')
            sys.exit(1)
        return response.json()['access_token']


    '''
    get_schemas: returns a list of Cordra objects that match a specific query
    '''
    def get_schemas(self):
        response = requests.get(f'{self.url}/objects/?query=type:"Schema"', headers=self.headers)
        if response.status_code != 200:
            print('Error: Unable to retrieve objects from Cordra')
            sys.exit(1)
        schema_list = response.json()['results']
        summary = {}
        for item in schema_list:
            pid = item['id']
            type = item['content']['name']
            base_uri = item['content'].get('baseUri')
            version = libschema.get_version(item['content']['schema'])
            id = item['content']['schema'].get('$id')
            summary[type] = {
                'pid': pid,
                'id': id,
                'version': version,
                'base_uri': base_uri}

        return summary


    '''
    get_versions: returns a list of versions of a specific Cordra object
    '''
    def get_versions(self, pid):
        # get the versions of the object
        response = requests.get(f'{self.url}/versions/?objectId={pid}', headers=self.headers)
        if response.status_code != 200:
            print('Error: Unable to retrieve versions from Cordra')
            sys.exit(1)
        version_list = response.json()
        # create simple list of versions, excluding the current version
        versions = []
        for item in version_list:
            if item['id'] != pid:
                versions.append(item['id'])
        return versions


    '''
    create: creates a new Cordra object
    '''
    def create(self, obj, type, full=False):
        full = '&full' if full else ''
        response = requests.post(f'{self.url}/objects/?type={type}{full}', json=obj, headers=self.headers)
        if response.status_code != 200:
            print('Error: Unable to create object in Cordra')
            sys.exit(1)
        return response.json()


    '''
    update: updates an existing Cordra object
    '''
    def update(self, pid, obj, full=False):
        full = '?full' if full else ''
        response = requests.put(f'{self.url}/objects/{pid}{full}', json=obj, headers=self.headers)
        if response.status_code != 200:
            print('Error: Unable to update object in Cordra')
            sys.exit(1)
        return response.json()


if __name__ == '__main__':
    print('This is a module, not a script!')