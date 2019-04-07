import json
import os
from pathlib import Path
from typing import Dict

from show_me.backend import G
from show_me.db import StatProcessor


class API:
    def __init__(self, cache_file_path: Path):
        self.g = G(os.getenv("GITHUB_TOKEN", ""))
        self.cache_path = cache_file_path

    def cache_to_file(self, contributions: Dict):
        self.cache_path.write_text(json.dumps(contributions, indent=2))

    def load_from_file(self) -> Dict:
        return json.loads(self.cache_path.read_text())

    def get_contributions(self, start_year: int):
        return self.g.get_contributions(start_year)

    def get_stats(self, contributions):
        s = StatProcessor(contributions)
        return s.get_stats()
