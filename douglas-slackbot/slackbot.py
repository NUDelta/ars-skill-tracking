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

RANGE_NAME = 'Blocker Setup!A2:E29'
result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,
                                             range=RANGE_NAME).execute()
user_values = result.get('values', [])

RANGE_NAME = 'P - People and Ways!A2:O29'
result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,
                                             range=RANGE_NAME).execute()
blocker_values = result.get('values', [])

user_list = ["sehmonburnam"]
sehmon_id = 'U3EHRC9DJ'
auth_token = os.environ["SLACK_BOT_TOKEN"]
client_id = "704780367654-ljc3kaq0eu58le5l65hibmkbojj1u54q.apps.googleusercontent.com"
slack_client = SlackClient(auth_token)

for i in xrange(len(user_values)):
  if(len(blocker_values[i]) >= 3) and (len(user_values[i]) >= 4):
    if(blocker_values[i][2]) and (blocker_values[i][2] != '#N/A'):
      blocker_string = "{}'s blocker for the week is: {}".format(user_values[i][4], blocker_values[i][2])
      res = slack_client.api_call(
          'chat.postMessage',
          channel=sehmon_id,
          text=blocker_string,
          as_user=True,
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