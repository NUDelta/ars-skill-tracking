from __future__ import print_function
import os
import json

from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
SPREADSHEET_ID = '1ifLpxHEPuxZR7hrEEc3bUjyAS4XKZQ3JogOUCh8q9sc'

store = file.Storage('credentials.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('sheets', 'v4', http=creds.authorize(Http()))

# ~~~~~~~~~~ Grab data from Google Sheets ~~~~~~~~~~
def get_skill_db(RANGE_LIST):
  categories_db = {}
  skill_db = {}

  for sheet in RANGE_LIST:
    result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,
        range=sheet[0]).execute()

    user_values = result.get('values', [])
    value_row = user_values[0]
    categories_db[sheet[1]] = value_row[1:]

    for row in user_values[1:]:
      l = [value_row[i] for i in xrange(len(row)) if (row[i] == 'x')]
      temp_user = skill_db.get(row[0], {})
      temp_user[sheet[1]] = l
      skill_db[row[0]] = temp_user

  return categories_db, skill_db

# ~~~~~~~~~~ Grab data from Google Sheets ~~~~~~~~~~

ranges = [
    ('Design!A1:M29', "design"),
    ('Tech!A1:T29', "tech"),
    ('Research!A1:K29', 'research'),
    ('Other!A1:F29', 'other'),
    ]

categories_db, skill_db = get_skill_db(ranges)
with open('categoriesDb.json', 'w') as outfile:
  json.dump(categories_db, outfile)
with open('skillDb.json', 'w') as outfile:
  json.dump(skill_db, outfile)

