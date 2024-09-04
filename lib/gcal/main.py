import os
import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# Define the scopes for the Google Calendar API
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def get_calendar_events():
    """Retrieves the next 10 events from the user's Google Calendar."""
    creds = None
    token_path = os.path.join(os.path.dirname(__file__), 'token.json')
    credentials_path = os.path.join(os.path.dirname(__file__), 'credentials.json')

    # Load the credentials from the token.json file
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    # If no valid credentials are found, log the user in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_path, 'w') as token_file:
            token_file.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API to fetch events
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        print('Getting the upcoming 10 events')
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                              maxResults=10, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
            return []
        else:
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                print(f"{start}: {event['summary']}")
            return events

    except Exception as error:
        print(f'An error occurred: {error}')
        return []

if __name__ == '__main__':
    get_calendar_events()
