import os
import hashlib
import json
import warnings

from hash_encrypt import hash_encrypt
import password
import yubikey

ACCOUNT_DATA_FILE = 'account.json'

class Authenticator(object):

    def authenticate(self, code):
        pass

class PasswordAuthenticator(Authenticator):

    def __init__(self, user_id):
        self.user_id = user_id

    def authenticate(self, code):
        return password.authenticate(self.user_id, code)

class YubiKeyAuthenticator(Authenticator):

    def __init__(self, user_id):
        self.user_id = user_id

    def authenticate(self, code):
        return yubikey.authenticate(self.user_id, code)

class FalseAuthenticator(Authenticator):

    def authenticate(self, code):
        return False

if __name__ == "__main__":
    pass

