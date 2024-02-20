'''
This is a python module that provides a simple interface to the Cordra API.
It contains a single class, Cordra, which provides methods for accessing
and manipulating Cordra objects. The class contains the following methods:
    - search: returns a list of Cordra objects that match a specific query
    - get: returns the contents of a specific Cordra object
    - create: creates a new Cordra object
    - update: updates an existing Cordra object

    - list_versions: returns a list of versions of a specific Cordra object
    - create_version: creates a new version of an existing Cordra object
'''

import sys

import requests


class Cordra:
    def __init__(self, url, username, password):
        self.url = url
        self.username = username
        self.password = password
        self.auth = (username, password)

    '''
    search: returns a list of Cordra objects that match a specific query
    '''
    def search(self, query):
        response = requests.get('{}/objects?query={}'.format(self.url, query), auth=self.auth)
        if response.status_code != 200:
            print('Error: Unable to retrieve objects from Cordra')
            sys.exit(1)
        return response.json()


    '''
    get: returns the contents of a specific Cordra object
    '''
    def get(self, id):
        response = requests.get('{}/objects/{}'.format(self.url, id), auth=self.auth)
        if response.status_code != 200:
            print('Error: Unable to retrieve object from Cordra')
            sys.exit(1)
        return response.json()


    '''
    create: creates a new Cordra object
    '''
    def create(self, obj):
        response = requests.post('{}/objects'.format(self.url), json=obj, auth=self.auth)
        if response.status_code != 201:
            print('Error: Unable to create object in Cordra')
            sys.exit(1)
        return response.json()


    '''
    update: updates an existing Cordra object
    '''
    def update(self, id, obj):
        response = requests.put('{}/objects/{}'.format(self.url, id), json=obj, auth=self.auth)
        if response.status_code != 200:
            print('Error: Unable to update object in Cordra')
            sys.exit(1)
        return response.json()


    '''
    list_versions: returns a list of versions of a specific Cordra object
    '''
    def list_versions(self, id):
        response = requests.get('{}/objects/{}/versions'.format(self.url, id), auth=self.auth)
        if response.status_code != 200:
            print('Error: Unable to retrieve versions from Cordra')
            sys.exit(1)
        return response.json()


    '''
    create_version: creates a new version of an existing Cordra object
    '''
    def create_version(self, id, obj):
        response = requests.post('{}/objects/{}/versions'.format(self.url, id), json=obj, auth=self.auth)
        if response.status_code != 201:
            print('Error: Unable to create version in Cordra')
            sys.exit(1)
        return response.json()
