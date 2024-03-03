#!/usr/bin/env python3

'''
This is a python module that provides some tools to work with JSON Schema.
It provides the following methods:
    - validate: validates a JSON object against a JSON Schema
    - get_type: returns the type of a JSON Schema
    - extract_schema_details: extracts and returns schema name and optional version
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
def validate(schema, draft=None):
    # if draft is not provided, get it from the schema
    if draft is None:
        draft = get_draft(schema)
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
extract schema name and optional version
'''
def extract_schema_details(schema):
    schema = schema.lower()   # convert to lower case
    schema = schema.strip()   # remove leading and trailing whitespaces
    # remove extensions ('.schema.json' or '.do.json')
    schema = schema.replace('.schema.json', '')
    schema = schema.replace('.do.json', '')
    # split schema string into name and version (on last '-v')
    if '-v' not in schema:
        return schema, None
    else: 
        name, version = schema.rsplit('-v', 1)
        return name, version


if __name__ == '__main__':
    print('This is a module, not a script!')