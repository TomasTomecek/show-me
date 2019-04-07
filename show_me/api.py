# MIT License
#
# Copyright (c) 2019 Tomas Tomecek
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

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
