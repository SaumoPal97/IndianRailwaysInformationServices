#Railway API - http://railwayapi.com/api/

from flask import Flask
from flask_ask import Ask, statement, question, session

import json
import requests
import time
import unidecode
import datetime

app = Flask(__name__)
ask = Ask(app, "/train_route") 
api_key = '6dg3lgmg'

def date_convert(date):
    year1 =  datetime.datetime.strptime(date, '%Y-%m-%d').year
    month1 =  datetime.datetime.strptime(date, '%Y-%m-%d').month
    day1 =  datetime.datetime.strptime(date, '%Y-%m-%d').day
    newdata1 = " "
    if (month1<10):
        newdate1 = retstr =  "{}0{}{}".format(year1, month1, day1)
    else:
        newdata1 =  "{}{}{}".format(year1, month1, day1)
    return newdate1

def get_live_train_status(trainnumber, doj):
    r = requests.get("http://api.railwayapi.com/live/train/{}/doj/{}/apikey/{}/".format(trainnumber,doj,api_key))
    try:
        data = json.loads(r.content.decode('utf-8'))
        if (data['response_code']==200):    
            return data['position']
        elif (data['response_code']==510):
            return "Train not scheduled to run on the given date"
        elif (data['response_code']==204):
            return "Empty response. Not able to fetch required data"
        else:
            return "Sorry, services not available at this moment"
    except Exception:
        return "Servers are busy"

def get_train_route(trainnumber): 
    cities = []
    r = requests.get('http://api.railwayapi.com/route/train/{}/apikey/{}/'.format(trainnumber, api_key))
    try:
        data = json.loads(r.content.decode('utf-8'))
        if (data['response_code']==200):    
            for listing in data['route']:
                cities.append(listing['fullname'])
            cities = "...then...".join(l for l in cities)
            cities =  "The train goes through..." + cities
            return cities
        elif (data['response_code']==204):
            return "Empty response. Not able to fetch required data"
        else:
            return "Sorry, services not available at this moment"
    except Exception:
        return "Servers are busy"

def get_train_number(trainname):
    r = requests.get("http://api.railwayapi.com/name_number/train/{}/apikey/{}/".format(trainname, api_key))
    try:
        data = json.loads(r.content.decode('utf-8'))
        if (data['response_code']==200):    
            info1 = "Train number for..." + data['name'] + "...is..." + data['number']
            return info1
        elif (data['response_code']==204):
            return "Empty response. Not able to fetch required data"
        else:
            return "Sorry, services not available at this moment"
    except Exception:
        return "Servers are busy"
  
@app.route('/')
def homepage():
    return 'Hello World'

@ask.launch
def start_skill():
    welcome = 'Welcome to Indian Railways Information Services...You can know about train routes and live train status...For live train status, say train status for train number followed by number on followed by date of journey...For train route, say check route for train number followed by number...For getting train number for a train name, say get train number for followed by train name...'
    return question(welcome)

@ask.intent("LiveTrainStatusIntent")
def share_live_train_status(trainnumber,doj):
    return statement(get_live_train_status(trainnumber, date_convert(doj)))

@ask.intent("TrainRouteIntent")
def share_train_route(trainnumber):
    return statement(get_train_route(trainnumber))

@ask.intent("GetTrainNumberIntent")
def share_train_number(trainname):
    return statement(get_train_number(trainname))

@ask.intent('AMAZON.HelpIntent')
def help():
    help_text = render_template('For live train status, say train status for train number followed by number on followed by date of journey...For train route, say check route for train number followed by number...For getting train number for a train name, say get train number for followed by train name...')
    return question(help_text).reprompt(help_text)


@ask.intent('AMAZON.StopIntent')
def stop():
    bye_text = render_template('bye')
    return statement(bye_text)


@ask.intent('AMAZON.CancelIntent')
def cancel():
    bye_text = render_template('bye')
    return statement(bye_text)

if __name__ == '__main__':
    app.run(debug=True)


