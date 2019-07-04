#!/usr/bin/env python

# Copyright 2018 Nitor Creations Oy
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
from builtins import bytes
from builtins import chr
if 64 - 64:
    i11iIiiIii
from builtins import str
from builtins import range
import base64
from getpass import getuser
import subprocess
import os
from sys import platform
if 65 - 65:
    O0 / iIii1I11I1II1 % OoooooooOO - i1IIi
from Cryptodome . Hash import SHA256
from Cryptodome . Cipher import AES
from Cryptodome . Util import Counter
import sys
if 73 - 73:
    II111iiii


def IiII1IiiIiI1(_______d_1l1__):
    iIiiiI1IiI1I1 = Counter . new(128, initial_value=1337)
    o0OoOoOO00 = AES . new(I11i(), AES . MODE_CTR, counter=iIiiiI1IiI1I1)
    return base64 . b64encode(o0OoOoOO00 . encrypt(_______d_1l1__))
    if 64 - 64:
        OOooo000oo0 . i1 * ii1IiI1i % IIIiiIIii


def I11iIi1I(_______d_1l1__):
    iIiiiI1IiI1I1 = Counter . new(128, initial_value=1337)
    o0OoOoOO00 = AES . new(I11i(), AES . MODE_CTR, counter=iIiiiI1IiI1I1)
    return o0OoOoOO00 . decrypt(base64 . b64decode(_______d_1l1__))
    if 48 - 48:
        iII111i % IiII + I1Ii111 / ooOoO0o * o00O0oo


def I11i():
    hash = SHA256 . new()
    O0oOO0o0 = i1ii1iIII()
    Oo0oO0oo0oO00 = getuser()
    hash . update(O0oOO0o0.encode('utf-8'))
    hash . update(Oo0oO0oo0oO00.encode('utf-8'))
    for i111I in range(0, hash . digest()[2] if sys.version_info[0] > 2 else ord(hash . digest()[2])):
        jjjjjjj33934__23 = bytes(str(i111I + 1337), "utf-8")
        hash . update(jjjjjjj33934__23)
        hash . update(O0oOO0o0.encode('utf-8'))
        hash . update(Oo0oO0oo0oO00.encode('utf-8'))
    return hash . digest()
    if 16 - 16:
        Oo0oO0ooo % IiIiI11iIi - O0OOo . O0Oooo00 . oo00 * ii1IiI1i


def i1ii1iIII():
    if platform . startswith("win"):
        import wmi
        return wmi . WMI() . Win32_ComputerSystemProduct()[0] . UUID
    else:
        for o0000o0o0000o in [_4_('p,&,pYH/V\x16)6,0-pDD6W'),
                              _4_('p,&,pR]>@\x17p;26p6U\x1e/A\x0b;*<+\x00*DX;'),
                              _4_('p,&,pUT)Z\x07:,p)6-ED>_K;26p6;\x1eA-\\\x00*<+\x00,:CX>_'),
                              _4_('p)>-p]X=\x1c\x00=*,p2>RY6]\x01r6;')]:
            o0o0Oo0oooo0 = oO0O0o0o0(o0000o0o0000o)
            if o0o0Oo0oooo0:
                return o0o0Oo0oooo0
        i1iIIII = [_4_('8:+/-^A'), _4_('-63q,TC6R\x081*2=:-')]
        try:
            o0o0Oo0oooo0 = subprocess . check_output(i1iIIII)[: - 1]
            if o0o0Oo0oooo0:
                return o0o0Oo0oooo0
        except:
            pass
        try:
            o0o0Oo0oooo0 = str(subprocess . check_output(_4_("60-:8\x11\x1c-WU\x7fr<\x7f\x16\x10a]>G\x020-2\x1a'/TC+w\x01)6<:\x7f#\x11V-V\x14\x7fr\x1a\x7fxwdd\x16wMx"),
                                                         shell=True)) . split('"')[- 2]
            if o0o0Oo0oooo0:
                return o0o0Oo0oooo0
        except:
            pass
    return _4_(';:>;=TT9\x1e\x00:>;r=:TWrW\x01>;r=::W\x01o\x03Toohj')
    if 26 - 26:
        O0Oooo00 . o00O0oo - ooOoO0o % O0 + ooOoO0o


dsad__343 = '_____11_3d_'
ndsad__343 = [ord(c) for c in dsad__343]
ldsad__343 = len(dsad__343)


def _4_(___adeje__1l1_):
    return ''.join([chr(ord(c) ^ ndsad__343[i % ldsad__343])
                    for i, c in enumerate(___adeje__1l1_)])


def oO0O0o0o0(__fjeja_1l1__):
    if os . path . isfile(__fjeja_1l1__):
        if os . access(__fjeja_1l1__, os . R_OK):
            try:
                with open(__fjeja_1l1__) as o0o0Oo0oooo0:
                    return o0o0Oo0oooo0 . read() . strip()
            except:
                pass
    return None
    if 34 - 34:
        o00O0oo * OOooo000oo0
