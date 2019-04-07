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

from typing import Iterable, Dict


class RepositoryStat:
    """ Contribution statistics for a repository """

    def __init__(self, name_with_owner: str):
        self.name_with_owner: str = name_with_owner
        self.pull_count: int = 0
        self.issue_count: int = 0
        self.commit_count: int = 0
        self.review_count: int = 0
        self.stars: int = 0

    def contrib_sum(self):
        return (
            self.pull_count + self.issue_count + self.commit_count + self.review_count
        )

    def __repr__(self):
        return (
            f"RepoStat({self.name_with_owner}, ★{self.stars}, PRs={self.pull_count}"
            f", issues={self.issue_count}, commits={self.commit_count}"
            f", reviews={self.review_count})"
        )

    def __str__(self):
        return (
            f"{self.name_with_owner}: ★{self.stars}, PRs={self.pull_count}"
            f", issues={self.issue_count}, commits={self.commit_count}"
            f", reviews={self.review_count}"
        )


class StatProcessor:
    """ compute statistics for a specific data set """

    def __init__(self, contributions):
        self.c = contributions
        self.m: Dict[str, RepositoryStat] = {}

    def get_stats(self) -> Iterable[RepositoryStat]:
        self.process_issues()
        self.process_pulls()
        self.process_reviews()
        self.process_commits()
        return sorted(self.m.values(), key=lambda x: x.contrib_sum(), reverse=True)

    def process_issues(self):
        for c in self.c:
            issues = c["data"]["viewer"]["contributionsCollection"][
                "issueContributions"
            ]["edges"]
            for i in issues:
                n = i["node"]["issue"]
                # n["title"]
                nwo = n["repository"]["nameWithOwner"]
                repo = self.m.setdefault(nwo, RepositoryStat(nwo))
                repo.issue_count += 1
                repo.stars = n["repository"]["stargazers"]["totalCount"]

    def process_pulls(self):
        for c in self.c:
            prs = c["data"]["viewer"]["contributionsCollection"][
                "pullRequestContributions"
            ]["edges"]
            for p in prs:
                n = p["node"]["pullRequest"]
                # n["title"]
                nwo = n["repository"]["nameWithOwner"]
                repo = self.m.setdefault(nwo, RepositoryStat(nwo))
                repo.pull_count += 1
                repo.stars = n["repository"]["stargazers"]["totalCount"]

    def process_commits(self):
        for c in self.c:
            commit_contrib = c["data"]["viewer"]["contributionsCollection"][
                "commitContributionsByRepository"
            ]
            for repo_contrib in commit_contrib:
                contributions = repo_contrib["contributions"]["edges"]
                for c in contributions:
                    n = c["node"]
                    nwo = n["repository"]["nameWithOwner"]
                    repo = self.m.setdefault(nwo, RepositoryStat(nwo))
                    total_commits = n["commitCount"]
                    repo.commit_count += total_commits
                    repo.stars = n["repository"]["stargazers"]["totalCount"]

    def process_reviews(self):
        for c in self.c:
            reviews = c["data"]["viewer"]["contributionsCollection"][
                "pullRequestReviewContributions"
            ]["edges"]
            for r in reviews:
                n = r["node"]
                nwo = n["repository"]["nameWithOwner"]
                repo = self.m.setdefault(nwo, RepositoryStat(nwo))
                repo.review_count += 1
                repo.stars = n["repository"]["stargazers"]["totalCount"]
