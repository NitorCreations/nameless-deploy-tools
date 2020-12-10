import json
from os import devnull
from subprocess import Popen, PIPE

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
        ret = BwEntry(item_data[0])
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
        if "uris" in item_data["login"]:
            for uri in item_data["login"]["uris"]:
                self.uris.append(uri["uri"])
