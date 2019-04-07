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
from pathlib import Path
from typing import Iterable

import click
import tabulate

from show_me.api import API
from show_me.db import RepositoryStat
from show_me.utils import set_logging, get_cache_file_path

logger = set_logging()
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


class PathlibPath(click.Path):
    """Path argument which returns pathlib.Path"""
    def convert(self, value, param, ctx):
        return Path(super().convert(value, param, ctx))


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('--cache-file-path', type=PathlibPath(dir_okay=False), show_default=True,
              default=get_cache_file_path(), help="Path to the cache file.")
@click.option('--load-from-cache', is_flag=True, help="Don't query Github and load from cache.")
@click.option('--save-to-cache', is_flag=True,
              help="Query Github and save response to a file (to save time and bandwidth).")
def main(load_from_cache, save_to_cache, cache_file_path):
    """Show me my Github contributions!"""
    a = API(cache_file_path)
    if load_from_cache:
        c = a.load_from_file()
    else:
        c = a.get_contributions()
    if save_to_cache:
        a.cache_to_file(c)
    repo_stats: Iterable[RepositoryStat] = a.get_stats(c)

    data = [
        (x.name_with_owner, x.contrib_sum(), x.pull_count,
         x.issue_count, x.commit_count, x.review_count)
        for x in repo_stats
    ]

    headers = ("Repo", "Total", "P", "I", "C", "R")

    click.echo(tabulate.tabulate(data, headers=headers))


if __name__ == '__main__':
    main()
