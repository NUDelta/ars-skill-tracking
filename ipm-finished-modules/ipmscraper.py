from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pdb

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms'
SAMPLE_RANGE_NAME = 'IPM!B2:H117'

helper_names = ["Maxine",
"Cooper",
"Caryl",
"Shankar",
"Josh",
"Kapil",
"Gobi",
"Ryan L",
"Leesha",
"Yongsung",
"Salome",
"Abizar",
"Harrison",
"Olivia",
"Zev",
"Nina",
"Amy",
"Mary",
"David",
"Vishal",
"Garret"]

all_ipm_sheets = [
"https://docs.google.com/spreadsheets/d/1bec84SS8HLfCJwGoYRpBH2_Wtks1dKQpm43p2FtNdEs/edit#gid=0",
"https://docs.google.com/spreadsheets/d/17DyrbWEBsjfPGVhOVKRGyGI6LjVCE4Zzg56MSlPUvoA/edit#gid=0",
"https://docs.google.com/spreadsheets/d/1cO_GCGCTPV_SCK2auuyBMoj-GRvH_Rrl3BijwbATO4Y/edit#gid=0",
"https://docs.google.com/spreadsheets/d/18ansNiBgtx4nl9eUaFiMsxM02IAWG0kYPPO6vn13R-E/edit#gid=0",
"https://docs.google.com/spreadsheets/d/1E7UwRlzNdbGsIGU6WcMuHI77R6JXO14eZcPm36eOL1Y/edit#gid=0",
"https://docs.google.com/spreadsheets/d/1xEJ3dDYqNA9SlufiD3GF4mN3DzvXg_JMc3D25rUjSHA/edit#gid=0",
"https://docs.google.com/spreadsheets/d/1oIVc3kVQPe8fYXJc8fVqxSZxRfJg7DZjjhcEcY5jDVw/edit#gid=0",
"https://docs.google.com/spreadsheets/d/1anytwho_bmYbAAPOkURNJsYsGajRrgG5kM8tbJZ1O90/edit#gid=0",
"https://docs.google.com/spreadsheets/d/1hqscLbWvQknikhcLaSKfQF06KTOEpJabVv8oDMlRQFQ/edit#gid=0",
"https://docs.google.com/spreadsheets/d/15xgQc4kQa9jEVguF-NtlCCshk74wfN1Eyp8ads6dRVw/edit#gid=0",
"https://docs.google.com/spreadsheets/d/1Kpf9ZAjmUKHk6cVeeJh7ve46LdBdOM3QtCz2pgqY1M4/edit#gid=0",
"https://docs.google.com/spreadsheets/d/1qJAJQv2trxYm-aWrgRJL6cmIfIWSC6-otMe3WQmv9AU/edit#gid=0",
"https://docs.google.com/spreadsheets/d/1tZZUUFli_atZneUTAiEjPTZryZnc_Q03Kn1JBqMpUJw/edit#gid=0",
"https://docs.google.com/spreadsheets/d/12FGZ-vp9KUt3IkdcZcUoeKuF5yB9K0z75BUZETLql_o/edit#gid=0",
"https://docs.google.com/spreadsheets/u/1/d/1xCTWPbClyRUcZX9x6v45fZsP_ruUwlhp7PEIIl0JtAM/edit#gid=0",
"https://docs.google.com/spreadsheets/d/1MimE-Uen0h3yy8cE3IDNF-hdHUQKM2ujl6gVvret6lI/edit#gid=0",
"https://docs.google.com/spreadsheets/d/19ROmPe5PGW5cekvPPW1ukcGv_OxXdFXKod_-1rXPgWE/edit#gid=0",
"https://docs.google.com/spreadsheets/d/1aDPIOO-KkxfdMpMSpD-3GGNa2TVy2UM_r4hzaldTqXQ/edit#gid=0",
"https://docs.google.com/spreadsheets/d/1MXfe7PyjXz7x0WUEFGVrHlC54t7Z6yfYx_lLg8t2SgE/edit#gid=0",
"https://docs.google.com/spreadsheets/d/1SrIUxtBLQKViZfEdU80CJYQ_wfz-bETGeJnF_SeFWA4/edit#gid=0",
"https://docs.google.com/spreadsheets/d/1uUtA2ibs_FRNw7ubJl-5J76jiL4s5nsk98iZtG3slhA/edit#gid=0"]

for i in range(len(all_ipm_sheets)):
    all_ipm_sheets[i] = all_ipm_sheets[i].split('/')[-2]

def check_if_valid_module(row):
    if row and ('y' in row[-1].lower() or 'x' in row[-1].lower() or 'y' in row[-2].lower() or 'x' in row[-2].lower()):
        return True
    return False

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
    res_json = {}
    for i in range(len(all_ipm_sheets)):
        # res_json[helper_names[i]] = []
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=all_ipm_sheets[i],
                                    range=SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])
        print("checking " + helper_names[i])
        if values:
            for row in values:
                if len(row)>=5:
                    if unicode(row[0]) in res_json:
                        res_json[unicode(row[0])] += ", " + helper_names[i]
                    else:
                        res_json[unicode(row[0])] = helper_names[i]
                    # res_json[helper_names[i]].append(unicode(row[0]))
        if not values:
            print('No data found.')

    with open('modules.csv', 'w') as f:
        for key in res_json:
            # val = ' '.join(res_json[key])
            f.write("%s, %s\n"%(key, res_json[key]))

if __name__ == '__main__':
    main()
