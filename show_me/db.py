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
        self.process_reviews()
        self.process_commits()
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

    def process_commits(self):
        commit_contrib = self.c["data"]["viewer"]["contributionsCollection"]["commitContributionsByRepository"]
        for repo_contrib in commit_contrib:
            contributions = repo_contrib["contributions"]["edges"]
            for c in contributions:
                n = c["node"]
                nwo = n["repository"]["nameWithOwner"]
                repo = self.m.setdefault(nwo, RepositoryStat(nwo))
                total_commits = n["commitCount"]
                repo.commit_count += total_commits

    def process_reviews(self):
        reviews = self.c["data"]["viewer"]["contributionsCollection"]["pullRequestReviewContributions"]["edges"]
        for r in reviews:
            n = r["node"]
            nwo = n["repository"]["nameWithOwner"]
            repo = self.m.setdefault(nwo, RepositoryStat(nwo))
            repo.review_count += 1
