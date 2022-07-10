from flask import Flask , request
from googleapiclient.discovery import build
from google.oauth2 import service_account
from dotenv import load_dotenv
import os
import json

app = Flask(__name__)

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'google-credentials.json'

creds=None
creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
SAMPLE_SPREADSHEET_ID = '1L6-bSmxrhJcHpHHrZznXL-Zdp2Ju25mAi_CyL4x0SMA'
service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()

def read_sheet():
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,range="Sheet1!A1:C3").execute()
    values = result.get('values', [])
    return values

def insert_row_fer(data_list):
    data = [data_list]
    request = sheet.values().append(spreadsheetId=SAMPLE_SPREADSHEET_ID, range="Recognition!A1:L1",
         valueInputOption="USER_ENTERED", insertDataOption="INSERT_ROWS", body={"values" : data})
    response = request.execute()
    return response

@app.route('/')
def index():
    return "Your App is Working"


@app.route("/getdata")
def get_data():
    res = read_sheet()
    return str(res)


@app.route('/post' ,  methods=['POST'])
def insert_new_row():
    id = request.form['id']
    player_id = request.form['playerId']
    date = request.form['date']
    time = request.form['time']
    age = request.form['age']
    gender = request.form['gender']
    hasAnyDisability = request.form['hasAnyDisability']
    disabilityName = request.form['disabilityName']
    level = request.form['level']
    emotion = request.form['emotion']
    timeTaken = request.form['timeTaken']
    wrongAttempts = request.form['wrongAttempts']
    
    fer_data = [id, player_id , date, time , age , gender , hasAnyDisability , disabilityName , level , emotion , timeTaken , wrongAttempts]
    res = insert_row_fer(fer_data)

    return str(res)

if __name__ == "__main__":
    app.run()
