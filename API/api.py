from werkzeug.utils import redirect
import sentry_sdk
from datetime import datetime
from flask import Flask, request, redirect, g
# from core. import ScoreTable, Member
from repositories.constant import PATERN_MONTH
from sentry_sdk.integrations.flask import FlaskIntegration
# from core.services import services
from adapter import adapter


def create_app(config_object=None):
    app = Flask(__name__, static_url_path='/static')

    if config_object:
        app.config.from_object(config_object)

    sentry_sdk.init(
        dsn=app.config["DSN"],
        integrations=[FlaskIntegration()]
    )

    @app.before_request
    def set_month() -> None:
        month = request.args.get('m')

        if not month:
            month = datetime.now().strftime(PATERN_MONTH)

        g.month = month

    @app.route("/")
    def home():
        print("g.month",g.month)
        table = adapter.Get_tableScoreAdapter(Month=g.month, short=True).getTb()

        # table = services.GettableScore(month=g.month).all(short=True,)

        now = datetime.now()
        year = now.year

        if now.day > 15:
            end_month = now.month + 1
        else:
            end_month = now.month
        table["end_month"] = end_month
        table["year"] = year

        return table

    @app.route("/members/<username>")
    def member(username):
        table = adapter.GetIssue_Addapter(username,g.month).getissueAdapter()
        # table =
        # table["username"] = username
        return table

    @app.route("/reportxxx")
    def report():
        table = adapter.Get_tableScoreAdapter(Month=g.month, short=True).getTb()
        return table

    return app
