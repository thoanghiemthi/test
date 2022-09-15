from domain.model import Member, Score
from repositories import constant
from datetime import datetime
from domain.model import (Issue, Score, Member)
import json

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

    def deadline_rate(self, duedate, status, finishdate, startdate, spend_day) -> str:
        if duedate and duedate < datetime.now() and status != constant.STATUS_DONE:
            return 'late'

        if not finishdate or not startdate:
            return 'fail'

        if spend_day:
            # +1 do tính cùng ngày là 1 ngày
            date_delta = (finishdate - startdate).days \
                         + 1 - spend_day

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

    def covert(self):
        external_data = {}
        return Issue(**external_data)


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
    def __init__(self):
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
    def total_point(self,assigned_issue,support_issues):
        rl_point = self.Release_point()
        Sp_bonus_percent = self.support_bonus_percent(support_issues)
        Monthly_bonus_point = self.monthly_bonus_point(rl_point,Sp_bonus_percent)
        Train_percent = self.training_bonus_percent()
        Im_point = self.Improvement_point()
        Performance_p = self.performance_point(assigned_issue)
        total = round(Monthly_bonus_point + Train_percent + Im_point + Performance_p, 2 )
        return Score(performance_point = Performance_p,
                     improvement_bonus_percent = ,
                     training_bonus_percent =,

                     monthly_bonus_point =,
                     support_bonus_percent=,
                     release_bonus_percent = ,
                     total = ,




        )
