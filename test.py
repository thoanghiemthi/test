# from jira import JIRA
#
# from core import config
# from datetime import datetime
# import time
# from jira.resources import Issue
# class JiraClient(object):
#     def __init__(self, url: str, jira_admin: str, jira_token: str) -> None:
#         self.url = url
#         self.jira_admin = jira_admin
#         self.jira_token = jira_token
#         self.jira = None
#
#     def connect(self) -> JIRA:
#         self.jira = JIRA(self.url, basic_auth=(self.jira_admin, self.jira_token))
#         return self.jira
#
#     def search_issues(self, jql_str: str = '', max_results: int = 500) -> list:
#         return self.jira.search_issues(jql_str=jql_str, maxResults=max_results)
#
#     def time_query_str(self, month: str = None) -> tuple:
#         start_str = ''
#         end_str = ''
#         start_date = 16
#         end_date = 15
#
#         if not month:
#             now = datetime.now()
#             _year, _month = now.year, now.month
#         else:
#             _year, _month = month.split("-")
#
#         start_str = "{}-{}-{}".format(
#             _year, int(_month) - 1, start_date
#         )
#         end_str = "{}-{}-{}".format(
#             _year, int(_month), end_date
#         )
#
#         return start_str, end_str
# if __name__=="__main__":
#     J = JiraClient(
#         url=config.JIRA_URL,
#         jira_admin=config.JIRA_ADMIN,
#         jira_token=config.JIRA_TOKEN)
#     print("start connect")
#     J.connect()
#     print("connected")
#     start_str, end_str = J.time_query_str("2022-9")
#     username  = 'toantruongvan',
#     startss = time.time()
#     print("start", startss)
#     jql_str = "assignee = {} AND duedate >= {} AND duedate <= {} and type in (Epic,Sub-task,Task,'New Feature') and status not in ('In Review', 'Reject') ORDER BY assignee DESC".format(
#         'tung491', '2022-8-16', '2022-9-15')
#     # jql_str = "'BFP_Người hỗ trợ' = {}  AND duedate >= {} AND duedate <= {} and type in (Epic,Sub-task,Task,'New Feature') and status not in ('In Review', 'Reject') ORDER BY assignee DESC".format(
#     #     'tung491', '2022-8-16', '2022-9-15')
#     aaa=J.search_issues(jql_str=jql_str)
#     for i in aaa:
#
#         print("aaaa",i)
#         print(Issue.get_field(i,"assignee"))
#         print(Issue.get_field(i,'summary'))
#         print(Issue.get_field(i,'summary'))
#         print()
#     print("ss", time.time()- startss)
# from celery import Celery
# from celery.schedules import crontab
#
# app = Celery()
#
# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     # Calls test('hello') every 10 seconds.
#     sender.add_periodic_task(10.0, test.s('hello'), name='add every 10')
#
#     # Calls test('world') every 30 seconds
#     sender.add_periodic_task(30.0, test.s('world'), expires=10)
#
#     # Executes every Monday morning at 7:30 a.m.
#     sender.add_periodic_task(
#         crontab(hour=7, minute=30, day_of_week=1),
#         test.s('Happy Mondays!'),
#     )
#
# @app.task
# def test(arg):
#     print(arg)
#
# @app.task
# def add(x, y):
#     z = x + y
#     print(z)
