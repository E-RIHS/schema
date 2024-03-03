#!/usr/bin/env python3

import os
import argparse
import json

import requests

import libutils
import libcordra
import libgithub
import libschema


''' main function '''
def main(cl_schema, use_github=False):
    # Read configuration
    config = libutils.get_config()

    # Initialize Cordra module
    cordra = libcordra.Cordra(
        config['cordra_url'], 
        config['cordra_user'], 
        config['cordra_pass']
    )

    # read the schema
    schema = read_schema(cl_schema, use_github)

    # check if the schema already exists in Cordra
    cordra_schemas = cordra.get_schemas()
    if schema['title'] not in cordra_schemas:
        print(f'Schema "{schema["name"]}" does not exist yet in Cordra, skipping')
        exit(1)
    schema_pid = cordra_schemas[schema['title']]['pid']
    
    # expand the schema with controlled lists
    schema = expand(schema)

    # write the schema to a file
    fname = 'cl.json'
    with open(fname, 'w') as file:
        file.write(json.dumps(schema, indent=4))

    # update the schema in Cordra
    response = cordra.update(pid=schema_pid, obj=schema, full=False)


''' read the schema '''
def read_schema(cl_schema, use_github=False):
    if use_github:
        print('Using GitHub repository for schema definitions is not yet implemented')
        exit(1)

    # read the schema file
    schema_fname = f'../{cl_schema}'
    if os.path.isfile(schema_fname):
        with open(schema_fname, 'r') as file:
            schema_content = file.read()
        return json.loads(schema_content)
    else:
        print(f'Schema "{schema_fname}" not found')
        exit(1)


''' expand the schema with controlled lists '''
def expand(schema):
    # loop over the schema definitions section
    for d in schema['definitions']:
        # check if the definition is a controlled list
        if 'e-rihs' in schema['definitions'][d]:
            if 'enum_source' in schema['definitions'][d]['e-rihs']:
                enum_source = schema['definitions'][d]['e-rihs']['enum_source']
                # fetch the controlled list from the url
                terms, labels = fetch_controlled_list(enum_source)
                # add the terms and labels to the schema
                schema['definitions'][d]['enum'] = terms
                if 'options' not in schema['definitions'][d]:
                    schema['definitions'][d]['options'] = {}
                schema['definitions'][d]['options']['enum_titles'] = labels
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


if __name__ == '__main__':
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--github', dest='github', action='store_true', help='use remote GitHub repository for schema definitions')
    parser.add_argument('--cl_schema', dest='cl_schema', action='store', default="controlled_lists-v1.0.schema.json", help='Schema with controlled lists that should be updated')
    args = parser.parse_args()

    if args.github:
        print('Using GitHub repository for schema definitions is not yet implemented')
        exit(1)

    main(cl_schema=args.cl_schema, use_github=args.github)