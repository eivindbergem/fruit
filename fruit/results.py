import time
import uuid
from collections import defaultdict
from . import result_storage as storage
from .storage import DatabaseItem
from .misc import flatten_dict
from .tabulate import Tabular
# from .misc import git_commit

# METADATA = {"git-commit": git_commit,
#             "random-seed":



class Experiments(object):
    def get_experiments(self):
        return storage.get_results()

    def tabulate(self):
        exp = [flatten_dict(ex) for ex in self.get_experiments().values()]

        return Tabular(exp, ["metadata-id", "config-learning_rate"],
                       sort_by="config-learning_rate")

experiments = Experiments()

class Series(list):
    def __init__(self, start_time):
        self.start_time = start_time

    def add_value(self, value, timestep):
        if timestep == None:
            timestep = time.time() - self.start_time

        self.append((timestep, value))

class Experiment(DatabaseItem):
    def __init__(self, hyperparameters, only_journal=False):
        super().__init__()
        self['config'] = hyperparameters
        self['results'] = {}
        self['metadata'] = {}
        self['series'] = defaultdict(lambda : Series(self['metadata']['start']))
        self.only_journal = only_journal

        self.generate_metadata()

    def generate_metadata(self):
        self.add_metadata('id', self.uid)

    def add_result(self, key, value):
        self['results'][key] = value

    def add_metadata(self, key, value):
        self['metadata'][key] = value

    def add_to_series(self, key, value, timestep=None):
        self['series'][key].add_value(value, timestep)

    def __enter__(self):
        self.add_metadata("start", time.time())

        return self

    def __exit__(self, *exc):
        self.add_metadata("stop", time.time())
        if self['results']:
            self.save()

        try:
            self.get_path().rmdir()
        except OSError:
            pass

    def save(self):
        storage.insert(self, self.only_journal)

    def get_path(self):
        return storage.experiment_path(self)

    def print_summary(self):
        print("Experiment {}:".format(self.uid))

        for key, value in self['results'].items():
            print("{}: {}".format(key, value))
