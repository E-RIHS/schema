#!/usr/bin/env python3

import argparse

import requests

import libutils
import libcordra


schema_type = 'Technique'


''' main function '''
def main(delete=False, new_only=False, fake=False):
    # Read configuration
    config = libutils.get_config()

    # Initialize Cordra module
    cordra = libcordra.Cordra(
        config['cordra_url'], 
        config['cordra_user'], 
        config['cordra_pass']
    )

    # get list of existing schemas from Cordra and from the vocabulary
    print('Fetching the techniques in Cordra and in Opentheso/CL...')
    techniques_in_cordra = get_techniques_from_cordra(cordra)
    url = libutils.default_config['cl_techniques_full_url']
    techniques_in_vocabulary = get_techniques_from_vocabulary(url)

    # fail if no techniques are found in the vocabulary 
    # this is likely an error in the stack and could lead to deleting all techniques in Cordra!
    if len(techniques_in_vocabulary) == 0:
        print('!! Error: No techniques found in the vocabulary !!')
        exit(1)

    # compare the two lists
    print('Creating work lists...')
    cordra_set = set(techniques_in_cordra.keys())
    vocab_set = set(techniques_in_vocabulary.keys())
    to_create = vocab_set - cordra_set   # items in the vocabulary that are not in Cordra
    to_delete = cordra_set - vocab_set   # items in Cordra that are not in the vocabulary
    to_update = cordra_set & vocab_set   # items that are in both Cordra and the vocabulary
    print(f' - Techniques to create: {len(to_create)}')
    print(f' - Techniques to update: {len(to_update)} {"" if new_only else "(skipping)"}')
    print(f' - Techniques to delete: {len(to_delete)} {"" if delete else "(skipping)"}')

    # if fake, do not actually create/update/delete techniques
    if fake:
        print('Running in fake mode, no changes will be made...')
        exit(0)

    # create new techniques
    if len(to_create) > 0:
        print('Creating new techniques...')
        for id in to_create:
            obj = construct_object(id, techniques_in_vocabulary[id])
            print(f' - Creating "{obj["preferred_label"]}"...')
            response = cordra.create(obj=obj, type=schema_type)
            print(f'   Successfully created')

    # update existing techniques
    if len(to_update) > 0 and not new_only:
        print('Updating techniques...')
        for id in to_update:
            obj = update_object(techniques_in_cordra[id]["content"], techniques_in_vocabulary[id])
            print(f' - Updating "{obj["preferred_label"]}"...')
            response = cordra.update(pid=techniques_in_cordra[id]['id'], obj=obj)
            print(f'   Successfully updated')
    
    # delete techniques
    if len(to_delete) > 0 and delete:
        print('Deleting techniques...')
        for id in to_delete:
            print(f' - Deleting "{techniques_in_cordra[id]["content"]["preferred_label"]}"...')
            response = cordra.delete(pid=techniques_in_cordra[id]['id'])
            print(f'   Successfully deleted')


''' Get all techniques from Cordra '''
def get_techniques_from_cordra(cordra):
    print(' - Fetching all techniques from Cordra...')
    q = f'type:"{schema_type}"'
    list_of_objects =  cordra.query(q)
    dict_of_objects = {}
    for obj in list_of_objects:
        dict_of_objects[obj['content']['e-rihs_vocab_id']] = obj
    print(f"   Found techniques in Cordra: {len(dict_of_objects)}")
    return dict_of_objects


''' Get all techniques from the vocabulary '''
def get_techniques_from_vocabulary(cl_techniques_full_url):
    print(' - Getting all techniques from Opentheso/CL...')
    response = requests.get(cl_techniques_full_url)
    if response.status_code != 200:
        print('   !! Error: Unable to retrieve techniques from the vocabulary !!')
        print(f'   response from the CL script: {response.text}')
        exit(1)
    dict_of_techniques = response.json()
    print(f"   Found techniques in Opentheso: {len(dict_of_techniques['data'])}")
    return dict_of_techniques["data"]


''' build object for a technique '''
def construct_object(id, data):
    obj = {
        "preferred_label": data['prefLabel'],
        "definition": data['definition'],
        "alternative_labels": data['altLabel'],
        "e-rihs_vocab_id": id,
        "e-rihs_vocab_json_url": data['term_json_url']
    }
    if len(data['narrower']) > 0:
        obj["narrower"] = []
        for k, v in data['narrower'].items():
            obj["narrower"].append({"e-rihs_vocab_id": k, "preferred_label": v})
    if len(data['broader']) > 0:
        obj["broader"] = []
        for k, v in data['broader'].items():
            obj["broader"].append({"e-rihs_vocab_id": k, "preferred_label": v})
    return obj


''' update existing object for a technique '''
def update_object(existing_object, data):
    existing_object['preferred_label'] = data['prefLabel']
    existing_object['definition'] = data['definition']
    existing_object['alternative_labels'] = data['altLabel']
    existing_object['e-rihs_vocab_json_url'] = data['term_json_url']
    if len(data['narrower']) > 0:
        existing_object["narrower"] = []
        for k, v in data['narrower'].items():
            existing_object["narrower"].append({"e-rihs_vocab_id": k, "preferred_label": v})
    if len(data['broader']) > 0:
        existing_object["broader"] = []
        for k, v in data['broader'].items():
            existing_object["broader"].append({"e-rihs_vocab_id": k, "preferred_label": v})
    return existing_object


''' main entry point '''
if __name__ == '__main__':
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--new', dest='new', action='store_true', help='Only add new techniques (no updates)')
    parser.add_argument('-d', '--delete', dest='delete', action='store_true', help='Delete techniques that are not in the vocabulary')
    parser.add_argument('--fake', dest='fake', action='store_true', help='Do not actually create/update/delete techniques')
    args = parser.parse_args()

    main(delete=args.delete, new_only=args.new, fake=args.fake)