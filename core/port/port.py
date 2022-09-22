from core.services import services


class Get_tableScore_port():
    def get_tbScore(self, data, month, short):
        return services.GettableScore(data, month).all(short)


class GetIssue_port():
    def __init__(self, username: str, data) -> None:
        self.username = username
        self.data = data

    def get_issue(self) -> dict:
        return services.GetIssue(self.username, self.data).getIssue()
