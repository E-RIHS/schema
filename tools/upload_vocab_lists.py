#!/usr/bin/env python3

import os
import argparse
import json
import time

import requests

import libutils
import libcordra
import libschema


sleep_time = 1                              # time to sleep between requests
refresh_parameter = "urlappend=%26refresh"  # parameter to force refresh of the vocab list


''' main function '''
def main(schema_names, use_github=False, use_cached=False, auth=False, force=False):
    # Read configuration
    config = libutils.get_config()

    # Initialize Cordra module
    cordra = libcordra.Cordra(
        config['cordra_url'], 
        config['cordra_user'], 
        config['cordra_pass']
    )

    # loop over the schema names
    for schema_name in schema_names:
        # read the schema
        if not use_github:
            schema = read_schema_from_local(schema_names)
        else:
            print('Using GitHub repository for schema definitions is not yet implemented')
            exit(1)

        # check if the schema already exists in Cordra
        cordra_schemas = cordra.get_schemas()
        if schema['title'] not in cordra_schemas:
            print(f'Schema "{schema["name"]}" does not exist yet in Cordra, skipping')
            exit(1)
        schema_pid = cordra_schemas[schema['title']]['pid']
        
        # expand the schema with controlled or example lists
        schema = expand(schema, use_cached, auth, force)

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


''' expand the schema with vocab lists '''
def expand(schema, use_cached=False, auth=False, force=False):
    print('Expanding schema with vocab lists')
    # loop over the schema definitions section
    for d in schema['definitions']:
        print(f' - Processing definition "{d}"...')
        # check if the definition is a controlled or examples list
        if 'e-rihs' in schema['definitions'][d]:
            if 'enum_source' in schema['definitions'][d]['e-rihs'] and "examples_source" in schema['definitions'][d]['e-rihs']:
                print('   !! Both "enum_source" and "examples_source" found in definition, ABORTING... !!')
                exit(1)
            elif 'enum_source' in schema['definitions'][d]['e-rihs']:
                # fetch the controlled list from the url
                print(f'   Fetching controlled list from {url}')
                url = schema['definitions'][d]['e-rihs']['enum_source']
                url = build_fetch_url(url, use_cached, auth)
                terms, labels = fetch_vocab_list(url, response_format='default')
                if len(terms) == 0 and not force:
                    print('   !! Controlled list is empty, ABORTING... !!')
                    exit(1)
                # add the terms and labels to the schema
                print(f'   Adding {len(terms)} terms to the schema')
                schema['definitions'][d]['enum'] = terms
                if 'options' not in schema['definitions'][d]:
                    schema['definitions'][d]['options'] = {}
                schema['definitions'][d]['options']['enum_titles'] = labels
            elif "examples_source" in schema['definitions'][d]['e-rihs']:
                # fetch the examples list from the url
                print(f'   Fetching examples list from {url}')
                url = schema['definitions'][d]['e-rihs']['examples_source']
                url = build_fetch_url(url, use_cached, auth)
                terms = fetch_vocab_list(url, response_format='simple')
                if len(terms) == 0 and not force:
                    print('   !! Examples list is empty, ABORTING... !!')
                    exit(1)
                # add the terms to the schema
                print(f'   Adding {len(terms)} examples to the schema')
                schema['definitions'][d]['examples'] = terms    # the JSON Schema compliant way
                if 'type' not in schema['definitions'][d]['cordra']:
                    schema['definitions'][d]['cordra']['type'] = {}
                schema['definitions'][d]['cordra']['type']['suggestedVocabulary'] = terms   # the Cordra way
            else:
                print('   No "enum_source" or "examples_source" found in definition, skipping')
        else:
            print('   No "enum_source" or "examples_source" found in definition, skipping')
        if sleep_time > 0:
            time.sleep(sleep_time)
    return schema


def build_fetch_url(url, use_cached, auth):
    # check if the url is a handle
    is_handle = 'hdl.handle.net' in url
    # look for existing urlappend parameter
    if is_handle:
        params = []
        # decompose the url
        base_url, urlappend = url.split('?urlappend=')
        urlappend = urlappend.split('%26')
        # remove empty strings from urlappend
        urlappend = [x for x in urlappend if x]
        # add the refresh parameter if not use_cached
        if not use_cached and 'refresh' not in urlappend:
            urlappend.append('refresh')
        # recompose the urlappend
        urlappend = list(set(urlappend))
        if len(urlappend) > 0:
            params.append("urlappend=%26" + "%26".join(urlappend))
        # add the auth parameter if auth
        if auth:
            params.append('auth')
        # recompose the url
        url = base_url + "?" + "&".join(params)
    return url


def fetch_vocab_list(enum_source, response_format='default'):
    response = requests.get(enum_source)
    if response.status_code != 200:
        print(f'Error: Unable to retrieve vocab list from {enum_source}')
        exit(1)
    response = response.json()
    if response_format == 'default':
        if 'list' in response and len(response['list']) > 0:
            response = response['list']
            # response['list'] is dict: terms are keys, labels are values
            terms = list(response.keys())
            labels = list(response.values())
            return terms, labels
        else:
            return [], []
    elif response_format == 'simple':
        #response is a simple list of terms
        return response
    else:
        print(f'!! Error: Unknown response format "{response_format}"')
        exit(1)


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
    parser.add_argument('-s', '--schema', dest='schema', nargs='*', action='store', help='schema(s) to be processed (space separated)')
    parser.add_argument('-c', '--cached', dest='use_cached', action='store_true', help="Use the cached vocab list (no refresh)")
    parser.add_argument('--auth', dest='auth', action='store_true', help='Bypass Handle proxy cache')
    parser.add_argument('--allow_empty', dest='force', action='store_true', help='Allow empty vocab lists')
    args = parser.parse_args()

    if args.github:
        print('Using GitHub repository for schema definitions is not yet implemented')
        exit(1)

    main(
        schema_names=args.schema, 
        use_github=args.github, 
        use_cached=args.use_cached, 
        auth=args.auth, 
        force=args.force
    )