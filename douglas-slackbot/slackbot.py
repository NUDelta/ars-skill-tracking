from __future__ import print_function
import os
import json
from slackclient import SlackClient

from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
SPREADSHEET_ID = '1uF8K1LMLqv-El1_41j8u029bTFuC4x1WAyMbpBJC8DU'

store = file.Storage('credentials.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('sheets', 'v4', http=creds.authorize(Http()))

# ~~~~~~~~~~ Grab data from Google Sheets ~~~~~~~~~~

# Get list of users and their slack_id
RANGE_NAME = 'Blocker Setup!A2:E29'
result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,
    range=RANGE_NAME).execute()
user_values = result.get('values', [])

# Get list of users and their blockers
RANGE_NAME = 'P - People and Ways!A2:O29'
result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,
    range=RANGE_NAME).execute()
blocker_values = result.get('values', [])

# Get list of people and how many times they were requested for help
RANGE_NAME = 'P - People and Ways!A33:E60'
result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,
    range=RANGE_NAME).execute()
people_request_values = result.get('values', [])

# Get list of 'places to resolve blocker' and how many times they were requested
RANGE_NAME = 'P - People and Ways!G33:L41'
result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,
    range=RANGE_NAME).execute()
place_request_values = result.get('values', [])


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Grab the list of overrequested people (4 or more requests)
over_requested_people = []
for row in people_request_values:
  if (int(row[2]) + int(row[4])) >= 4:
    over_requested_people.append(row[0])

# Grab the list of overrequested places (10 or more requests)
over_requested_places = []
for row in place_request_values:
  if (int(row[3]) + int(row[5])) >= 10:
    over_requested_places.append(row[0])

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



user_list = ["sehmonburnam"]
sehmon_id = 'U3EHRC9DJ'
auth_token = os.environ["SLACK_BOT_TOKEN"]
client_id = "704780367654-ljc3kaq0eu58le5l65hibmkbojj1u54q.apps.googleusercontent.com"
slack_client = SlackClient(auth_token)


blocker_string = "Hey {}! In studio you said your biggest blocker for the week was '{}', are you still having trouble? If so, check back to The Weekly to find someone who can help!".format(user_values[0][0], blocker_values[0][2])
res = slack_client.api_call(
    'chat.postMessage',
    channel=sehmon_id,
    text=blocker_string,
    username='Douglas Reminder'
    )


def sendAll():
  for i in xrange(len(user_values)):
    if(len(blocker_values[i]) >= 3) and (len(user_values[i]) >= 4):
      if(blocker_values[i][2]) and (blocker_values[i][2] != '#N/A'):
        blocker_string = "Hey {}, I'm Douglas: a bot here to help you make progress on your project! In studio you said your biggest blocker for the week was '{}', are you still having trouble? If so, check back to The Weekly to find someone who can help!".format(user_values[i][0], blocker_values[i][2])
        user_id = user_values[i][4]
        res = slack_client.api_call(
            'chat.postMessage',
            channel=user_id,
            text=blocker_string,
            as_user=True,
            username='Douglas Reminder'
            )


# api_call = slack_client.api_call('users.list')
# if api_call.get('ok'):
#   users = api_call.get('members')
#   for user in users:
#     print("{}'s id = {}".format(user.get('name'), user.get('id')))


# for user in user_list:
#   res = slack_client.api_call(
#       'chat.postMessage',
#       channel=user_channel,
#       text="When do you have Sig?",
#       as_user=True,
#       attachments = sample_message['attachments']
#       )

# dm_history = slack_client.api_call('im.list')
# dms = {}
# for dm in dm_history['ims']:
#   dms[dm['user']] = dm['id']

# for user_id, dm_id in dms.iteritems():
#   conversation =  slack_client.api_call(
#       'conversations.history',
#       channel=dm_id,
#       )
#   if conversation['messages']:
#     print "Message history for {}".format(user_id)
#     for message in conversation['messages']:
#       print message['text']