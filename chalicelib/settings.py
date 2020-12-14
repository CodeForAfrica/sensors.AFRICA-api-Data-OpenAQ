import os

from dotenv import load_dotenv

load_dotenv()

DEBUG = os.environ.get("DEBUG", "False").lower() in ["true", "1", "t", "y", "yes"]

SENTRY_DSN = os.environ["SENTRY_DSN"]

# Everyday hour,
SCHEDULE_RATE = os.environ.get("SCHEDULE_RATE", "rate(1 hour)")

SENSORSAFRICA_API_URL = os.environ.get(
    "SENSORSAFRICA_API_URL", "https://api.sensors.africa/v2"
)
SENSORSAFRICA_API_AUTHORIZATION_TOKEN = os.environ[
    "SENSORSAFRICA_API_AUTHORIZATION_TOKEN"
]

SHEETS_CREDENTIALS_FILENAME = os.environ.get(
    "SHEETS_CREDENTIALS_FILENAME", "chalicelib/credentials.json"
)
SHEETS_SPREADSHEET_ID = os.environ["SHEETS_SPREADSHEET_ID"]
SHEETS_SHEET_TITLE = os.environ["SHEETS_SHEET_TITLE"]
SHEETS_SHEET_COLUMN_PAGE_SIZE = os.environ.get(
    "SHEETS_SHEET_COLUMN_PAGE_SIZE", "pageSize"
)
SHEETS_SHEET_COLUMN_START_DATE = os.environ.get(
    "SHEETS_SHEET_COLUMN_START_DATE", "startDate"
)
SHEETS_SHEET_COLUMN_COUNT = os.environ.get("SHEETS_SHEET_COLUMN_COUNT", "count")
SHEETS_SHEET_COLUMN_LAST_END_DATE = os.environ.get(
    "SHEETS_SHEET_COLUMN_LAST_END_DATE", "lastEndDate"
)
SHEETS_SHEET_COLUMN_LAST_COUNT = os.environ.get(
    "SHEETS_SHEET_COLUMN_LAST_COUNT", "lastCount"
)

OPENAQ_API_URL = os.environ["OPENAQ_API_URL"]
OPENAQ_API_COUNTRIES = os.environ.get("OPENAQ_API_COUNTRIES", "KE,NG,ZA")
OPENAQ_API_PARAMETERS = os.environ.get("OPENAQ_API_PARAMETERS", "pm25,pm10")
OPENAQ_API_DEFAULT_PAGE_SIZE = int(
    os.environ.get("OPENAQ_API_DEFAULT_PAGE_SIZE", "1000"), 10
)
