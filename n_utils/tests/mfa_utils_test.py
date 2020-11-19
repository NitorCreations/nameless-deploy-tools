import re
import json
from os import unlink
from tempfile import NamedTemporaryFile
from n_utils import _to_bytes
from n_utils.mfa_utils import mfa_add_token, mfa_delete_token, mfa_generate_code, mfa_backup_tokens, mfa_decrypt_backup_tokens

class MyArgs:
    def __init__(self):
        self.token_name = "test-token"
        self.token_secret = "I65VU7K5ZQL7WB4E"
        self.token_arn = "arn:aws:token:adfd0987654321"
        self.force = True
        self.bitwarden_entry = None

MY_ARGS = MyArgs()

def test_add_token():
    mfa_add_token(MY_ARGS)

def test_get_code():
    assert re.match(r"[0-9]{6}", mfa_generate_code(MY_ARGS.token_name))

def test_backup():
    with NamedTemporaryFile(delete=False) as out:
        out.write(_to_bytes(mfa_backup_tokens("test")))
    tokens = json.loads(mfa_decrypt_backup_tokens("test", out.name))
    unlink(out.name)
    found = False
    for token in tokens:
        if token["token_name"] == MY_ARGS.token_name:
            assert token["token_arn"] == MY_ARGS.token_arn
            assert token["token_secret"] == MY_ARGS.token_secret
            found = True
    assert found

def test_delete_token():
    mfa_delete_token(MyArgs().token_name)