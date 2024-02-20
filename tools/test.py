#!/usr/bin/env python3

import libutils
import libcordra
import libgithub
import libschema


''' main function '''
def main():
    # Read configuration
    config = libutils.get_config()

    # Initialize Cordra module
    cordra = libcordra.Cordra(
        config['cordra_url'], 
        config['cordra_user'], 
        config['cordra_pass']
    )

    # get an overview of the existing schemas in Cordra
    schemas = cordra.get_schemas()

    # retrieve versions of each stored schema
    for item in schemas.values():
        item['stored_versions'] = cordra.get_versions(item['pid'])

    print(schemas)


if __name__ == '__main__':
    main()