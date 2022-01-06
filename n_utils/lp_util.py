import json
from os import devnull
from subprocess import Popen, PIPE

_LP_CACHE = {}


def get_lpentry(search_term):
    if search_term in _LP_CACHE:
        return _LP_CACHE[search_term]
    proc = Popen(
        ["lpass", "show", "--all", "--quiet", "--json", "--expand-multi", search_term],
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
        ret = LpEntry(item)
        _LP_CACHE[search_term] = ret
        return ret
    else:
        _LP_CACHE[search_term] = None
        return None


class LpEntry:
    def __init__(self, item_data):
        super().__init__()
        self.uris = []
        self.notes = ""
        if "note" in item_data:
            self.notes = item_data["note"]
            if self.notes.startswith("NoteType:"):
                self.notedata = {}
                for line in self.notes.split("\n"):
                    item = line.split(":", 1)
                    if len(item) > 1:
                        self.notedata[item[0]] = item[1]
        if "username" in item_data:
            self.username = item_data["username"]
        if "password" in item_data:
            self.password = item_data["password"]
        if "uri" in item_data:
            self.uris.append(item_data["uri"])
