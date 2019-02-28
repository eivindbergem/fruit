import time
from . import result_storage as storage
# from .misc import git_commit

# METADATA = {"git-commit": git_commit,
#             "random-seed": 

class Experiment(dict):
    def __init__(self, hyperparameters, only_journal=False):
        super().__init__()
        self['config'] = hyperparameters
        self['results'] = {}
        self['metadata'] = {}
        self.only_journal = only_journal

        self.generate_metadata()

    def generate_metadata(self):
        pass

    def add_result(self, key, value):
        self['results'][key] = value

    def add_metadata(self, key, value):
        self['metadata'][key] = value

    def __enter__(self):
        self.add_metadata("start", time.time())
        return self

    def __exit__(self, *exc):
        self.add_metadata("stop", time.time())
        if self['results']:
            self.save()

    def save(self):
        storage.insert(self, self.only_journal)
