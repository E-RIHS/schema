#!/usr/bin/env python3

import argparse
import os
import json

import libutils
import libgithub
import libschema


''' main function '''
def main(use_github=False, override_draft=None):
    # Read configuration
    config = libutils.get_config()

    # create a GitHub object
    github = libgithub.GitHub(config['github_repo'])

    # get the list of schemas
    if use_github:
        print('Using GitHub repository:', config['github_repo'])
        schemas = get_schemas_from_github(github)
    else:
        print('Using local schema definitions')
        schemas = get_schemas_from_local()

    # print the draft version override
    if override_draft is not None:
        print('Overriding draft version with:', override_draft)

    # loop over schemas, load the schema
    for schema_path in schemas:
        if use_github:
            schema_content = github.get_schema(schema_path)
        else:
            with open('../' + schema_path, 'r') as file:
                schema_content = file.read()

        # convert the schema JSON string to dict
            schema_content = json.loads(schema_content)

        # get the draft version
        if override_draft is None:
            draft = libschema.get_draft(schema_content)
        else:
            draft = override_draft

        # get the schema type, name and version
        schema = schema_path.split('/')[-1]
        type = libschema.get_type(schema_content)
        name, version = libschema.extract_schema_details(schema)

        # validate the schema
        valid = libschema.validate(schema_content, draft)

        print(' - Schema:', schema)
        print('   Type:', type)
        print('   Version:', version)
        print('   Draft:', draft)
        print('   Valid:', valid)
    
    print()


''' get the list of schemas from the GitHub repository '''
def get_schemas_from_github(github):
    schemas = github.get_schemas()
    return schemas


''' get the list of schemas from the local file system '''
def get_schemas_from_local():
    # find all .schema.json files in the the above directory
    schemas = []
    for file in os.listdir('..'):
        if file.endswith('.schema.json'):
            schemas.append(file)
    return schemas


if __name__ == '__main__':
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-g', '--github', dest='github', action='store_true', help='use remote GitHub repository for schema definitions')
    parser.add_argument('-d', '--draft', dest='draft', action='store', help='override draft version for schema validation (full url)')
    args = parser.parse_args()

    main(use_github=args.github, override_draft=args.draft)