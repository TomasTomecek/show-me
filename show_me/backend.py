"""
Getting the data from a backend: Github
"""
import logging

import requests


logger = logging.getLogger(__name__)

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
        self.session = requests.Session()
        self.session.headers.update({'Authorization': f'token {token}'})

    def request(self, query):
        """
        do a GraphQL request
        """
        logger.debug(f'query = {query}')
        response = self.session.post(url=URL, json={'query': query})
        return response

    def get_contributaions(self):
        return self.request(INSANITY_QUERY).json()
