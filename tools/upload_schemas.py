#!/usr/bin/env python3

import os
import argparse
import json

import libutils
import libcordra
import libgithub
import libschema


''' main function '''
def main(schemas, use_github=False, update=False):
    # Read configuration
    config = libutils.get_config()

    # Initialize Cordra module
    cordra = libcordra.Cordra(
        config['cordra_url'], 
        config['cordra_user'], 
        config['cordra_pass']
    )

    # get list of existing schemas from Cordra
    cordra_schemas = cordra.get_schemas()

    # loop over schemas
    for schema_string in schemas:
        # extract schema name and optional version
        schema_name, schema_version = libschema.extract_schema_details(schema_string)
        print(f'Processing schema "{schema_name}" (version "{schema_version}")...')
        # compose the full schema digital object
        schema_do = compose_schema_digital_object(schema_name, schema_version, use_github)
        # check if the schema digital object already exists in Cordra
        if schema_do['name'] not in cordra_schemas:
            # create the schema digital object in Cordra
            response = cordra.create(obj=schema_do, type='Schema', full=True)
            print(f'Created schema "{response["content"]["name"]}" with handle {response["id"]}')
        else:
            # update the schema digital object in Cordra
            if update:
                pid = cordra_schemas[schema_do['name']]['pid']
                response = cordra.update(pid=pid, obj=schema_do, full=True)
                print(f'Updated schema "{response["content"]["name"]}" with handle {response["id"]}')
            else:
                print(f'Schema "{schema_name}" already exists in Cordra, skipping')
                continue
        # just a newline for better output formatting
        print()


''' compose the full schema digital object '''
def compose_schema_digital_object(schema_name, schema_version, use_github=False):
    if use_github:
        print('Using GitHub repository for schema definitions is not yet implemented')
        exit(1)

    # get the .do.json from the local file system and read it into a dictionary
    do_fname = f'../cordra/{schema_name}.do.json'
    if os.path.isfile(do_fname):
        with open(do_fname, 'r') as file:
            do_content = file.read()
        print(f'Found {do_fname}')
        do_dict = json.loads(do_content)
    else:
        print(f'Digital object for {schema_name} not found')
        exit(1)
    
    # get the .schema.json from the local file system and read it into a dictionary
    if schema_version is None:
        schema_version = '1.0'
    schema_fname = f'../{schema_name}-v{schema_version}.schema.json'
    if os.path.isfile(schema_fname):
        with open(schema_fname, 'r') as file:
            schema_content = file.read()
        print(f'Found {schema_fname}')
        do_dict['schema'] = json.loads(schema_content)
    
    # get the .do.js from the local file system and read it into a string
    js_fname = f'../cordra/{schema_name}.do.js'
    if os.path.isfile(js_fname):
        with open(js_fname, 'r') as file:
            do_js = file.read()
        print(f'Found {js_fname}')
        do_dict['javascript'] = do_js

    return do_dict


if __name__ == '__main__':
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-g', '--github', dest='github', action='store_true', help='use remote GitHub repository for schema definitions')
    parser.add_argument('-u', '--update', dest='update', action='store_true', help='update schema definitions in Cordra it they already exist')
    parser.add_argument('-s', '--schema', nargs='*', action='store', help='schema(s) to be processed')
    args = parser.parse_args()

    if args.github:
        print('Using GitHub repository for schema definitions is not yet implemented')
        exit(1)

    if len(args.schema) == 0:
        print('No schema(s) specified')
        exit(1)

    main(schemas=args.schema, use_github=args.github, update=args.update)