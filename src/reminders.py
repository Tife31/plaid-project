import datetime

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]


def set_reminder(due_date, account_id, amount):
  """Shows basic usage of the Google Calendar API.
  Prints the start and name of the next 10 events on the user's calendar.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("calendar", "v3", credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
    print("Getting the upcoming 10 events")
    events_result = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=now,
            maxResults=10,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = events_result.get("items", [])
    new_datetime = str(datetime.date.today()) + 'T09:00:00-04:00'
    add_event = {
    'summary': 'Sending a reminder about financial commitment',
    'description': 'You have this amount ' + str(amount) + 'due at ' + str(due_date) + 'for this account' + str(account_id),
    'start': {
        'dateTime': new_datetime,
        'timeZone': 'America/Toronto',
    },
    'end': {
        'dateTime': new_datetime,
        'timeZone': 'America/Toronto',
    },
    'attendees': [
        {'email': 'lpage@example.com'},
        {'email': 'sbrin@example.com'},
    ],
    }
    event__insert_result =  service.events().insert(calendarId ='primary', body =add_event).execute()
    print ('Event created: {}' .format(event__insert_result.get('htmlLink')))

    if not events:
      print("No upcoming events found.")
      return

    # Prints the start and name of the next 10 events
    for event in events:
      start = event["start"].get("dateTime", event["start"].get("date"))
      print(start, event["summary"])

  except HttpError as error:
    print(f"An error occurred: {error}")



def send_reminder(due_date, amount):
    """Send a reminder notification."""
    today = datetime.date.today()

    if today == due_date:
        print(f"Reminder: You have a payment of ${amount} due today!")
        # Add code to send email or push notification

def extract_due_dates(transactions):
    """
    Extracts due dates from transaction data.
    
    Args:
        transactions (list): A list of transaction dictionaries.
        
    Returns:
        list: A list of due dates.
    """
    due_dates = []
    
    for transaction in transactions:
        # Example: Extract due dates based on transaction description
        if "payment due" in transaction["name"].lower():
            due_dates.append(transaction["date"])
    
    return due_dates