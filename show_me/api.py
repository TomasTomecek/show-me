import json
import os
from typing import Dict

from show_me.backend import G
from show_me.db import StatProcessor


class API:
    def __init__(self):
        self.g = G(os.getenv("GITHUB_TOKEN", ""))
        self.cache_path = "j"

    def cache_to_file(self, contributions: Dict):
        with open(self.cache_path, "w") as fd:
            json.dump(contributions, fd, indent=2)

    def load_from_file(self) -> Dict:
        with open(self.cache_path, "r") as fd:
            contributions = json.load(fd)
        return contributions

    def get_contributions(self):
        return self.g.get_contributions()

    def get_stats(self, contributions):
        """
        return an ordered list of Repository statistics

        :return:
        """
        s = StatProcessor(contributions)
        return s.get_stats()
