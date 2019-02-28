import json
import time
import shutil
from pathlib import Path

from .misc import lockfile, add_suffix

class Storage(object):
    def __init__(self, path):
        self.path = Path(path)
        self.path.mkdir(exist_ok=True)

    def database_filename(self):
        return self.path / "db.json"

    def journal_path(self):
        path = self.path / "journal"
        path.mkdir(exist_ok=True)

        return path

    def lock(self):
        filename = self.path / "fuit.lock"

        return lockfile(filename)

    def read(self):
        try:
            with open(self.database_filename()) as fd:
                return json.load(fd)
        except FileNotFoundError:
            return []

    def write(self, data):
        filename = self.database_filename()
        tmp = add_suffix(filename, ".tmp")

        with open(tmp, "w") as fd:
            json.dump(data, fd)

        tmp.rename(filename)

    def insert(self, item, only_journal=False):
        self.insert_journal(item)

        if not only_journal:
            self.merge_journal()

    def insert_journal(self, item):
        with self.lock():
            with open(self.journal_path() / str(time.time()), "w") as fd:
                json.dump(item, fd)

    def merge_journal(self):
        with self.lock():
            data = self.read()
            journals = list(self.journal_path().iterdir())

            for filename in journals:
                with open(filename) as fd:
                    try:
                        data.append(json.load(fd))
                    except json.decoder.JSONDecodeError:
                        # TODO ERROR MESSAGE
                        pass

            self.write(data)

            for filename in journals:
                filename.unlink()
