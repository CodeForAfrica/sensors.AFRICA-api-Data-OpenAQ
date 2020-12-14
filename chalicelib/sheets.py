import gspread

from chalicelib import settings


class ApiParametersSheet:
    def __init__(self):
        gc = gspread.service_account(filename=settings.SHEETS_CREDENTIALS_FILENAME)
        sh = gc.open_by_key(settings.SHEETS_SPREADSHEET_ID)
        self._worksheet = sh.worksheet(settings.SHEETS_SHEET_TITLE)

    def load(self):
        if hasattr(self, "_parameters"):
            return self._parameters

        parameters = {}
        records = self._worksheet.get_all_records()
        if len(records):
            # We're just interested in the first row of data
            record = records[0]
            limit = record.get(settings.SHEETS_SHEET_COLUMN_PAGE_SIZE)
            parameters["limit"] = (
                limit if limit else settings.OPENAQ_API_DEFAULT_PAGE_SIZE
            )
            # OpenAQ allows data access via API only up to 2018-01-01
            # see:https://openaq.medium.com/openaq-extends-api-and-download-tool-access-from-90-days-to-2-years-3697540c85a3
            date_from = record.get(settings.SHEETS_SHEET_COLUMN_START_DATE)
            parameters["date_from"] = (
                date_from if date_from and date_from.strip() else "2018-01-01"
            )
            last_end_date = record.get(settings.SHEETS_SHEET_COLUMN_LAST_END_DATE)
            if last_end_date:
                parameters["date_from"] = last_end_date
            count = record.get(settings.SHEETS_SHEET_COLUMN_COUNT)
            parameters["count"] = count if count else 0
            self._parameters = parameters

        return self._parameters
