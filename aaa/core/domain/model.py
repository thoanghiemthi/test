from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional
from flask_pydantic import validate


class Issue(BaseModel):
    assignee: Optional[str]
    task_id: Optional[str]
    link: Optional[str]
    summary: Optional[str]
    category: Optional[str]
    type: Optional[str]
    level: Optional[str]
    due_date: Optional[str]
    start_date: Optional[datetime]
    finish_date: Optional[datetime]
    rate: Optional[str]
    spend_day: Optional[str]
    status: Optional[str]
    deadline_rate: Optional[str]


class Score(BaseModel):
    performance_point: Optional[float]
    improvement_bonus_percent: Optional[float]
    training_bonus_percent: Optional[float]
    monthly_bonus_point: Optional[float]
    support_bonus_percent: Optional[float]
    release_bonus_percent: Optional[float]
    total: Optional[float]


class Member:
    def __init__(self, username: str, month: str = None):
        self.username = username
        self.month = month
        self.start_str = None
        self.end_str = None
        self.time_query_str()

    def time_query_str(self):

        start_date = 16
        end_date = 15

        if not self.month:
            now = datetime.now()
            _year, _month = now.year, now.month
        else:
            _year, _month = self.month.split("-")

        self.start_str = "{}-{}-{}".format(
            _year, int(_month) - 1, start_date
        )
        self.end_str = "{}-{}-{}".format(
            _year, int(_month), end_date
        )
