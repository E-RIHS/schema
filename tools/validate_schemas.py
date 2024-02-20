#!/usr/bin/env python3

import os
import json

import libutils
import libgithub
import libschema


config = libutils.default_config


''' read and update configuration from config.json'''
def get_config():
    if os.path.isfile('config.json'):
        with open('config.json', 'r') as f:
            # update config with the values from config.json
            config.update(json.load(f))
    return config


''' main function '''
def main():
    # Read configuration
    config = get_config()

    # get the list of schemas from the GitHub repository
    github = libgithub.GitHub(config['github_repo'])
    schemas = github.get_schemas()

    # loop over schemas, get the schema from GitHub and update it in Cordra
    for schema_url in schemas:
        # get the schema from GitHub
        schema_content = github.get_schema(schema_url)

        # print some debug information
        schema = schema_url.split('/')[-1]
        type = libschema.get_type(schema_content)
        version = libschema.get_version(schema_content)
        draft = libschema.get_draft(schema_content)
        valid = libschema.validate(schema_content, draft)

        print('Schema:', schema)
        print('Type:', type)
        print('Version:', version)
        print('Draft:', draft)
        print('Valid:', valid)
        print()


if __name__ == '__main__':
    main()