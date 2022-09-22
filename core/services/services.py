from repositories import constant
from core.domain.model import (Score)


class GetIssue():
    def __init__(self, username: str, data) -> None:
        self.username = username
        self.data = data
        print("data", self.data)
    def getIssue(self):
        return self.data["{}".format(self.username)]


class IssueCalculator(object):
    def __init__(self, issue: dict) -> None:
        super().__init__()
        self.issue = issue

    def calc_issue(self) -> dict:
        rank_str = "lateOrNotDoneOrNone"
        print("status", self.issue["status"], constant.STATUS_DONE)
        if self.issue["status"] == constant.STATUS_DONE:
            rank_str = "{}{}".format(self.issue["deadline_rate"], self.issue["rate"])

            self.issue["rank"] = constant.RANKS.get(rank_str, 'E')
        else:
            self.issue["rank"] = "E"

        point_str = "{}{}{}".format(self.issue["type"], self.issue["level"], self.issue["rank"])
        print("point_str", point_str)
        self.issue["point"] = constant.POINTS.get(point_str, 0)
        self.issue["rank_str"] = rank_str
        self.issue["point_str"] = point_str

        return self.issue

    def calc_support_issue(self, issue: dict) -> dict:
        pass


class Cal_Score():
    def __init__(self, username: str, month: str):
        self.username = username
        self.month = month
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
        print("support_issues", support_issues)
        total_support_issues_point = 0
        tt_sp_persent = 0
        for support_issue in support_issues:
            s_issue = IssueCalculator(support_issue)
            calcul_support_issue = s_issue.calc_issue()
            print("calcul_support_issue['point']", calcul_support_issue['point'])
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
        print("assigned_issue____", len(assigned_issue), assigned_issue)
        performancepoint = 0
        for i in assigned_issue:
            a_issue = IssueCalculator(i).calc_issue()
            percent = a_issue["point"] * 0.7 * 100.0 / self.quota
            performancepoint += percent
        print("performancepoint", performancepoint)
        return performancepoint

    def total_point(self, assigned_issue, support_issues):
        rl_point = self.Release_point()
        Sp_bonus_percent = self.support_bonus_percent(support_issues)
        Monthly_bonus_point = self.monthly_bonus_point(rl_point, Sp_bonus_percent)
        Train_percent = self.training_bonus_percent()
        Im_point = self.Improvement_point()
        Performance_p = self.performance_point(assigned_issue)
        total = round(Monthly_bonus_point + Train_percent + Im_point + Performance_p, 2)
        salary_bonus = self.salary_bonus(total)
        print("aaaaaaaaaa", Score(performance_point=Performance_p,
                                  improvement_bonus_percent=Im_point,
                                  training_bonus_percent=Train_percent,
                                  monthly_bonus_point=Monthly_bonus_point,
                                  support_bonus_percent=Sp_bonus_percent,
                                  release_bonus_percent=rl_point,
                                  total=total,
                                  salary_bonus=salary_bonus
                                  ))
        return Score(performance_point=Performance_p,
                     improvement_bonus_percent=Im_point,
                     training_bonus_percent=Train_percent,
                     monthly_bonus_point=Monthly_bonus_point,
                     support_bonus_percent=Sp_bonus_percent,
                     release_bonus_percent=rl_point,
                     total=total,
                     salary_bonus=salary_bonus
                     )


class GettableScore():

    def __init__(self, data, month: str = None) -> None:
        super().__init__()
        self.month = month
        self.data = data

    def all(self, sort: bool = True, short: bool = False) -> dict:
        re = {}

        for username in self.list_username():


            issue = self.data["{}".format(username)]

            m = dict(
                Cal_Score(username=username, month=self.month).total_point(issue["list_issue"],
                                                                           issue["list_support_issue"]))

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


# if __name__ == "__main__":
#     aaa = GettableScore("2022-09").all()
#     print(aaa)
