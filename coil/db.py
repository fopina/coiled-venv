import json

from .config import ENV_DB


class DB(dict):
    def __init__(self, *a, **b):
        super().__init__(self, *b, **b)
        self.load()

    def load(self):
        self.clear()
        try:
            with open(ENV_DB) as f:
                self.update(json.load(f))
        except FileNotFoundError:
            pass

    def dump(self):
        with open(ENV_DB, 'w') as f:
            json.dump(self, f)
