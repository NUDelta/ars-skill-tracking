from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pdb
import json

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms'
SAMPLE_RANGE_NAME = 'Canvas Summary!A1:BJ10'

helper_names = """Maxine
Cooper
Caryl
Shankar
Josh
Kapil
Gobi
Ryan L
Leesha
Salome
Abizar
Harrison
Olivia
Zev
Nina
Amy
Mary
David
Vishal"""

helper_names = helper_names.split('\n')

all_ipm_sheets = """https://docs.google.com/spreadsheets/d/1VO8azPPWtGqFJKGFvZEUnYQ5-UMKSLcsf9YXoydH8m0/edit#gid=288134260
https://docs.google.com/spreadsheets/d/1UCEAn-PGd2zOGDpcbTrkbyDK6tL2_KkzysM5uQkcewE/edit#gid=86492355
https://docs.google.com/spreadsheets/d/1kiQKCjSSrFIhoIHakEO6k_FMDPaUrsMn1HEnfur5faQ/edit
https://docs.google.com/spreadsheets/d/1qVnVspN-1iVcISsyolkSywiuK0SjSvskxFZdE4SvJaU/edit
https://docs.google.com/spreadsheets/d/1kiQKCjSSrFIhoIHakEO6k_FMDPaUrsMn1HEnfur5faQ/edit
https://docs.google.com/spreadsheets/d/1wDWcmQ06Ir5d3nRuM-v7TavdrNuuUkPzrRApQ0xhIF8/edit#gid=1376751709
https://docs.google.com/spreadsheets/d/1_O1qhO9muiFK1YsU5w4_fcA4WjrpCvgjQ3fmmr5jueQ/edit
https://docs.google.com/spreadsheets/d/1lmpdK9cCOWNC12uYrac3IO4H5PsIyqjays2cIBKGhZs/edit#gid=1149902915
https://docs.google.com/spreadsheets/d/1mwW376vxrp7KUbWI8bcsleW9uA5tkfWDl2cQYQaPjUk/edit#gid=1912796421
https://docs.google.com/spreadsheets/d/1VQ5lHtNmz20d1H3V_s9XCVjRQP6UlFIAMLYPn-SBEIM/edit#gid=1212308561
https://docs.google.com/spreadsheets/d/1rMC4mjExeumnPE80inPbxbahANlxmyEmBsG6i_2ZJsI/edit#gid=2093086477
https://docs.google.com/spreadsheets/d/1mazre24O1nqvQlhDBE9k99za3Z4gaGDXu5Bu2Qs_vt0/edit#gid=913011565
https://docs.google.com/spreadsheets/d/1MbFsifXBCZYVAYuidRf53YdAB_4WLT_WjvAts9ah8go/edit#gid=7285913
https://docs.google.com/spreadsheets/d/1MbFsifXBCZYVAYuidRf53YdAB_4WLT_WjvAts9ah8go/edit#gid=7285913
https://docs.google.com/spreadsheets/d/17hX5RsIaMQ1JA-rM0k0Jl6hZxCFk-KYvfTyxbD97pLk/edit#gid=979289651
https://docs.google.com/spreadsheets/d/1bJ4FILD5JWjirh9ct6a6V8VY-rNDwm0Ptndu6E7G6BQ/edit#gid=904227030
https://docs.google.com/spreadsheets/d/1bJ4FILD5JWjirh9ct6a6V8VY-rNDwm0Ptndu6E7G6BQ/edit#gid=904227030
https://docs.google.com/spreadsheets/d/17hX5RsIaMQ1JA-rM0k0Jl6hZxCFk-KYvfTyxbD97pLk/edit#gid=979289651
https://docs.google.com/spreadsheets/d/1AC186ZQA7q0QDtbFj_6ZH-z7iy3TfmbTKOY_LQ0I7rs/edit"""

all_ipm_sheets = all_ipm_sheets.split('\n')

for i in range(len(all_ipm_sheets)):
    all_ipm_sheets[i] = all_ipm_sheets[i].split('/')[-2]

def getCompletedSections(values):
    # pdb.set_trace()
    section = {}
    rows = len(values)
    j = 0
    while(j < 62):
        cur_section = ""
        for i in range(rows):
            try:
                if i == 0 and j >= 61:
                    break
                if i in [6,7,8,9] and j >= 58:
                    break
                if i == 0 and unicode(values[i][j]):
                    cur_section = unicode(values[i][j])
                    section[unicode(values[i][j])] = []
                    continue
                if unicode(values[i][j]) and unicode(values[i][j]) != "Prompt" and unicode(values[i][j]) != "Status":
                    section[cur_section].append({"prompt": unicode(values[i][j]), "status": unicode(values[i][j+1])})
                    continue
            except:
                pdb.set_trace()
                print(values[i][len(values[i])-1])
                raise Exception("at row",i,"and col",j)
        j += 4

    # pdb.set_trace()
    return section




def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    res_json = []
    for i in range(len(all_ipm_sheets)):
        cur_row = {}
        sheet = service.spreadsheets()
        print("Looking at "+helper_names[i])
        result = sheet.values().get(spreadsheetId=all_ipm_sheets[i],
                                    range=SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])
        cur_row["sections"] = [getCompletedSections(values)]
        cur_row["name"] = helper_names[i]
        res_json.append(cur_row)
        # if values:
        #     for row in values:
        #         if len(row)>=5:
        #             res_json[helper_names[i]].append(unicode(row[0]))
        # if not values:
        #     print('No data found.')

    # pdb.set_trace()
    with open('canvasSections.json', 'w') as f:
        json.dump(res_json, f)
    print("fin.")
    # with open('canvasSections.csv', 'w') as f:
    #     for key in res_json:
    #         val = ' '.join(res_json[key])
    #         f.write("%s, %s\n"%(key, val))

if __name__ == '__main__':
    main()
