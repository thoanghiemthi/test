from dotenv import load_dotenv
from distutils.util import strtobool
import os


load_dotenv()


ENV = os.environ.get("ENV", "development")
DEBUG = bool(strtobool(os.environ.get("DEBUG", True)))
JIRA_URL = os.environ.get("", "https://jira.vccloud.vn")
JIRA_ADMIN = os.environ.get("JIRA_ADMIN")
JIRA_TOKEN = os.environ.get("JIRA_TOKEN")
DSN = os.environ.get("DSN")
FLASK_RUN_HOST = os.environ.get("FLASK_RUN_HOST", "127.0.0.1")
FLASK_RUN_PORT = os.environ.get("FLASK_RUN_PORT", 8080)
