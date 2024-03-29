from flask import Flask , request
from googleapiclient.discovery import build
from google.oauth2 import service_account
from dotenv import load_dotenv
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
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,range="Analysis!A1:D22").execute()
    values = result.get('values', [])
    return values

def read_EmoLevelPi():
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,range="EmoLevelPi!A1:B4").execute()
    values = result.get('values', [])
    return values

def read_VisibilityPercentage():
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,range="VisibilityPercentage!A1:B8").execute()
    values = result.get('values', [])
    return values

#AULabel
def read_AULabel():
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,range="AULabel!A1:B15").execute()
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
    request = sheet.values().append(spreadsheetId=SAMPLE_SPREADSHEET_ID, range="Expression!A1:Q1",
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


#A Function to Read the Analysis Results
def get_analysis_results():
    res_array = read_sheet()
    #key_arr = res_array[0]

    return_dic = {
        'timestamp': [],
        'Emotion Level':[],
        'Valence':[],
        'Arousal':[]
    }

    for i in range(1, len(res_array)):
        arr = res_array[i]
        return_dic['timestamp'].append(arr[0])
        return_dic['Emotion Level'].append(arr[1])
        return_dic['Valence'].append(arr[2])
        return_dic['Arousal'].append(arr[3])
    
    return return_dic


def get_EmoLevelPi():
    res_array = read_EmoLevelPi()
    return_dic = {
        'Emotion Level':[],
        'Percentage':[]
    }

    for i in range(1, len(res_array)):
        arr = res_array[i]
        return_dic['Emotion Level'].append(arr[0])
        return_dic['Percentage'].append(float(arr[1]))
      
    return return_dic

def get_VisibilityPercentage():
    res_array = read_VisibilityPercentage()
    return_dic = {
        'Emotion':[],
        'VisibilityPercentage':[]
    }

    for i in range(1, len(res_array)):
        arr = res_array[i]
        return_dic['Emotion'].append(arr[0])
        return_dic['VisibilityPercentage'].append(int(arr[1]))

    return return_dic

def get_AULabel():
    res_array = read_AULabel()
    return_dic = {
        'AULabel':[],
        'Activation':[]
    }

    for i in range(1, len(res_array)):
        arr = res_array[i]
        return_dic['AULabel'].append(arr[0])
        return_dic['Activation'].append(int(arr[1]))

    return return_dic





@app.route('/')
def index():
    return "Your App is Working"


@app.route("/getdata")
def get_data():
    res = get_analysis_results()
    jsonStr = json.dumps(res)
    return {"result" : jsonStr}

@app.route("/EmoLevelPi")
def get_emotion_level_pi_data():
    res = get_EmoLevelPi()
    jsonStr = json.dumps(res)
    return {"result" : jsonStr}


@app.route("/VisibilityPercentage")
def get_VisibilityPercen():
    res = get_VisibilityPercentage()
    jsonStr = json.dumps(res)
    return {"result" : jsonStr}

#AULabel
@app.route("/AULabel")
def get_Labels_Au():
    res = get_AULabel()
    jsonStr = json.dumps(res)
    return {"result" : jsonStr}



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
    expectEdemotion = request.form['expectEdemotion']
    expressedEmotion = request.form['expressedEmotion'] 
    startTime = request.form['startTime'] 
    endTime = request.form['endTime'] 
    timeTaken = request.form['timeTaken']
    arousal = request.form['arousal']
    valence = request.form['valence']
    emotionLevel = request.form['emotionLevel']

    fee_data = [id, player_id , date, time , age , gender , hasAnyDisability , disabilityName ,
             level , expectEdemotion ,expressedEmotion, startTime, endTime, timeTaken , arousal , valence , emotionLevel]

    res = insert_row_fee(fee_data)

    return str(res)


if __name__ == "__main__":
    app.run()
