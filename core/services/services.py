# from core.domain.model import Member, Score
from repositories import constant
from datetime import datetime
from core.domain.model import (Issue, Score, Member)
import json
from jira.resources import Issue
from core import config

f = open('/home/thoa/PycharmProjects/scoring_hexagonal/issuseTable.json')
data = json.load(f)
data = data["issueTable"]
data = data['table']
print("data", data)


class GetIssue(Member):
    def __init__(self, username: str, month: str = None) -> None:
        super().__init__(username, month)
        f = open('/home/thoa/PycharmProjects/scoring_hexagonal/issuseTable.json')
        self.data = json.load(f)
        self.data = self.data["issueTable"]
        self.data = self.data['table']
        print("data", self.data)

    def __parse_datetime(self, date) -> datetime:
        try:
            return datetime.strptime(date, constant.PATTERN_DATETIME)
        except:
            return None

    def deadline_rate(self, duedate, status, finishdate, startdate, spendday) -> str:
        if duedate and duedate < datetime.now() and status != constant.STATUS_DONE:
            return 'late'

        if not finishdate or not startdate:
            return 'fail'

        if spendday:
            # +1 do tính cùng ngày là 1 ngày
            date_delta = (finishdate - startdate).days \
                         + 1 - spendday

            if date_delta == 0:
                return 'pass'
            elif date_delta > 0:
                return 'late'
            else:
                return 'early'
        else:
            if finishdate == duedate:
                return 'pass'
            elif finishdate > duedate:
                return 'late'
            else:
                return 'early'

    def covertdata(self, issue):
        list_issue = []
        for i in issue:
            duedate = self.__parse_datetime(i["duedate"])
            startdate = self.__parse_datetime(i["startdate"])
            finishdate = self.__parse_datetime(i["finishdate"])
            status = i["status"]
            spendday = i["spendday"] if i['spendday'] else None

            Issue(assignee=i["assignee"],
                  task_id=i["key"],
                  link="{}/browse/{}".format(config.JIRA_URL, i["task_id"]),
                  summary=i["summary"],
                  category=i["category"],
                  type=i["type"],
                  level=i["level"],
                  due_date=self.__parse_datetime(i["duedate"]),
                  start_date=self.__parse_datetime(i["startdate"]),
                  finish_date=self.__parse_datetime(i["finishdate"]),
                  rate=i["rate"] if i['rate'] else None,
                  spend_day=i["spendday"] if i['spendday'] else None,
                  status=i["status"],
                  deadline_rate=self.deadline_rate(duedate, status, finishdate, startdate, spendday))
            list_issue.append(dict(Issue))
        return list_issue

    def getIssue(self):
        self.data["assign_issue"] = self.covertdata(self.data["assign_issue"])
        self.data["support_issue"] = self.covertdata(self.data["support_issue"])
        return self.data


class IssueCalculator(object):
    def __init__(self, issue: dict) -> None:
        super().__init__()
        self.issue = issue

    def calc_issue(self, issue: dict) -> dict:
        rank_str = "lateOrNotDoneOrNone"

        if issue["status"] == constant.STATUS_DONE:
            rank_str = "{}{}".format(issue["deadline_rate"], issue["rate"])
            issue["rank"] = constant.RANKS.get(rank_str, 'E')
        else:
            issue["rank"] = "E"

        point_str = "{}{}{}".format(issue["type"], issue["level"], issue["rank"])
        issue["point"] = constant.POINTS.get(point_str, 0)
        issue["rank_str"] = rank_str
        issue["point_str"] = point_str

        return issue

    def calc_support_issue(self, issue: dict) -> dict:
        pass


class Cal_Score(Member):
    def __init__(self, username: str, month: str):
        super().__init__(username, month)
        self.quota = constant.MEMBERS[self.username]

    def salary_bonus(self, point: float) -> int:
        if point < 70:
            return constant.SALARY_BONUS["L0"]
        elif 70 <= point < 110:
            return constant.SALARY_BONUS["L1"]
        elif 110 <= point < 120:
            return constant.SALARY_BONUS["L2"]
        elif 120 <= point < 130:
            return constant.SALARY_BONUS["L3"]
        elif 130 <= point < 150:
            return constant.SALARY_BONUS["L4"]
        elif 150 <= point < 170:
            return constant.SALARY_BONUS["L5"]
        elif 170 <= point:
            return constant.SALARY_BONUS["L6"]

    def Release_point(self):
        release_issue = constant.RELEASE_BONUS.get(self.month, {}).get(self.username)
        release_bonus_percent = release_issue["point"] if release_issue else 0
        return release_bonus_percent

    def support_bonus_percent(self, support_issues):
        total_support_issues_point = 0
        tt_sp_persent = 0
        for support_issue in support_issues:
            s_issue = IssueCalculator(support_issue)
            calcul_support_issue = s_issue.calc_issue(support_issue)
            if calcul_support_issue['point'] > 0:
                earned = calcul_support_issue['point'] * constant.SUPPORT_RATE
                total_support_issues_point += earned
        tt_sp_persent = total_support_issues_point * 0.7 * 100.0 / self.quota
        return tt_sp_persent

    def monthly_bonus_point(self, support_bonus_percent=0, release_bonus_percent=0):
        return support_bonus_percent + release_bonus_percent

    def training_bonus_percent(self):
        training_issues = constant.TRAINING_BONUS.get(self.month, {}).get(self.username)
        training_bonus_percent = training_issues['point'] if training_issues else 0
        return training_bonus_percent

    def Improvement_point(self):
        improvement_issues = constant.IMPROVEMENT_BONUS.get(self.month, {}).get(self.username)
        improvement_bonus_percent = improvement_issues['point'] if improvement_issues else 0
        return improvement_bonus_percent

    def performance_point(self, assigned_issue):
        performance_point = 0
        for i in assigned_issue:
            a_issue = IssueCalculator(i)
            percent = a_issue["point"] * 0.7 * 100 / self.quota
            performance_point += percent
        return performance_point

    def total_point(self, assigned_issue, support_issues):
        rl_point = self.Release_point()
        Sp_bonus_percent = self.support_bonus_percent(support_issues)
        Monthly_bonus_point = self.monthly_bonus_point(rl_point, Sp_bonus_percent)
        Train_percent = self.training_bonus_percent()
        Im_point = self.Improvement_point()
        Performance_p = self.performance_point(assigned_issue)
        total = round(Monthly_bonus_point + Train_percent + Im_point + Performance_p, 2)
        salary_bonus = self.salary_bonus(total)
        return Score(performance_point=Performance_p,
                     improvement_bonus_percent=Im_point,
                     training_bonus_percent=Train_percent,
                     monthly_bonus_point=Monthly_bonus_point,
                     support_bonus_percent=Sp_bonus_percent,
                     release_bonus_percent=rl_point,
                     total=total,
                     salary_bonus=salary_bonus
                     )


class tb_totalPoint():

    def __init__(self, month: str = None) -> None:
        super().__init__()
        self.month = month

    def all(self, sort: bool = True, short: bool = False) -> dict:
        re = {}

        for username in self.list_username():

            issue = GetIssue(username=username, month=self.month).getIssue()

            m = dict(
                Cal_Score(username=username, month=self.month).total_point(issue["assign_issue"], issue["support"]))

            if short:

                re[username] = {
                    "total": m["total"],
                    "salary_bonus": m["salary_bonus"],
                }
            else:
                re[username] = m

        if short and sort:
            re = dict(sorted(re.items(), key=lambda item: -item[1]["total"]))

        return re

    def list_username(self) -> list:
        return list(constant.MEMBERS.keys())
