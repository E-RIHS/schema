import sys
import os
import random
import string
import argparse

import libcordra
import libutils


ORCID_PID_TYPE = "https://hdl.handle.net/21.11158/0001-435g7fgxnl86qx92p8d3tdnhc"
RESEARCH_DISCIPLINES = ["https://hdl.handle.net/21.11158/0001-pr292qprrb6fj5gp48wv6xfxj"]   # = heritage science
ACL_WRITERS_INIT = ["21.11158/c9ce-5592-beb0-6240"] # = administrators group


# generate strong password (32 characters, upper, lower, digits, special)
def generate_password():
    password = ''.join(random.choice(string.ascii_letters + string.digits + string.punctuation) for i in range(24))
    return password


# read the request file and return the chosen line
def read_request(fn, line_number: int):
    print('Reading request file:', fn)
    # read and parse the line in the request file
    with open(fn, 'r') as file:
        for i, line in enumerate(file):
            if i + 1 == line_number:
                print(f'  - Line: {line}')
                parts = line.strip().split('\t')
                request = {
                    'ts': parts[0],
                    'first_name': parts[1].strip(),
                    'last_name': parts[2].strip(),
                    'email': parts[3].strip(),
                    'orcid': parts[4].strip(),
                    'organisation_name': parts[5].strip(),
                    'organisation_acronym': parts[6].strip(),
                    'country': parts[7].strip().lower(),
                }
    if request:
        # check if all fields (except ts) are not ''
        for key in request:
            if key != 'ts' and request[key] == '':
                print('!! Error: missing field in request:', key)
                sys.exit(1)
        # remove url part of orcid
        if request['orcid'].startswith('https://orcid.org/'):
            request['orcid'] = request['orcid'][18:]
        # replace country name with vocab handle
        countries = libutils.get_countries()
        country_pid = None
        for key, value in countries.items():
            if value == request['country']:
                country_pid = key
                break
        if country_pid: 
            request['country'] = country_pid
        else:
            # if not found, exit with error
            print('!! Error: country not found in vocab:', request['country'])
            sys.exit(1)
        return request
    else:
        return None


# create the CordraUser in Cordra
def create_cordra_user(cordra, request):
    print('Creating user:', request['email'])
    # check if the user already exists (by orcid)
    query = f'type:"CordraUser" AND /orcid:"{request["orcid"]}"'
    response = cordra.query(query)
    if len(response) == 1:
        print('!! Warning: a user with this orcid already exists')
        return response[0]['content']
    elif len(response) > 1:
        print('!! Error: multiple users with this orcid already exist')
        sys.exit(1)
    # create the CordraUser object
    cordra_user = {
        "username": request['email'],
        "password": generate_password(),
        "accountActive": True,
        "requirePasswordChange": False,
        "orcid": request['orcid']
    }
    print(cordra_user)
    # post the CordraUser object to Cordra
    user = cordra.create(
        obj=cordra_user,
        type='CordraUser'
    )
    print('  - User created:', user['id'])
    return user


# create the Organisation in Cordra
def create_cordra_organisation(cordra, request):
    print('Creating organisation:', request['organisation_name'])
    # check if the organisation already exists (by acronym)
    query = f'type:"Organisation" AND /acronym:"{request["organisation_acronym"]}"'
    response = cordra.query(query)
    if len(response) == 1:
        print('!! Warning: an organisation with this acronym already exists')
        # ask if we should use this organisation or create a new one (repeat until valid answer)
        while True:
            answer = input('  - Use this organisation or create new? (this/new/exit): ')
            if answer.lower().startswith('t'):
                print('  - using existing organisation:', response[0]['id'])
                return response[0]
            elif answer.lower().startswith('n'):
                print('  - creating new organisation')
                break
            elif answer.lower().startswith('e'):
                print('Exiting...')
                sys.exit(1)
    elif len(response) > 1:
        print('!! Error: multiple organisations with this acronym already exist')
        sys.exit(1)
    # create the Organisation object
    organisation = {
        "id": "",
        "acronym": request['organisation_acronym'],
        "name": request['organisation_name'],
        "research_disciplines": RESEARCH_DISCIPLINES
    }
    # post the Organisation object to Cordra
    org = cordra.create(
        obj=organisation,
        type='Organisation'
    )
    print(org)
    print('  - Organisation created:', org['id'])
    return org


# create the Person in Cordra
def create_cordra_person(cordra, request, organistion_id):
    print('Creating person:', request['first_name'], request['last_name'])
    # check if the person already exists (by orcid, by email, by full name, by organisation, by country)
    query = f'type:"Person" AND (/external_pids/_/pid:"{request["orcid"]}" OR /mbox="{request["email"]}" OR /full_name="{request["last_name"]}, {request["first_name"]}")'
    response = cordra.query(query)
    if len(response) == 1:
        print('!! Warning: an organisation with this acronym already exists')
        # ask if we should use this organisation or create a new one (repeat until valid answer)
        while True:
            answer = input('  - Use this organisation or create new? (this/new/exit): ')
            if answer.lower().startswith('t'):
                print('  - using existing organisation:', response[0]['id'])
                return response[0]
            elif answer.lower().startswith('n'):
                print('  - creating new organisation')
                break
            elif answer.lower().startswith('e'):
                print('Exiting...')
                sys.exit(1)
    elif len(response) > 1:
        print('!! Warning: multiple persons with this orcid already exist')
        i = 1
        for r in response:
            print(f'    ({i}) {r["content"]["full_name"]} - {r["content"]["mbox"]} ({r['id']})')
        while True:
            answer = input(f'  - Select person to use (1-{len(r)}/new/exit): ')
            if answer.isdigit() and 1 <= int(answer) <= len(r):
                print('  - using existing person:', response[int(answer)-1]['id'])
                return response[int(answer)-1]
            elif answer.lower().startswith('n'):
                print('  - creating new person')
                break
            elif answer.lower().startswith('e'):
                print('Exiting...')
                sys.exit(1)
    # create the Person object
    person = {
        "id": "",
        "first_name": request['first_name'],
        "last_name": request['last_name'],
        "external_pids": [
            {
                "pid_type": ORCID_PID_TYPE,
                "pid": f"https://orcid.org/{request['orcid']}"
            }
        ],
        "based_in": request['country'],
        "part_of_organisation": [
            {
                "organisation_pid": organistion_id
            }
        ],
        "mbox": request['email'],
        "research_disciplines": RESEARCH_DISCIPLINES
    }
    # post the Person object to Cordra
    person = cordra.create(
        obj=person,
        type='Person'
    )
    print('  - Person created:', person['id'])
    return person


# update acl writers list
def update_acl_writers(cordra, object_id, user_id, init=False):
    # get the current acl
    acl = cordra.get_acl(object_id)
    if init:
        acl['writers'] = ACL_WRITERS_INIT
    acl['writers'].append(user_id)
    cordra.update_acl(object_id, acl)


# create_all (main) function
def create_all(request, existing_person=None, existing_organisation=None):
    # Read configuration
    config = libutils.get_config()

    # initialize the cordra object
    cordra = libcordra.Cordra(
        config['cordra_url'], 
        config['cordra_user'], 
        config['cordra_pass']
    )

    # create the user in Cordra
    user = create_cordra_user(cordra, request)

    # create/update the organisation in Cordra
    if existing_organisation:
        organisation_id = existing_organisation
        # add the user to the organisation acl writers list
        update_acl_writers(
            cordra=cordra,
            object_id=organisation_id,
            user_id=user['id'],
            init=False)
    else:
        # create the organisation
        organisation = create_cordra_organisation(cordra, request)
        organisation_id = organisation['id']
        # create the acl writers list
        update_acl_writers(
            cordra=cordra,
            object_id=organisation_id,
            user_id=user['id'],
            init=True)

    # create/update the person in Cordra
    person = None
    if existing_person:
        person_id = existing_person
        # add user to the acl writers list
        update_acl_writers(
            cordra=cordra,
            object_id=person_id,
            user_id=user['id'],
            init=False)
    else:
        # create the person
        person = create_cordra_person(cordra, request, organisation_id)
        person_id = person['id']
        # create the acl writers list
        update_acl_writers(
            cordra=cordra,
            object_id=person_id,
            user_id=user['id'],
            init=True)

    # update the CordraUser with the linked person
    print('Updating user with linked person')
    user['linked_person'] = person_id
    cordra.update(user['id'], user)


if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', dest='fn', action='store', default="./requests.tsv", help='file with requests (default: ./requests.tsv)')
    parser.add_argument('-l', '--line', dest='line', action='store', type=int, default=1, help='line number to process (default: 1)')
    parser.add_argument('-p', '--person', dest='person', action='store', help='link to an existing person object (handle)')
    parser.add_argument('-o', '--organisation', dest='organisation', action='store', help='link to an existing organisation object (handle)')
    args = parser.parse_args()

    # check if file exists
    if not os.path.exists(args.fn):
        print('File not found:', args.fn)
        sys.exit(1)

    # read the request file and return the chosen line
    # print line and type of line
    request = read_request(args.fn, args.line)

    # call the main function
    create_all(request, args.person, args.organisation)
