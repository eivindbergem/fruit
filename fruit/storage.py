import json
import time
import shutil
import uuid
from pathlib import Path

from .misc import lockfile, add_suffix
class JsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Path):
            return str(obj)

        return json.JSONEncoder.default(self, obj)

class DatabaseItem(dict):
    def __init__(self, items=None, uid=None):
        if items != None:
            super().__init__(items)
        else:
            super().__init__()

        self.uid = uid if uid != None else str(uuid.uuid4())

    @classmethod
    def from_file(cls, filename):
        with filename.open() as fd:
            return cls(json.load(fd), filename.name)

class Database(dict):
    @classmethod
    def from_file(cls, filename):
        with filename.open() as fd:
            data = json.load(fd)

            return cls({uid: DatabaseItem(item, uid)
                        for uid,item in data.items()})

    def add_item(self, item):
        self[item.uid] = item

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
            return Database.from_file(self.database_filename())
        except FileNotFoundError:
            return []

    def get_results(self):
        self.merge_journal()
        return self.read()

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
            with open(self.journal_path() / item.uid, "w") as fd:
                json.dump(item, fd, cls=JsonEncoder)

    def merge_journal(self):
        with self.lock():
            data = self.read()
            journals = list(self.journal_path().iterdir())

            for filename in journals:
                item = DatabaseItem.from_file(filename)
                data.add_item(item)

            self.write(data)

            data = self.read()

            for filename in journals:
                item = DatabaseItem.from_file(filename)

                if item.uid in data and data[item.uid] == item:
                    filename.unlink()

    def experiment_path(self, ex):
        path = self.path / "ex" / ex.uid
        path.mkdir(parents=True, exist_ok=True)

        return path
