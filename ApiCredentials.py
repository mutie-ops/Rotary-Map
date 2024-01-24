from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import os
from requests import Request
from google.auth.transport.requests import Request


SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# Load or create credentials
credentials_file = 'C:\\Users\\HP\\OneDrive\\Desktop\\RotaryScrap\\credentials.json'
credentials = None

# The file token.json stores the user's access and refresh tokens and is created automatically when the authorization
# flow completes for the first time.

token_file = 'C:\\Users\\HP\\OneDrive\\Desktop\\RotaryScrap\\token.json'

if os.path.exists(token_file):
    credentials = Credentials.from_authorized_user_file(token_file)

# If there are no (valid) credentials available, let the user log in.
if not credentials or not credentials.valid:
    if credentials and credentials.expired and credentials.refresh_token:
        credentials.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(credentials_file, SCOPES)
        credentials = flow.run_local_server(port=0)

    # Save the credentials for the next run
    with open(token_file, 'w') as token:
        token.write(credentials.to_json())
