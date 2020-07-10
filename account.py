import os
import json
import warnings
import getpass

from hash_encrypt import hash_encrypt
import authenticate
import password

ACCOUNT_DATA_FILE = 'account.json'


def init(default_admin_password: str):
    salt_a_a = 'VZJ4KDICUHPCJEA7'
    salt_a_b = 'CRKJ6KZ34WK3SIB3'
    salt_b_a = 'TBJZJREKFRHABNMA'
    salt_b_b = 'SU3KANPTYEMPO462'
    default_admin_yubikey = []

    new_data = {
        'config': {
            'login': {
                'GlobalLoginPolicy': [('password', 'requisite'), ('YubiKey', 'optional'), ('TOTP', 'optional')],
                'LoginMethod': {
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
            'NextUserID': 1
        },
        'data': {
            '0': {
                'username': 'Administrator',
                'login': {
                    'LoginMethod': {
                        'password': '41fd9bd52846bf40eb0ebca6a0ebfde174c439a10813e8aaa8df4bfb33d0b212df1f70f488006299a68d8ff47fe58b25960e0b27da640fd7cad5addece20b5d7',
                        'YubiKey': default_admin_yubikey,
                        'TOTP': None,
                    },
                    'LoginPolicy': [('password', 'requisite'), ('YubiKey', 'optional'), ('TOTP', 'optional')]
                },
                'status': [0, None, None]
            }
        }
    }
    with open(ACCOUNT_DATA_FILE, "w") as dump_file:
        json.dump(new_data, dump_file)

    with open(ACCOUNT_DATA_FILE, 'r') as load_file:
        load_data = json.load(load_file)
    print(load_data['data']['0']['username'])
    password.change_password(0, default_admin_password)


def create_user(username: str, pwd: str) -> int:
    if get_user_id(username) != -1:
        return -2
    with open(ACCOUNT_DATA_FILE, 'r') as load_file:
        load_data = json.load(load_file)
    user_id = load_data['config']['NextUserID']
    method_policy = load_data['config']['login']['GlobalLoginPolicy']
    new_data = load_data
    new_data['data'][str(user_id)] = {
        'username': username,
        'login': {
            'LoginMethod': {
                'password': None,
                'YubiKey': [],
                'TOTP': None
            },
            'LoginPolicy': method_policy
        },
        'status': [0, None, None]
    }
    new_data['config']['NextUserID'] = user_id + 1
    with open(ACCOUNT_DATA_FILE, "w") as dump_file:
        json.dump(new_data, dump_file)
    password.change_password(user_id, pwd)
    return (user_id)


def get_user_id(username: str) -> int:
    with open(ACCOUNT_DATA_FILE, 'r') as load_file:
        load_data = json.load(load_file)
    account_data = load_data['data']
    for user_id, user_data in account_data.items():
        if user_data['username'] == username:
            return int(user_id)
    return -1


class Account(object):

    logged_in = False
    user_id = -1
    login_codes = []

    def __init__(self, user_id):
        self.user_id = user_id

    def login(self):
        if self.logged_in:
            return True
        else:
            with open(ACCOUNT_DATA_FILE, 'r') as load_file:
                load_data = json.load(load_file)
            if len(self.login_codes) >= len(load_data['data'][str(self.user_id)]['login']['LoginPolicy']):
                for method in load_data['data'][str(self.user_id)]['login']['LoginPolicy']:
                    if method[0] == 'password':
                        authenticator = authenticate.PasswordAuthenticator(self.user_id)
                    elif method[0] == 'YubiKey':
                        authenticator = authenticate.YubiKeyAuthenticator(self.user_id)
                    else:
                        authenticator = authenticate.FalseAuthenticator()
                    if authenticator.authenticate(self.login_codes.pop(0)):
                        if method[1] == 'sufficient':
                            self.logged_in = True
                            return True
                    else:
                        if method[1] == 'required' or method[1] == 'requisite':
                            return False
                self.logged_in = True
                return True
            else:
                return False


if __name__ == "__main__":
    '''
    init('admin')
    pwd = getpass.getpass('Enter new password:')
    if getpass.getpass('Retype new password:') == pwd:
        password.change_password(0, pwd)
    else:
        print('Sorry, passwords do not match')

    print()
    print('TEST')
    pwd = getpass.getpass('Enter new password:')
    if getpass.getpass('Retype new password:') == pwd:
        print(create_user('TEST', pwd))
    else:
        print('Sorry, passwords do not match')

    print(get_user_id('TEST'))
    '''
    from account import Account
    a = Account(0)
    a.login_codes = ['admin', 'cccccciittvfveinbfunfnteijjevkehntltngjbdrle', 'sssss']
    a.login()
    print(a.logged_in)

