# https://yubico-client.readthedocs.io/en/latest/
# pip install yubico-client

from yubico_client import Yubico

ACCOUNT_DATA_FILE = 'account.json'

client = Yubico('42160', 'QdFqJ0hpRN3EFddDOfThTAL/4Hs=')


def get_identity(otp_code):
    return otp_code[0:12]


def auth(public_identity, otp_code):
    otp_auth = False
    err_code = ''
    try:
        if otp_code[0:12] == public_identity:
            otp_auth = client.verify(otp_code)
        else:
            err_code = 'INVALID_ID'
    except Exception as excpt:
        err_code = excpt.args[0]
    finally:
        return otp_auth, err_code
