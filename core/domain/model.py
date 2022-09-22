from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional
# from flask_pydantic import validate


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
    salary_bonus : Optional[str]


class Member:
    def __init__(self, username: str, month: str = None):
        self.username = username
        self.month = month
