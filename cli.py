import os
import json
import logging

import requests
import tabulate


def set_logging(
        logger_name="show-me",
        level=logging.DEBUG,
        handler_class=logging.StreamHandler,
        handler_kwargs=None,
        format='%(asctime)s.%(msecs).03d %(filename)-17s %(levelname)-6s %(message)s',
        date_format='%H:%M:%S'):
    """
    Set personal logger for this library.

    :param logger_name: str, name of the logger
    :param level: int, see logging.{DEBUG,INFO,ERROR,...}: level of logger and handler
    :param handler_class: logging.Handler instance, default is StreamHandler (/dev/stderr)
    :param handler_kwargs: dict, keyword arguments to handler's constructor
    :param format: str, formatting style
    :param date_format: str, date style in the logs
    :return: logger instance
    """
    logger = logging.getLogger(logger_name)
    # do we want to propagate to root logger?
    # logger.propagate = False
    logger.setLevel(level)

    # don't readd handler
    if not [x for x in logger.handlers if isinstance(x, handler_class)]:
        handler_kwargs = handler_kwargs or {}
        handler = handler_class(**handler_kwargs)
        handler.setLevel(level)
        formatter = logging.Formatter(format, date_format)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


logger = set_logging()


URL = "https://api.github.com/graphql"


INSANITY_QUERY = """
{
  viewer {
    contributionsCollection(from: "2019-01-01T00:00:00") {
      pullRequestContributions(first: 100) {
        edges {
          cursor
          node {
            pullRequest {
              commits {
                totalCount
              }
              title
              repository {
                nameWithOwner
              }
            }
          }
        }
      }
      issueContributions(first: 100) {
        edges {
          cursor
          node {
            issue {
              title,
              repository {
                nameWithOwner
              }
            }
          }
        }
      }
    }
  }
}
"""


class G:
    """ GraphQL client """

    def __init__(self, token):
        """
        :param configuration: instance of Configuration
        :param git: instance of Git
        """
        self.session = requests.Session()
        self.session.headers.update({'Authorization': f'token {token}'})

    def request(self, query, method="GET"):
        """
        do a GraphQL request
        """
        logger.debug(f'query = {query}')
        response = self.session.post(url=URL, json={'query': query})
        return response

    def get_contributaions(self):
        return self.request(INSANITY_QUERY).json()


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

