
import random
import string

import libcordra
import libutils


# CordraUser

cordra_user = {
    "type": "CordraUser",
    "content": {
        "username": "",             # e-mail
        "linked_person": None,
        "password": "",             # generate
        "accountActive": True,
        "orcid": ""                 # only the number
    }
}

# Organisation

organisation = {
    "type": "Organisation",
    "content": {
        "acronym": "",            # acronym
        "name": "",               # full name
        "mbox": "",               # e-mail, optional?
        "research_disciplines": [
            "https://hdl.handle.net/21.11158/0001-pr292qprrb6fj5gp48wv6xfxj"
        ]
    }
}

# Person

person = {
    "type": "Person",
    "content": {
        "first_name": "",           # first name
        "last_name": "Padfield",    # last name
        "external_pids": [
            {
                "pid_type": "https://hdl.handle.net/21.11158/0001-435g7fgxnl86qx92p8d3tdnhc",   # = ORCID
                "pid": ""                                                                       # ORCID number (with https://orcid.org/ prefix)
            }
        ],
        "based_in": "",             # country handle from vocab
        "part_of_organisation": [
            {
                "organisation_pid": "",  # organisation PID, which we just created (or linked)
            }
        ],
        "mbox": "",                 # e-mail
        "research_disciplines": [
            "https://hdl.handle.net/21.11158/0001-pr292qprrb6fj5gp48wv6xfxj"    # = heritage science
        ]
    }
}


# create strong password (32 characters, upper, lower, digits, special)
def create_password():
    password = ''.join(random.choice(string.ascii_letters + string.digits + string.punctuation) for i in range(32))
    return password


# Read configuration
config = libutils.get_config()


# get the details
print('Enter the following details:')
cordra_user['content']['username'] = input('E-mail: ')
cordra_user['content']['password'] = create_password()
cordra_user['content']['orcid'] = input('ORCID: ')



# initialize the cordra object
cordra = libcordra.Cordra(
    config['cordra_url'], 
    config['cordra_user'], 
    config['cordra_pass']
)




# create the cordraUser object
#cordra_user['content']['username'] = "
