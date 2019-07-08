import json
import warnings

from hash_encrypt import hash_encrypt

ACCOUNT_DATA_FILE = 'account.json'


def set_password(user_id, password):
    pwd = password
    if pwd == '':
        warnings.warn('Empty password')
    hash_pwd = hash_encrypt(user_id, pwd)
    with open(ACCOUNT_DATA_FILE, 'r') as load_f:
        load_data = json.load(load_f)
    new_data = load_data.copy()
    new_data['data'][str(user_id)] = {
        'login': {
            'LoginMethod': {
                'password': hash_pwd
            }
        }
    }
    with open(ACCOUNT_DATA_FILE, "w") as dump_f:
        json.dump(new_data, dump_f)


def authenticate_password(user_id, password):
    pwd = password
    hash_pwd = hash_encrypt(user_id, pwd)
    with open(ACCOUNT_DATA_FILE, 'r') as load_f:
        load_data = json.load(load_f)
    try:
        if load_data['data'][str(user_id)]['login']['LoginMethod']['password'] == hash_pwd:
            return True
        else:
            return False
    except KeyError:
        # print('RuntimeError: Unable to locate user')
        return False


if __name__ == "__main__":
    pass
