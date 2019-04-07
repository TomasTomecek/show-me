"""
Getting the data from a backend: Github
"""
import json
import logging

import requests

from show_me.constants import URL


logger = logging.getLogger(__name__)

START_DATE = "{year}-01-01T00:00:00"
END_DATE = "{year}-12-31T23:59:59"

INSANITY_QUERY = """
{{
  viewer {{
    contributionsCollection(from: "{start_date}", to: "{end_date}") {{
      commitContributionsByRepository {{
        contributions(first: 100{commit_cursor}) {{
          edges {{
            cursor
            node {{
              commitCount
              repository {{
                nameWithOwner
              }}
            }}
          }}
        }}
      }}    
      pullRequestReviewContributions(first: 100{review_cursor}) {{
        edges {{
          cursor
          node {{
            repository {{
              nameWithOwner
            }}
          }}
        }}
      }}
      pullRequestContributions(first: 100{pr_cursor}) {{
        edges {{
          cursor
          node {{
            pullRequest {{
              commits {{
                totalCount
              }}
              title
              repository {{
                nameWithOwner
              }}
            }}
          }}
        }}
      }}
      issueContributions(first: 100{issue_cursor}) {{
        edges {{
          cursor
          node {{
            issue {{
              title,
              repository {{
                nameWithOwner
              }}
            }}
          }}
        }}
      }}
    }}
  }}
}}
"""


def render_template_query(year, issue_cursor="", pr_cursor="", review_cursor="", commit_cursor=""):
    if issue_cursor:
        issue_cursor = f", after: \"{issue_cursor}\""
    if pr_cursor:
        pr_cursor = f", after: \"{pr_cursor}\""
    if review_cursor:
        review_cursor = f", after: \"{review_cursor}\""
    if commit_cursor:
        commit_cursor = f", after: \"{commit_cursor}\""
    q = INSANITY_QUERY.format(
        start_date=START_DATE.format(year=year),
        end_date=END_DATE.format(year=year),
        issue_cursor=issue_cursor,
        pr_cursor=pr_cursor,
        review_cursor=review_cursor,
        commit_cursor=commit_cursor
    )
    return q


class G:
    """ GraphQL client """
    issue_cursor: str
    pr_cursor: str
    review_cursor: str
    commit_cursor: str

    def __init__(self, token):
        self.session = requests.Session()
        self.token = token
        self.session.headers.update({'Authorization': f'token {token}'})
        self.reset_cursors()

    def reset_cursors(self):
        self.issue_cursor = ""
        self.pr_cursor = ""
        self.review_cursor = ""
        self.commit_cursor = ""

    def request(self, query):
        """
        do a GraphQL request
        """
        assert self.token, "Please set a github token."
        logger.debug(f'query = {query}')
        response = self.session.post(url=URL, json={'query': query})
        return response

    def _get_i_cursor(self, contrib_collection):
        i_edges = contrib_collection["issueContributions"]["edges"]
        if i_edges:
            self.issue_cursor = i_edges[-1]["cursor"]
            return True

    def _get_pr_cursor(self, contrib_collection):
        pr_edges = contrib_collection["pullRequestContributions"]["edges"]
        if pr_edges:
            self.pr_cursor = pr_edges[-1]["cursor"]
            return True

    def _get_r_cursor(self, contrib_collection):
        r_edges = contrib_collection["pullRequestReviewContributions"]["edges"]
        if r_edges:
            self.review_cursor = r_edges[-1]["cursor"]
            return True

    def _get_c_cursor(self, contrib_collection):
        response = None
        max = 0
        for c in contrib_collection["commitContributionsByRepository"]:
            edges = c["contributions"]["edges"]
            if not edges:
                continue
            num = len(edges)
            cursor = edges[-1]["cursor"]
            if num > max:
                response = cursor
                max = num
            logger.debug(f"items = {num}, cursor = {cursor}")
        if response:
            self.commit_cursor = response
        return response

    def _get_template_query(self, year, last_response=None):
        if last_response:
            cc = last_response["data"]["viewer"]["contributionsCollection"]
            if not any((
                self._get_i_cursor(cc),
                self._get_pr_cursor(cc),
                self._get_r_cursor(cc),
                self._get_c_cursor(cc),
            )):
                logger.debug("we know everything now")
                # everything is processed
                return
        return render_template_query(
            year,
            issue_cursor=self.issue_cursor,
            pr_cursor=self.pr_cursor,
            review_cursor=self.review_cursor,
            commit_cursor=self.commit_cursor
        )

    def get_contributions(self):
        json_set = []
        j = None
        years_to_scan = iter(range(2010, 2020))
        year = next(years_to_scan)
        import ipdb; ipdb.set_trace()
        while True:
            query = self._get_template_query(year, last_response=j)
            if not query:
                self.reset_cursors()
                j = None
                try:
                    year = next(years_to_scan)
                except StopIteration:
                    break
                continue
            j = self.request(query).json()
            if "errors" in j:
                raise RuntimeError(json.dumps(j, indent=2))
            json_set.append(j)
        logger.debug("# of queries = %d", len(json_set))
        return json_set
