import json
from bs4 import BeautifulSoup
from twill.commands import *
import json
import os
import twill
import boto3
def lambda_handler(event, context):
    
    if event['request']['type'] == "IntentRequest":
       return on_intent(event['request'], event['session']);
    return 'Hello from Lambda'

def on_intent(intent_request, session):
#  print("on_intent requestId=" + intent_request['requestId'] +
#    ", sessionId=" + session['sessionId'])

  intent = intent_request['intent']
  intent_name = intent_request['intent']['name']
  if intent_name == "CheckGrades":
    return check_grades(intent, session)
  else:
    raise ValueError("Invalid intent")

def check_grades(intent, session):
    session_attributes={}
    student = intent['slots']['student']['value'].lower()
    card_title="Check grades for %s" % (student)
    username=""
    password=""
    f = open(os.devnull,"w")
    twill.set_output(f)
    go('https://apps.gwinnett.k12.ga.us/dca/app/logout')
    go('https://publish.gwinnett.k12.ga.us/gcps/home/gcpslogin')
    fv("2", "portalUserID", username)
    fv("2", "portalPassword", password)
    submit()
    go('https://apps.gwinnett.k12.ga.us/dca/student/dashboard')
    soup = BeautifulSoup(show(),"lxml")
    subjects = soup.findAll('span', { "class": "subject" })
    percentages = soup.findAll('span', { "class": ["percentage","lettergrade"] })
    grades={}   
    i = 0
    for subject in subjects:
       if (percentages[i].contents):
          grades[subject.renderContents()] = percentages[i].renderContents()
       i = i + 1
    go('https://apps.gwinnett.k12.ga.us/dca/app/logout')
