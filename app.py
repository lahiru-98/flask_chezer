from flask import Flask
from googleapiclient.discovery import build
from google.oauth2 import service_account
from dotenv import load_dotenv
import os
import json

app = Flask(__name__)


SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'google-credentials.json'

creds=None
#creds = Credentials.fr(create_keyfile_dict(), scopes=SCOPES)

creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)


SAMPLE_SPREADSHEET_ID = '1L6-bSmxrhJcHpHHrZznXL-Zdp2Ju25mAi_CyL4x0SMA'

service = build('sheets', 'v4', credentials=creds)
# Call the Sheets API
sheet = service.spreadsheets()

def read_sheet():
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,range="Sheet1!A1:C3").execute()
    values = result.get('values', [])
    return values


@app.route('/')
def index():
    return "Your App is Working"


@app.route("/getdata")
def get_data():
    res = read_sheet()
    return str(res)


if __name__ == "__main__":
    app.run()
