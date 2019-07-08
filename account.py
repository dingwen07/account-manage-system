import os
import hashlib
import json
import warnings
import getpass

ACCOUNT_DATA_FILE = 'account.json'


def init():
    salt_a_a = 'VZJ4KDICUHPCJEA7'
    salt_a_b = 'CRKJ6KZ34WK3SIB3'
    salt_b_a = 'TBJZJREKFRHABNMA'
    salt_b_b = 'SU3KANPTYEMPO462'
    default_admin_password = '41fd9bd52846bf40eb0ebca6a0ebfde174c439a10813e8aaa8df4bfb33d0b212df1f70f488006299a68d8ff47fe58b25960e0b27da640fd7cad5addece20b5d7'
    default_admin_yubikey = []

    new_data = {
        'config': {
            'login': {
                'GlobalLoginPolicy': {
                    'AllowPasswordLogin': True,
                    'RequireMultiFactor': False
                },
                'password': {
                    'salt': {
                        'salt_a_a': salt_a_a,
                        'salt_a_b': salt_a_b,
                        'salt_b_a': salt_b_a,
                        'salt_b_b': salt_b_b
                    }
                },
                'YubiKey': {
                    'API_KEY': {
                        'client_id': '<Client ID>',
                        'secret_key': '<Secret key>',
                    }
                }
            }
        },
        'data': {
            '0': {
                'name': 'Administrator',
                'login': {
                    'LoginMethod': {
                        'password': default_admin_password,
                        'YubiKey': default_admin_yubikey,
                        'TOTP': False,
                    },
                    'LoginPolicy': {
                        'MultiFactor': False
                    }
                }
            }
        }
    }
    with open(ACCOUNT_DATA_FILE, "w") as dump_file:
        json.dump(new_data, dump_file)

    with open(ACCOUNT_DATA_FILE, 'r') as load_file:
        load_data = json.load(load_file)
    print(load_data['config']['login']['password']['salt']['salt_a_a'])


def create_user(user_id, name, password):
    from hash_encrypt import hash_encrypt
    with open(ACCOUNT_DATA_FILE, 'r') as load_f:
        load_data = json.load(load_f)
    new_data = load_data
    new_data['data'][str(user_id)] = {
        'name': name,
        'login': {
            'LoginMethod': {
                'password': hash_encrypt(user_id, password)
            },
            'LoginPolicy': {
                'MultiFactor': False
            }
        }
    }
    with open(ACCOUNT_DATA_FILE, "w") as dump_f:
        json.dump(new_data, dump_f)


class Account(object):

    logged_in = False
    user_id = -1

    def __init__(self):
        pass


if __name__ == "__main__":
    init()
    create_user(1, 'TEST', getpass.getpass('Input Password for TEST'))
