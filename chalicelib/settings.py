import os

from dotenv import load_dotenv

load_dotenv()

DEBUG = os.environ.get("DEBUG", "False").lower() in ["true", "1", "t", "y", "yes"]

SENTRY_DSN = os.environ["SENTRY_DSN"]

# Everyday day,
SCHEDULE_RATE = os.environ.get("SCHEDULE_RATE", "rate(1 day)")

SENSORSAFRICA_API_URL = os.environ.get(
    "SENSORSAFRICA_API_URL", "https://api.sensors.africa/v2"
)
# In milliseconds
SENSORSAFRICA_API_DELAY = int(os.environ.get("SENSORSAFRICA_API_DELAY", "100"), 10)
SENSORSAFRICA_API_AUTHORIZATION_TOKEN = os.environ[
    "SENSORSAFRICA_API_AUTHORIZATION_TOKEN"
]
SENSORSAFRICA_API_OWNER_ID = int(os.environ["SENSORSAFRICA_API_OWNER_ID"], 10)
# https://github.com/opendata-stuttgart/feinstaub-api/blob/1ea02fddb335325d06750544a6198ba753b3bb4d/feinstaub/sensors/models.py#L79
SENSORSAFRICA_API_PARAMETER_MAPPING = {
    "pm1": "P0",
    "pm10": "P1",
    "pm25": "P2",
}

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
OPENAQ_API_COUNTRIES = os.environ.get("OPENAQ_API_COUNTRIES", "KE,NG,TZ,UG,ZA")
OPENAQ_API_PARAMETERS = os.environ.get("OPENAQ_API_PARAMETERS", "pm25,pm10")
OPENAQ_API_DEFAULT_PAGE_SIZE = int(
    os.environ.get("OPENAQ_API_DEFAULT_PAGE_SIZE", "1000"), 10
)

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
OPENAQ_API_COUNTRIES = os.environ.get("OPENAQ_API_COUNTRIES", "KE,NG,TZ,UG,ZA")
OPENAQ_API_PARAMETERS = os.environ.get("OPENAQ_API_PARAMETERS", "pm25,pm10")
# Assuming each measurement parameter is on a different node/sensor pin
OPENAQ_API_PARAMETERS_PIN_MAPPING = {
    "pm25": "1",
    "pm10": "2",
}
OPENAQ_API_DEFAULT_PAGE_SIZE = int(
    os.environ.get("OPENAQ_API_DEFAULT_PAGE_SIZE", "1000"), 10
)
