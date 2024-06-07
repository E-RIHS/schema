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
            print(response.text)
            print('!! Error: Unable to get token from Cordra !!')
            print(f' - response from Cordra: {response.text}')
            sys.exit(1)
        return response.json()['access_token']


    '''
    get_schemas: returns a list of Cordra objects that match a specific query
    '''
    def get_schemas(self):
        response = requests.get(f'{self.url}/objects/?query=type:"Schema"', headers=self.headers)
        if response.status_code != 200:
            print(response.text)
            print('!! Error: Unable to retrieve objects from Cordra !!')
            print(f' - response from Cordra: {response.text}')
            sys.exit(1)
        schema_list = response.json()['results']
        summary = {}
        for item in schema_list:
            pid = item['id']
            type = item['content']['name']
            base_uri = item['content'].get('baseUri')
            name, version = libschema.extract_schema_details(item['content']['schema']['$id'])
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
            print('!! Error: Unable to retrieve versions from Cordra !!')
            print(f' - response from Cordra: {response.text}')
            sys.exit(1)
        version_list = response.json()
        # create simple list of versions, excluding the current version
        versions = []
        for item in version_list:
            if item['id'] != pid:
                versions.append(item['id'])
        return versions
    

    '''
    get_by_id: returns the contents of a specific Cordra object
    '''
    def get_by_id(self, pid):
        response = requests.get(f'{self.url}/objects/{pid}', headers=self.headers)
        if response.status_code != 200:
            print('!! Error: Unable to retrieve object from Cordra !!')
            print(f' - response from Cordra: {response.text}')
            sys.exit(1)
        return response.json()


    '''
    query: returns a list of Cordra objects that match a specific query
    '''
    def query(self, query, page_num=0, page_size=-1):
        post_data = {
            'query': query,
            'pageNum': page_num,
            'pageSize': page_size
        }
        response = requests.post(f'{self.url}/search', json=post_data, headers=self.headers)
        if response.status_code != 200:
            print('!! Error: Unable to retrieve objects from Cordra !!')
            print(f' - response from Cordra: {response.text}')
            sys.exit(1)
        return response.json()['results']


    '''
    create: creates a new Cordra object
    '''
    def create(self, obj, type, full=False):
        full = '&full' if full else ''
        response = requests.post(f'{self.url}/objects/?type={type}{full}', json=obj, headers=self.headers)
        if response.status_code != 200:
            print('!! Error: Unable to create object in Cordra !!')
            print(f' - response from Cordra: {response.text}')
            sys.exit(1)
        return response.json()


    '''
    update: updates an existing Cordra object
    '''
    def update(self, pid, obj, full=False):
        full = '?full' if full else ''
        response = requests.put(f'{self.url}/objects/{pid}{full}', json=obj, headers=self.headers)
        if response.status_code != 200:
            print('!! Error: Unable to update object in Cordra !!')
            print(f' - response from Cordra: {response.text}')
            sys.exit(1)
        return response.json()


    '''
    delete: deletes an existing Cordra object
    '''
    def delete(self, pid):
        response = requests.delete(f'{self.url}/objects/{pid}', headers=self.headers)
        if response.status_code != 200:
            print('!! Error: Unable to delete object in Cordra !!')
            print(f' - response from Cordra: {response.text}')
            sys.exit(1)
        return response.json()


    '''
    get_acl: returns the ACL of a specific Cordra object
    '''
    def get_acl(self, pid):
        response = requests.get(f'{self.url}/acls/{pid}', headers=self.headers)
        if response.status_code != 200:
            print('!! Error: Unable to retrieve ACL from Cordra !!')
            print(f' - response from Cordra: {response.text}')
            sys.exit(1)
        return response.json()


    '''
    update_acl: updates the ACL of a specific Cordra object
    '''
    def update_acl(self, pid, acl):
        response = requests.put(f'{self.url}/acls/{pid}', json=acl, headers=self.headers)
        if response.status_code != 200:
            print('!! Error: Unable to update ACL in Cordra !!')
            print(f' - response from Cordra: {response.text}')
            sys.exit(1)
        return response.json()


if __name__ == '__main__':
    print('This is a module, not a script!')