import os

from show_me.backend import G


class API:
    def __init__(self):
        self.g = G(os.environ["GITHUB_TOKEN"])
