# ==========================
# sheets_service.py
# Google Sheets操作モジュール（open_by_key版）
# ==========================

import gspread
from oauth2client.service_account import ServiceAccountCredentials

# 【ここにシートIDを正確に貼り付けてください！】
SHEET_ID = '1VS-KBh13nRPymYOaaswUpFwDtJqWHTq9wRFp-hswhTU'

def get_worksheet():
    CREDENTIALS_FILE = 'credentials.json'
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, scope)
    client = gspread.authorize(creds)

    # シートIDで直接開く
    spreadsheet = client.open_by_key(SHEET_ID)
    worksheet = spreadsheet.sheet1
    return worksheet

def append_signal(signal_type, symbol, price):
    """
    シグナル情報をGoogle Sheetsに追加する
    :param signal_type: 'entry' or 'exit'
    :param symbol: 銘柄シンボル
    :param price: 取引価格
    """
    worksheet = get_worksheet()

    from datetime import datetime
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")

    row = [date_str, time_str, signal_type, symbol, price]
    worksheet.append_row(row)