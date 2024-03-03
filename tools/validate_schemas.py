#!/usr/bin/env python3

import libutils
import libgithub
import libschema


''' main function '''
def main():
    # Read configuration
    config = libutils.get_config()

    # get the list of schemas from the GitHub repository
    github = libgithub.GitHub(config['github_repo'])
    schemas = github.get_schemas()

    # loop over schemas, get the schema from GitHub and update it in Cordra
    print()
    for schema_url in schemas:
        # get the schema from GitHub
        schema_content = github.get_schema(schema_url)

        # print some debug information
        schema = schema_url.split('/')[-1]
        type = libschema.get_type(schema_content)
        name, version = libschema.extract_schema_details(schema_content)
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