#!/usr/bin/env python

# Copyright 2017 Nitor Creations Oy
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License
from builtins import str
from builtins import object
import os
import yaml
import pyotp
from os import walk
from n_utils.yuuuu3332111i1l1i import IiII1IiiIiI1, I11iIi1I
import json
import base64
import pyqrcode
from Cryptodome.Cipher import AES
from Cryptodome.Util import Counter
from Cryptodome.Hash import SHA256
from n_utils import _to_bytes, _to_str

def mfa_add_token(args):
    """ Adds or overwrites an MFA token to be used with role assumption.
        Tokens will be saved in a .ndt subdirectory in the user's home directory. """
    ndt_dir = get_ndt_dir()
    if not os.path.exists(ndt_dir):
        os.makedirs(ndt_dir)
    data = {
        'token_name': args.token_name,
        'token_secret': "enc--" + _to_str(IiII1IiiIiI1(_to_bytes(args.token_secret)))
    }
    if args.token_arn:
        data['token_arn'] = args.token_arn
    token_file = ndt_dir + '/mfa_' + args.token_name
    if os.path.isfile(token_file) and not args.force:
        raise ValueError('A token with the name ' + args.token_name + ' already exists!')
    with open(token_file, 'w') as outfile:
        os.chmod(token_file, 0o600)
        yaml.safe_dump(data, outfile, allow_unicode=True, default_flow_style=False)


def mfa_read_token(token_name):
    """ Reads a previously added MFA token file and returns its data. """
    data = None
    with open(get_ndt_dir() + '/mfa_' + token_name, 'r') as infile:
        try:
            data = yaml.load(infile, yaml.SafeLoader)
        except yaml.YAMLError as exc:
            print(exc)
    if data:
        if not data['token_secret'].startswith("enc--"):
            data['force'] = True
            mfa_add_token(Struct(**data))
            return mfa_read_token(token_name)
    return data


def get_ndt_dir():
    """ Gets cross platform ndt directory path. Makes sure it exists. """
    ndt_dir = os.path.expanduser("~/.ndt")
    if not os.path.exists(ndt_dir):
        os.makedirs(ndt_dir)
    return ndt_dir


def mfa_generate_code(token_name):
    """ Generates an MFA code with the specified token. """
    token = mfa_read_token(token_name)
    if token['token_secret'].startswith("enc--"):
        secret = I11iIi1I(token['token_secret'][5:])
    else:
        secret = token['token_secret']
    totp = pyotp.TOTP(secret)
    return totp.now()


def mfa_to_qrcode(token_name):
    """ Generates a qr code of the token for importing into other devices """
    token = mfa_read_token(token_name)
    if token['token_secret'].startswith("enc--"):
        secret = I11iIi1I(token['token_secret'][5:])
    else:
        secret = token['token_secret']
    url = "otpauth://totp/" + token_name + "?secret=" + secret
    qr = pyqrcode.create(url)
    print(qr.terminal())


def mfa_generate_code_with_secret(secret):
    """ Generates an MFA code using the secret passed in. """
    if _to_str(secret).startswith("enc--"):
        secret = I11iIi1I(secret[5:])
    totp = pyotp.TOTP(secret)
    return totp.now()


def mfa_delete_token(token_name):
    """ Deletes an MFA token file from the .ndt subdirectory in the user's
        home directory """
    os.remove(get_ndt_dir() + '/mfa_' + token_name)


def mfa_backup_tokens(backup_secret):
    """ Writes MFA secrets encrypted with backup_secret and base64 encoded to stdout. """
    tokens = []
    for token in list_mfa_tokens():
        token_data = mfa_read_token(token)
        if token_data['token_secret'].startswith("enc--"):
            token_data['token_secret'] = I11iIi1I(token_data['token_secret'][5:])
        tokens.append(token_data)
    counter = Counter.new(128, initial_value=1337)
    cipher = AES.new(get_backup_key_digest(backup_secret), AES.MODE_CTR, counter=counter)
    return base64.b64encode(cipher.encrypt(json.dumps(tokens)))


def mfa_decrypt_backup_tokens(backup_secret, file):
    """ Decrypts backed up MFA secrets from file, prints to stdout. """
    with open(os.path.expanduser(file), 'r') as infile:
        data = infile.read()
    counter = Counter.new(128, initial_value=1337)
    cipher = AES.new(get_backup_key_digest(backup_secret), AES.MODE_CTR, counter=counter)
    return cipher.decrypt(base64.b64decode(data)).decode()


class Struct (object):
    def __init__(self, ** entries):
        self . __dict__ . update(entries)


def list_mfa_tokens():
    tokens = []
    for (dirpath, dirnames, filenames) in walk(get_ndt_dir()):
        tokens.extend([fn[4:] for fn in filenames if fn.startswith("mfa_")])
        break
    return tokens


def get_backup_key_digest(backup_secret):
    key = SHA256.new()
    key.update(backup_secret.encode('utf-8'))
    return key.digest()
