import random

from google.oauth2 import service_account
from googleapiclient.discovery import build

from core.config import GOOGLE_SHEETS_ID


SERVICE_ACCOUNT_FILE = 'service_account.json'
credentials = service_account.Credentials.from_service_account_file(
    filename=SERVICE_ACCOUNT_FILE
)

class GoogleSheetAPI:
    def __init__(self):
        self._service_sheets = build('sheets', 'v4', credentials=credentials)
        self._sheet_id = GOOGLE_SHEETS_ID
    
    def _read_column(self, sheet):
        data = (
            self._service_sheets.spreadsheets().values()
            .get(spreadsheetId=self._sheet_id, range=sheet + '!' + 'A:A')
        ).execute()
        if 'values' in data:
            cleaned_data = [i[0] for i in data['values']]
            return cleaned_data
    
    def get_random_value_from_sheet(self, sheet):
        data = self._read_column(sheet)
        if data:
            random_item =random.choice(data)
            return random_item


if __name__ == '__main__':
    google_sheet = GoogleSheetAPI()
    column_data = google_sheet._read_column('Group1')
    random_item = google_sheet.get_random_value_from_sheet('Group1')
    print(column_data, random_item)
    