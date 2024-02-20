#!/usr/bin/env python3

'''
This is a python module that provides some tools to work with JSON Schema.
It provides the following methods:
    - validate: validates a JSON object against a JSON Schema
    - get_type: returns the type of a JSON Schema
    - get_version: returns the version of a JSON Schema
    - get_draft: returns the draft version of a JSON Schema
'''

import sys

import requests
import jsonschema


'''
get_draft: returns the draft version of a JSON Schema
'''
def get_draft(schema):
    return schema.get('$schema')


'''
validate: validates a JSON object against a JSON Schema
'''
def validate(schema, draft):
    # download the draft from the web
    draft_content = requests.get(draft)
    if draft_content.status_code != 200:
        print('Error: Unable to retrieve draft from web')
        sys.exit(1)
    draft = draft_content.json()
    # validate the object against the schema
    try:
        jsonschema.validate(schema, draft)
    except jsonschema.exceptions.ValidationError as e:
        print(e)
        return False
    return True


'''
get_type: returns the type of a JSON Schema
'''
def get_type(schema):
    return schema.get('title')


'''
get_version: returns the version of a JSON Schema
'''
def get_version(schema):
    id = schema.get('$id')
    try:
        version = id.split('/')[-1].split('-')[-1].replace('v', '').replace('.schema.json', '')
    except:
        print('Error: {id} -> Unable to retrieve version from schema')
        sys.exit(1)
    return version


if __name__ == '__main__':
    print('This is a module, not a script!')