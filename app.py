from flask import Flask , request
from googleapiclient.discovery import build
from google.oauth2 import service_account
from dotenv import load_dotenv



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
    request = sheet.values().append(spreadsheetId=SAMPLE_SPREADSHEET_ID, range="Recognition!A1:T1",
         valueInputOption="USER_ENTERED", insertDataOption="INSERT_ROWS", body={"values" : data})
    response = request.execute()
    return response


def insert_row_fee(data_list):
    data = [data_list]
    request = sheet.values().append(spreadsheetId=SAMPLE_SPREADSHEET_ID, range="Expression!A1:N1",
         valueInputOption="USER_ENTERED", insertDataOption="INSERT_ROWS", body={"values" : data})
    response = request.execute()
    return response

def getAnswersList(givenAnswers):
    givenAnswersList  = givenAnswers.split(",")
    arrlen = len(givenAnswersList)
    returnlist = []
    for i in range(0,4):
        if i<arrlen:
            returnlist.append(givenAnswersList[i])
        else:
            returnlist.append(" ")
    return returnlist

def getAnsweredTimesList(answerGivenTimes):
    answerGivenTimesList = answerGivenTimes.split(",")
    arrlen = len(answerGivenTimesList)
    returnlist = []
    for i in range(0,4):
        if i<arrlen:
            returnlist.append(answerGivenTimesList[i])
        else:
            returnlist.append("0")
    return returnlist


@app.route('/')
def index():
    return "Your App is Working"


@app.route("/getdata")
def get_data():
    res = read_sheet()
    return str(res)

''''
Following API Endpoint will be used to insert the Data gathered while playing the Emotion Recognition Game
Request Body - Form Data
'''
@app.route('/fer' ,  methods=['POST'])
def save_fer():
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
    givenAnswers = request.form['givenAnswers']
    answerGivenTimes = request.form['answerGivenTimes']

    givenAnswersList = getAnswersList(givenAnswers)
    answerGivenTimesList = getAnsweredTimesList(answerGivenTimes)
    
    print("**** - ",givenAnswersList, givenAnswersList[0])

    fer_data = [id, player_id , date, time , age , gender , hasAnyDisability , disabilityName , 
                level , emotion , timeTaken , wrongAttempts,
                givenAnswersList[0], givenAnswersList[1], givenAnswersList[2], givenAnswersList[3],
                answerGivenTimesList[0], answerGivenTimesList[1], answerGivenTimesList[2], answerGivenTimesList[3]]

    res = insert_row_fer(fer_data)

    return str(res)

''''
Following API Endpoint will be used to insert the Data gathered while playing the Emotion Expression Game
Request Body - Form Data
'''
@app.route('/fee' , methods=['POST'])
def save_fee():
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
    arousal = request.form['arousal']
    valence = request.form['valence']

    fee_data = [id, player_id , date, time , age , gender , hasAnyDisability , disabilityName ,
             level , emotion , timeTaken , wrongAttempts, arousal , valence]

    res = insert_row_fee(fee_data)

    return str(res)


if __name__ == "__main__":
    app.run()
