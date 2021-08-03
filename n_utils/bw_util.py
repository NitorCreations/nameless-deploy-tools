import json
from os import devnull
import pyotp
import string
from subprocess import Popen, PIPE


def strip_whitespace(s):
    return s.translate({ord(c): None for c in string.whitespace})


_BW_CACHE = {}
NO_ENTRY = "NO ENTRY"


def get_bwentry(search_term):
    if search_term in _BW_CACHE:
        if _BW_CACHE[search_term] == NO_ENTRY:
            return None
        return _BW_CACHE[search_term]
    proc = Popen(
        ["bw", "list", "items", "--search", search_term],
        stdout=PIPE,
        stderr=open(devnull, "w"),
    )
    item, _ = proc.communicate()
    if proc.returncode != 0:
        return None

    item_data = json.loads(item)
    if len(item_data) > 0:
        # find exact match for search term
        item = [
            item for item in item_data if item["name"].lower() == search_term.lower()
        ][0]
        ret = BwEntry(item)
        _BW_CACHE[search_term] = ret
        return ret
    else:
        _BW_CACHE[search_term] = NO_ENTRY
        return None


class BwEntry:
    def __init__(self, item_data):
        super().__init__()
        self.fields = {}
        self.uris = []
        if "fields" in item_data:
            for field in item_data["fields"]:
                self.fields[field["name"]] = field["value"]
        self.username = item_data["login"]["username"]
        self.password = item_data["login"]["password"]
        self.totp = item_data["login"]["totp"]
        if self.totp:
            self.totp_now = pyotp.TOTP(strip_whitespace(self.totp)).now()
        else:
            self.totp_now = None
        if "uris" in item_data["login"]:
            for uri in item_data["login"]["uris"]:
                self.uris.append(uri["uri"])
