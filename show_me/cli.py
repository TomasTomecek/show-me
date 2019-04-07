# -*- coding: utf-8 -*-
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

"""
TODO: print progress & add colors & nicer table
      add diffstats
      sort by stars
      sort by # of commits
      sort by # of +- code
      sort by last contributed repositories
      enable picking a different user
      add releases as contributions
"""
import logging
import sys
from pathlib import Path
from typing import Iterable

import click
import tabulate

from show_me.api import API
from show_me.constants import DEFAULT_START_YEAR
from show_me.db import RepositoryStat
from show_me.utils import set_logging, get_cache_file_path

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


class PathlibPath(click.Path):
    """Path argument which returns pathlib.Path"""

    def convert(self, value, param, ctx):
        return Path(super().convert(value, param, ctx))


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option(
    "-n", "--lines", default=15, show_default=True, help="Print first N lines."
)
@click.option(
    "--cache-file-path",
    type=PathlibPath(dir_okay=False),
    show_default=True,
    default=get_cache_file_path(),
    help="Path to the cache file.",
)
@click.option(
    "--load-from-cache", is_flag=True, help="Don't query Github and load from cache."
)
@click.option(
    "--save-to-cache",
    is_flag=True,
    help="Query Github and save response to a file (to save time and bandwidth).",
)
@click.option("--debug", is_flag=True, help="Show debug logs.")
@click.option(
    "--start-year",
    default=DEFAULT_START_YEAR,
    show_default=True,
    type=click.INT,
    help="Start counting the contributions in the selected year.",
)
def main(load_from_cache, save_to_cache, cache_file_path, debug, lines, start_year):
    """Show me my Github contributions!"""
    if debug:
        logger = set_logging(level=logging.DEBUG)
    else:
        logger = set_logging(level=logging.WARNING)
    logger.debug("cache file path = %s", cache_file_path)
    a = API(cache_file_path)
    if load_from_cache:
        c = a.load_from_file()
    else:
        click.echo("Querying Github and preparing results just for you.")
        try:
            c = a.get_contributions(start_year)
        except RuntimeError as ex:
            click.echo(f"Something went wrong:\n{ex}")
            sys.exit(7)
    if save_to_cache:
        a.cache_to_file(c)
    repo_stats: Iterable[RepositoryStat] = a.get_stats(c)

    data = [
        (
            x.name_with_owner,
            x.stars,
            x.contrib_sum(),
            x.pull_count,
            x.issue_count,
            x.commit_count,
            x.review_count,
        )
        for x in repo_stats[:lines]
    ]

    headers = ("Repo", "★", "Total", "Pulls", "Issues", "Commits", "Reviews")

    click.echo(tabulate.tabulate(data, headers=headers, tablefmt="presto"))


if __name__ == "__main__":
    main()
