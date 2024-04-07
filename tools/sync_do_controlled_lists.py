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
    pass


if __name__ == '__main__':
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-g', '--github', dest='github', action='store_true', help='Use remote GitHub repository for schema definitions')
    parser.add_argument('-s', '--schema', dest='schema', action='store', help='Schema with controlled lists that should be updated')
    parser.add_argument('-c', '--cached', dest='use_cached', action='store_true', help="Use the cached controlled list (no refresh)")
    args = parser.parse_args()

    if args.github:
        print('Using GitHub repository for schema definitions is not yet implemented')
        exit(1)

    main(schema_name=args.schema, use_github=args.github, use_cached=args.use_cached)