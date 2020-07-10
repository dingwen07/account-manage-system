import hashlib
import json

ACCOUNT_DATA_FILE = 'account.json'


def hash_encrypt(user_id, password):
    with open(ACCOUNT_DATA_FILE, 'r') as load_f:
        load_data = json.load(load_f)
    salt_a_a = load_data['config']['login']['LoginMethod']['password']['salt']['salt_a_a']
    salt_a_b = load_data['config']['login']['LoginMethod']['password']['salt']['salt_a_b']
    salt_b_a = load_data['config']['login']['LoginMethod']['password']['salt']['salt_b_a']
    salt_b_b = load_data['config']['login']['LoginMethod']['password']['salt']['salt_b_b']
    pwd = password
    salt_part_a = salt_a_a + str(user_id + 1) + salt_a_b
    salt_part_b = salt_b_a + str(user_id - 1) + salt_b_b
    pwd_final = salt_part_a + pwd + salt_part_b
    hash_pwd = hashlib.sha512(pwd_final.encode()).hexdigest()
    return hash_pwd
