"""
TODO: python packaging & upload to pypi
      print progress & add colors & nicer table
      show last 25 entries
      add stars
      add diffstats
      sort by stars
      sort by # of commits
      sort by # of +- code
      sort by last contributed repositories
      enable setting start date
      add releases as contributions
"""
from typing import Iterable

import tabulate

from show_me.api import API
from show_me.db import RepositoryStat
from show_me.utils import set_logging

logger = set_logging()


def main():
    a = API()
    c = a.get_contributions()
    a.cache_to_file(c)
    c = a.load_from_file()
    repo_stats: Iterable[RepositoryStat] = a.get_stats(c)

    data = [
        (x.name_with_owner, x.contrib_sum(), x.pull_count,
         x.issue_count, x.commit_count, x.review_count)
        for x in repo_stats
    ]

    headers = ("Repo", "Total", "P", "I", "C", "R")

    print(tabulate.tabulate(data, headers=headers))


main()
