import re
from n_utils.mfa_utils import mfa_add_token, mfa_delete_token, mfa_generate_code

class MyArgs:
    def __init__(self):
        self.token_name = "test-token"
        self.token_secret = "I65VU7K5ZQL7WB4E"
        self.token_arn = "arn:aws:token:adfd0987654321"
        self.force = True

def test_add_token():
    mfa_add_token(MyArgs())

def test_get_code():
    assert re.match(r"[0-9]{6}", mfa_generate_code(MyArgs().token_name))

def test_delete_token():
    mfa_delete_token(MyArgs().token_name)