import arrow
import gspread

from chalicelib import settings

# Must be ordered as they appear in gSheet
SHEET_COLUMNS = [
    "page_size",
    "start_date",
    "count",
    "last_end_date",
    "last_count",
]
SHEET_RANGE = "A2:E2"


class ApiParametersSheet:
    def __init__(self):
        gc = gspread.service_account(filename=settings.SHEETS_CREDENTIALS_FILENAME)
        sh = gc.open_by_key(settings.SHEETS_SPREADSHEET_ID)
        self._worksheet = sh.worksheet(settings.SHEETS_SHEET_TITLE)

    def load(self):
        if hasattr(self, "_parameters"):
            return self._parameters

        parameters = {}
        record = {}
        records = self._worksheet.get_all_records()
        if len(records):
            # We're just interested in the first row of data
            record = records[0]
        page_size = record.get(settings.SHEETS_SHEET_COLUMN_PAGE_SIZE)
        parameters["page_size"] = (
            page_size if page_size else settings.OPENAQ_API_DEFAULT_PAGE_SIZE
        )
        # OpenAQ allows data access via API only up to 2018-01-01
        # see:https://openaq.medium.com/openaq-extends-api-and-download-tool-access-from-90-days-to-2-years-3697540c85a3
        start_date = record.get(settings.SHEETS_SHEET_COLUMN_START_DATE)
        if start_date and start_date.strip():
            parameters["start_date"] = arrow.get(start_date.strip()).isoformat()
        count = record.get(settings.SHEETS_SHEET_COLUMN_COUNT)
        parameters["count"] = count if count else 0
        last_end_date = record.get(settings.SHEETS_SHEET_COLUMN_LAST_END_DATE)
        if last_end_date and last_end_date.strip():
            parameters["last_end_date"] = last_end_date.strip()
        last_count = record.get(settings.SHEETS_SHEET_COLUMN_LAST_COUNT)
        parameters["last_count"] = last_count if last_count else 0
        self._parameters = parameters

        return self._parameters

    def save(self, parameters):
        updated_parameters = {**self._parameters, **parameters}
        updated_values = list(map(lambda x: updated_parameters[x], SHEET_COLUMNS))
        self._worksheet.update(SHEET_RANGE, [updated_values])
