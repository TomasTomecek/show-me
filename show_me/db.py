from typing import Iterable, Dict


class RepositoryStat:
    """ Contribution statistics for a repository """

    def __init__(self, name_with_owner: str):
        self.name_with_owner: str = name_with_owner
        self.pull_count: int = 0
        self.issue_count: int = 0
        self.commit_count: int = 0
        self.review_count: int = 0

    def contrib_sum(self):
        return self.pull_count + self.issue_count + self.commit_count + self.review_count

    def __repr__(self):
        return (
            f"RepoStat({self.name_with_owner}, PRs={self.pull_count}"
            f", issues={self.issue_count}, commits={self.commit_count}"
            f", reviews={self.review_count})"
        )

    def __str__(self):
        return (
            f"{self.name_with_owner}: PRs={self.pull_count}"
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
        return sorted(self.m.values(), key=lambda x: x.contrib_sum())

    def process_issues(self):
        issues = self.c["data"]["viewer"]["contributionsCollection"]["issueContributions"]["edges"]
        for i in issues:
            n = i["node"]["issue"]
            # n["title"]
            nwo = n["repository"]["nameWithOwner"]
            repo = self.m.setdefault(nwo, RepositoryStat(nwo))
            repo.issue_count += 1

    def process_pulls(self):
        prs = self.c["data"]["viewer"]["contributionsCollection"]["pullRequestContributions"]["edges"]
        for p in prs:
            n = p["node"]["pullRequest"]
            # n["title"]
            nwo = n["repository"]["nameWithOwner"]
            repo = self.m.setdefault(nwo, RepositoryStat(nwo))
            repo.pull_count += 1
            total_commits = n["commits"]["totalCount"]
            repo.commit_count += total_commits

    def process_commits(self):
        pass

    def process_reviews(self):
        pass

