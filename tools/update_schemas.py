import os
import json

import libgithub
import libschema
import libcordra

config = {
    "cordra_url": "https://data.e-rihs.io",
    "cordra_user": "admin",
    "cordra_pass": None,
    "github_repo": "e-rihs/schema",
    "github_branch": "master"
}


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

        # update the schema in Cordra
        #cordra = libcordra.Cordra(config['cordra_url'], config['cordra_user'], config['cordra_pass'])
        #cordra.create_version(schema, schema_content)




if __name__ == '__main__':
    main()