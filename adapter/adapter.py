from core.port import port
import json
from datetime import datetime
from core.domain.model import Member
import os
from pathlib import Path


def data_repositoresadapter(Month):
    curDT = datetime.now()
    print("Month", Month)
    if not Month:
        namefile = curDT.strftime("%Y_%m")
    else:
        name = str(datetime.strptime(Month, "%Y-%m"))
        _year, _month = name.split("-")[:2]
        namefile = _year + '_' + _month
    # os.chdir()
    print("aaaaa", os.getcwd())

    file = os.getcwd() + "/repositories/" + namefile + '.json'
    # file = '/home/thoa/PycharmProjects/scoring_hexagon/repositories/2022_09.json'
    print("file", file)

    f = open(file, "r")
    return json.load(f)


class GetIssue_Addapter(Member):
    def __init__(self, username: str, month: str = None):
        super().__init__(username)
        self.username = username
        self.Month = month

    def getissueAdapter(self):
        data = data_repositoresadapter(self.Month)
        return port.GetIssue_port(self.username, data).get_issue()


class Get_tableScoreAdapter():
    def __init__(self, Month, short):
        self.Month = Month
        self.short = short
        self.data = data_repositoresadapter(self.Month)

    def getTb(self):
        return port.Get_tableScore_port().get_tbScore(self.data, self.Month, self.short)


if __name__ == '__main__':
    # Get_tableScoreAdapter('2022-09',True).getTb()
    GetIssue_Addapter('duynguyenngoc', '2022-09').getissueAdapter()
