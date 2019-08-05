import json
import warnings

from hash_encrypt import hash_encrypt

ACCOUNT_DATA_FILE = 'account.json'


def change_password(user_id, pwd):
    if pwd == '':
        warnings.warn('Empty password')
    hash_pwd = hash_encrypt(user_id, pwd)
    with open(ACCOUNT_DATA_FILE, 'r') as load_file:
        load_data = json.load(load_file)
    new_data = load_data.copy()
    new_data['data'][str(user_id)]['login']['LoginMethod']['password'] = hash_pwd
    with open(ACCOUNT_DATA_FILE, "w") as dump_file:
        json.dump(new_data, dump_file)


def authenticate(user_id, pwd):
    hash_pwd = hash_encrypt(user_id, pwd)
    with open(ACCOUNT_DATA_FILE, 'r') as load_file:
        load_data = json.load(load_file)
    try:
        if load_data['data'][str(user_id)]['login']['LoginMethod']['password'] == hash_pwd:
            return True
        else:
            return False
    except KeyError:
        return False


if __name__ == "__main__":
    pass
