"""
TODO: print progress
      sort by stars
      sort by # of commits
      sort by # of +- code
      sort by last contributed repositories
      filter by date interval
"""
import json

import tabulate

from show_me.utils import set_logging

logger = set_logging()





# g = G(os.environ["GITHUB_TOKEN"])
# contributions = g.get_contributaions()
# 
# print(contributions)
# 
# with open("j", "w") as fd:
#     json.dump(contributions, fd, indent=2)

with open("j", "r") as fd:
    contributions = json.load(fd)


prs = contributions["data"]["viewer"]["contributionsCollection"]["pullRequestContributions"]["edges"]
issues = contributions["data"]["viewer"]["contributionsCollection"]["issueContributions"]["edges"]

data = []

for p in prs:
    n = p["node"]["pullRequest"]
    data.append(
        (n["title"], n["repository"]["nameWithOwner"], n["commits"]["totalCount"])
    )

for i in issues:
    n = i["node"]["issue"]
    data.append(
        (n["title"], n["repository"]["nameWithOwner"], "")
    )

print(tabulate.tabulate(data))
