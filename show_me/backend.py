"""
Getting the data from a backend: Github
"""
import logging

import requests

from show_me.constants import URL


logger = logging.getLogger(__name__)

INSANITY_QUERY = """
{
  viewer {
    contributionsCollection(from: "2019-01-01T00:00:00") {
      commitContributionsByRepository {
        contributions(last: 100) {
          edges {
            node {
              commitCount
              repository {
                nameWithOwner
              }
            }
          }
        }
      }    
      pullRequestReviewContributions(first: 100) {
        edges {
          node {
            repository {
              nameWithOwner
            }
          }
        }
      }
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
        self.token = token
        self.session.headers.update({'Authorization': f'token {token}'})

    def request(self, query):
        """
        do a GraphQL request
        """
        assert self.token, "Please set a github token."
        logger.debug(f'query = {query}')
        response = self.session.post(url=URL, json={'query': query})
        return response

    def get_contributaions(self):
        return self.request(INSANITY_QUERY).json()
