# https://yubico-client.readthedocs.io/en/latest/
# pip install yubico-client
import json
from yubico_client import Yubico

ACCOUNT_DATA_FILE = 'account.json'

try:
    with open(ACCOUNT_DATA_FILE, 'r') as load_file:
        load_data = json.load(load_file)
        client_id = load_data['config']['login']['YubiKey']['API_KEY']['client_id']
        secret_key = load_data['config']['login']['YubiKey']['API_KEY']['secret_key']
except:
    pass

def __get_identity(otp_code):
    return otp_code[0:12]


def __auth(public_identity, otp_code):
    otp_auth = False
    err_code = ''
    try:
        if otp_code[0:12] == public_identity:
            otp_auth = client.verify(otp_code)
        else:
            err_code = 'INVALID_ID'
    except Exception as e:
        err_code = e.args[0]
    finally:
        return otp_auth, err_code


def add_yubikey(user_id, otp_code):
    public_identity = __get_identity(otp_code)
    with open(ACCOUNT_DATA_FILE, 'r') as load_file:
        load_data = json.load(load_file)
    try:
        yubikeys = load_data['data'][str(user_id)]['login']['LoginMethod']['YubiKey']
    except KeyError:
        return 1
    if public_identity in yubikeys:
        return 2
    else:
        if __auth(public_identity, otp_code)[0]:
            yubikeys.append(public_identity)
            new_data = load_data.copy()
            new_data['data'][str(user_id)]['login']['LoginMethod']['YubiKey'] = yubikeys
            with open(ACCOUNT_DATA_FILE, "w") as dump_file:
                json.dump(new_data, dump_file)
            return 0
        else:
            return 3


def remove_yubikey(user_id, otp_code):
    public_identity = __get_identity(otp_code)
    with open(ACCOUNT_DATA_FILE, 'r') as load_file:
        load_data = json.load(load_file)
    try:
        yubikeys = load_data['data'][str(user_id)]['login']['LoginMethod']['YubiKey']
    except KeyError:
        return 1
    if public_identity in yubikeys:
        yubikeys.remove(public_identity)
        new_data = load_data.copy()
        new_data['data'][str(user_id)]['login']['LoginMethod']['YubiKey'] = yubikeys
        with open(ACCOUNT_DATA_FILE, "w") as dump_file:
            json.dump(new_data, dump_file)
        return 0
    else:
        return 2


def authenticate(user_id, otp_code):
    public_identity = __get_identity(otp_code)
    with open(ACCOUNT_DATA_FILE, 'r') as load_file:
        load_data = json.load(load_file)
    try:
        yubikeys = load_data['data'][str(user_id)]['login']['LoginMethod']['YubiKey']
    except KeyError:
        return False
    if public_identity in yubikeys:
        return __auth(public_identity, otp_code)[0]
    else:
        return False
