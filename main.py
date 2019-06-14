import os
import time
import requests
import json
import myq

USERNAME = "EMAILID"
PASSWORD = "MyQPASSWIRD"
mq = myq.MyQ(USERNAME,PASSWORD)

def lambda_handler(event, context):
    mq.login()
    mq.get_device_id()
    doorstate = mq.status()
    session = event['session']
    requestId = event['responseId']
    intentName = event['queryResult']['intent']['displayName']
    try:
      userDoorState = event['queryResult']['parameters']['DOOR_STATES']
    except Exception, e:
      userDoorState = "None"
    print ("onSessionStarted Google requestId="+requestId+" , sessionInfo ="+session)
    
    #Google Action Intent Handlers
    if intentName == "StateIntent":
      cardTitle = "Garage Door Status - "+doorstate
      expectUserResponse = False
      
      if userDoorState == "open":
        if doorstate == "open":
          speechText = "Yes, your garage door is currently open."
        elif doorstate == "closed":
          speechText = "No, your garage door is currently closed."
      elif userDoorState == "close":
        if doorstate == "open":
          speechText = "No, your garage door is currently open."
        elif doorstate == "closed":
          speechText = "Yes, your garage door is currently closed."
      else:
        speechText = "Your garage door is currently "+doorstate+"."
    
    elif intentName == "MoveIntent":
      expectUserResponse = False
      
      if userDoorState == "open":
        if doorstate == "open":
          speechText = "Your Garage Door is already open."
          cardTitle = "Open Garage Door"
        elif doorstate == "closed":
          mq.open()
          speechText = "Ok, I'm opening your garage door."
          cardTitle = "Opening Garage Door"
      elif userDoorState == "close":
        if doorstate == "open":
          mq.close()
          speechText = "Ok, I'm closing your garage door."
          cardTitle = "Closing Garage Door"
        elif doorstate == "closed":
          speechText = "Your Garage Door is already closed."
          cardTitle = "Close Garage Door"
      else:
        speechText = "I didn't understand that. You can say ask my garage door to open or close garage door."
        cardTitle = "Open/Close Garage Door - Help"
    else:
      cardTitle = "Help"
      speechText = "You can open or close your garage door by saying, ask my garage door to open. What would you like to do?"
      expectUserResponse = True
      print "Invaild Intent Name ("+intentName+")"

# Response builder
    return (
        {
          "fulfillmentText": speechText,
          "fulfillmentMessages": [
            {
              "card": {
                "title": "MyQ - "+cardTitle,
                "subtitle": "",
                "imageUri": "",
                "buttons": [
                  {
                    "text": "",
                    "postback": ""
                  }
                ]
              }
            }
          ],
          "source": "MyQ.com",
          "payload": {
            "google": {
              "expectUserResponse": expectUserResponse,
              "richResponse": {
                "items": [
                  {
                    "simpleResponse": {
                      "textToSpeech": speechText
                    }
                  }
                ]
              }
            }
          }
        }
    )