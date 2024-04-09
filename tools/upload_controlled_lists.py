#!/usr/bin/env python3

import os
import argparse
import json

import requests

import libutils
import libcordra
#import libgithub
import libschema


''' main function '''
def main(schema_name, use_github=False, use_cached=False):
    # Read configuration
    config = libutils.get_config()

    # Initialize Cordra module
    cordra = libcordra.Cordra(
        config['cordra_url'], 
        config['cordra_user'], 
        config['cordra_pass']
    )

    # read the schema
    if not use_github:
        schema = read_schema_from_local(schema_name)
    else:
        print('Using GitHub repository for schema definitions is not yet implemented')
        exit(1)

    # check if the schema already exists in Cordra
    cordra_schemas = cordra.get_schemas()
    if schema['title'] not in cordra_schemas:
        print(f'Schema "{schema["name"]}" does not exist yet in Cordra, skipping')
        exit(1)
    schema_pid = cordra_schemas[schema['title']]['pid']
    
    # expand the schema with controlled lists
    schema = expand(schema, use_cached)

    # build the digital object
    do = build_digital_object(schema_name, schema)

    # update the schema in Cordra
    print(f'Updating schema "{schema_pid}" in Cordra')
    response = cordra.update(pid=schema_pid, obj=do, full=False)
    print(' - Schema updated successfully')


''' read the schema '''
def read_schema_from_local(schema):
    # read the schema file
    schema_fname = f'../{schema}.schema.json'
    print(f'Reading schema from "{schema_fname}"...')
    if os.path.isfile(schema_fname):
        with open(schema_fname, 'r') as file:
            schema_content = file.read()
        print(f' - Schema file read successfully')
        return json.loads(schema_content)
    else:
        print(f' - !! Schema file not found !!')
        exit(1)


''' expand the schema with controlled lists '''
def expand(schema, use_cached=False):
    print('Expanding schema with controlled lists')
    # loop over the schema definitions section
    for d in schema['definitions']:
        print(f' - Processing definition "{d}"...')
        # check if the definition is a controlled list
        if 'e-rihs' in schema['definitions'][d]:
            if 'enum_source' in schema['definitions'][d]['e-rihs']:
                enum_source = schema['definitions'][d]['e-rihs']['enum_source']
                if not use_cached:
                    enum_source += "&refresh"
                # fetch the controlled list from the url
                print(f'   Fetching controlled list from {enum_source}')
                terms, labels = fetch_controlled_list(enum_source)
                # add the terms and labels to the schema
                print(f'   Adding {len(terms)} terms to the schema')
                schema['definitions'][d]['enum'] = terms
                if 'options' not in schema['definitions'][d]:
                    schema['definitions'][d]['options'] = {}
                schema['definitions'][d]['options']['enum_titles'] = labels
            else:
                print('   No "enum_source" found in definition, skipping')
        else:
            print('   No "enum_source" found in definition, skipping')
    return schema


def fetch_controlled_list(enum_source):
    response = requests.get(enum_source)
    if response.status_code != 200:
        print(f'Error: Unable to retrieve controlled list from {enum_source}')
        exit(1)
    cl = response.json()
    if 'list' in cl and len(cl['list']) > 0:
        cl = cl['list']
        # cl['list'] is dict: terms are keys, labels are values
        terms = list(cl.keys())
        labels = list(cl.values())
        return terms, labels
    else:
        return [], []


def build_digital_object(schema_id, schema):
    # get schema name
    name, version = libschema.extract_schema_details(schema_id)
    print(f'Building digital object "{name}"')
    # get the .do.json from the local file system and read it into a dictionary
    do_fname = f'../cordra/{name}.do.json'
    if os.path.isfile(do_fname):
        with open(do_fname, 'r') as file:
            do_content = file.read()
        print(f' - Reading {do_fname}')
        do = json.loads(do_content)
    else:
        print(f' !! Digital object for {name} not found !!')
        exit(1)
    # paste in the new schema
    print(f' - Adding expanded schema to digital object')
    do['schema'] = schema
    # get the .do.json from the local file system and read it into a dictionary
    js_fname = f'../cordra/{name}.do.js'
    if os.path.isfile(js_fname):
        with open(js_fname, 'r') as file:
            js_content = file.read()
        print(f' - Adding javascript from {js_fname}')
        do['javascript'] = js_content
    return do


if __name__ == '__main__':
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-g', '--github', dest='github', action='store_true', help='Use remote GitHub repository for schema definitions')
    parser.add_argument('-s', '--schema', dest='schema', action='store', default="controlled_lists-v1.0", help='Schema with controlled lists that should be updated')
    parser.add_argument('-c', '--cached', dest='use_cached', action='store_true', help="Use the cached controlled list (no refresh)")
    args = parser.parse_args()

    if args.github:
        print('Using GitHub repository for schema definitions is not yet implemented')
        exit(1)

    main(schema_name=args.schema, use_github=args.github, use_cached=args.use_cached)