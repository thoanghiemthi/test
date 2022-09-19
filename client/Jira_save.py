from jira import JIRA

from core import config
from datetime import datetime
import time
from celery import Celery


class JiraClient(object):
    def __init__(self, url: str, jira_admin: str, jira_token: str) -> None:
        self.url = url
        self.jira_admin = jira_admin
        self.jira_token = jira_token
        self.jira = None

    def connect(self) -> JIRA:
        self.jira = JIRA(self.url, basic_auth=(self.jira_admin, self.jira_token))
        return self.jira

    def search_issues(self, jql_str: str = '', max_results: int = 500) -> list:
        return self.jira.search_issues(jql_str=jql_str, maxResults=max_results)

    def time_query_str(self, month: str = None) -> tuple:
        start_str = ''
        end_str = ''
        start_date = 16
        end_date = 15

        if not month:
            now = datetime.now()
            _year, _month = now.year, now.month
        else:
            _year, _month = month.split("-")

        start_str = "{}-{}-{}".format(
            _year, int(_month) - 1, start_date
        )
        end_str = "{}-{}-{}".format(
            _year, int(_month), end_date
        )

        return start_str, end_str


class save_data:
    def __init__(self, moth):
        self.J = JiraClient(
            url=config.JIRA_URL,
            jira_admin=config.JIRA_ADMIN,
            jira_token=config.JIRA_TOKEN)
        print("start connect")
        self.J.connect()
        print("connected")
        self.start_str, self.end_str = self.J.time_query_str(moth)
        # username = "toantruongvan",
        startss = time.time()
        print("start", startss)

    def aquery_isjsues(self, jql_str: str):
        return self.J.search_issues(jql_str=jql_str)

    def assigned_issues(self) -> list:
        jql_str = "assignee  AND duedate >= {} AND duedate <= {} and type in (Epic,Sub-task,Task,'New Feature') and status not in ('In Review', 'Reject') ORDER BY assignee DESC".format(
            self.start_str, self.end_str)
        return self.aquery_isjsues(jql_str)

    def support_issues(self) -> list:
        jql_str = "'BFP_Người hỗ trợ'   AND duedate >= {} AND duedate <= {} and type in (Epic,Sub-task,Task,'New Feature') and status not in ('In Review', 'Reject') ORDER BY assignee DESC".format(
            self.start_str, self.end_str)
        return self.aquery_isjsues(jql_str)

    @Celery.task
    def save_issue(self):
        curDT = datetime.now()
        namefile = curDT.strftime("%Y_%m")
        total_issue = {}
        total_issue["assign_issue"] = self.assigned_issues()
        total_issue["support_issue"] = self.support_issues()
        f = open(namefile + ".json", "w")
        f.writelines(total_issue)
