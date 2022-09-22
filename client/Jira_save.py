from jira import JIRA
from jira.resources import Issue
from repositories import constant
from core import config
from datetime import datetime
import time
from celery import Celery
import json

from celery import Celery
appcelery = Celery('savedata', backend='rpc://', broker='amqp://guest@localhost//')
appcelery.conf.timezone = 'UTC'


@appcelery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    sender.add_periodic_task(60.0, test.s('2022-09'), name='add every 10')

    # Calls test('world') every 30 seconds
    # sender.add_periodic_task(30.0, test.s('world'), expires=10)
@appcelery.task
def test(arg):

    save_data(str(arg))

class BFIssue(Issue):
    def __reinit__(self) -> None:
        self.assignee = self.fields.assignee.name
        self.task_id = self.key
        self.summary = self.fields.summary
        self.type = self.fields.customfield_10304.value if self.fields.customfield_10304 else None
        self.category = self.fields.customfield_10303.value if self.fields.customfield_10303 else None
        self.level = self.fields.customfield_10226.value if self.fields.customfield_10226 else None
        print("self.fields.duedate",self.fields.duedate)
        self.duedate = self.__parse_datetime(self.fields.duedate)
        self.startdate = self.__parse_datetime(self.fields.customfield_10209)
        self.finishdate = self.__parse_datetime(self.fields.customfield_10210)
        self.rate = self.fields.customfield_10227.value if self.fields.customfield_10227 else None
        self.spend_day = int(self.fields.customfield_10707) if self.fields.customfield_10707 else None
        self.status = self.fields.status.name
        self.deadline_rate = self.deadline_rate()
        self.link = "{}/browse/{}".format(config.JIRA_URL, self.key)
        self.PATTERN_DATETIME = "%Y-%m-%d"
        self.STATUS_DONE = "Done"

    def to_dict(self) -> dict:
        return {
            "assignee": self.assignee,
            "task_id": self.task_id,
            "link": self.link,
            "summary": self.summary,
            "type": self.type,
            "category": self.category,
            "level": self.level,
            "duedate": str(self.duedate),
            "startdate": str(self.startdate),
            "finishdate": str(self.finishdate),
            "rate": self.rate,
            "spend_day": self.spend_day,
            "status": self.status,
            "deadline_rate": self.deadline_rate,
        }

    def __parse_datetime(self, date) -> datetime:
        # print("date",date,datetime.strptime(date, "%Y-%m-%d"))
        try:
            return datetime.strptime(date, "%Y-%m-%d")
        except:
            return None

    def deadline_rate(self) -> str:
        if self.duedate and self.duedate < datetime.now() and self.status != "Done":
            return 'late'

        if not self.finishdate or not self.startdate:
            return 'fail'

        if self.spend_day:
            # +1 do tính cùng ngày là 1 ngày
            date_delta = (self.finishdate - self.startdate).days \
                         + 1 - self.spend_day

            if date_delta == 0:
                return 'pass'
            elif date_delta > 0:
                return 'late'
            else:
                return 'early'
        else:
            if self.finishdate == self.duedate:
                return 'pass'
            elif self.finishdate > self.duedate:
                return 'late'
            else:
                return 'early'


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


class save_data():

    def __init__(self, moth):
        self.J = JiraClient(
            url=config.JIRA_URL,
            jira_admin=config.JIRA_ADMIN,
            jira_token=config.JIRA_TOKEN)
        print("start connect")
        self.J.connect()
        print("connected")
        self.start_str, self.end_str = self.J.time_query_str(moth)
        self.list_members = constant.MEMBERS.keys()
        self.username = ''
        self.save_issue()

    def __query_isjsues(self, jql_str: str) -> list:
        return self.J.search_issues(jql_str=jql_str)

    def assigned_issues(self) -> list:
        jql_str = "assignee = {} AND duedate >= {} AND duedate <= {} and type in (Epic,Sub-task,Task,'New Feature') and status not in ('In Review', 'Reject') ORDER BY assignee DESC".format(
            self.username, self.start_str, self.end_str)
        return self.__query_isjsues(jql_str=jql_str)

    def support_issues(self) -> list:
        jql_str = "'BFP_Người hỗ trợ' = {}  AND duedate >= {} AND duedate <= {} and type in (Epic,Sub-task,Task,'New Feature') and status not in ('In Review', 'Reject') ORDER BY assignee DESC".format(
            self.username, self.start_str, self.end_str)
        return self.__query_isjsues(jql_str=jql_str)

    def convert_issue(self, issue: Issue) -> BFIssue:
        issue.__class__ = BFIssue
        issue.__reinit__()
        return issue.to_dict()

    # @appcelery.task
    def save_issue(self):
        print("aaaaaaaa")
        curDT = datetime.now()
        path = r'/home/thoa/PycharmProjects/scoring_hexagon/repositories/'
        namefile = curDT.strftime("%Y_%m")
        f = open(path + namefile + ".json", "w")
        data_save = {}

        for k in self.list_members:
            self.username = k
            total_issue = {}
            list_issue = []
            for i in self.assigned_issues():
                i = self.convert_issue(i)
                list_issue.append(i)
            list_support_issue = []
            for j in self.support_issues():
                j = self.convert_issue(j)
                list_support_issue.append(j)
            total_issue["support_issue"] = self.support_issues()
            data_save["{}".format(self.username)] = {"list_issue": list_issue,
                                                     "list_support_issue": list_support_issue,

                                                     }
            print(self.username, data_save["{}".format(self.username)])
            json_object = json.dumps(data_save)

        print("data_save", str(data_save))
        f.writelines(json_object)


if __name__ == "__main__":
    save_data('2022-9')

