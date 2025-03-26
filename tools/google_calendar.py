import os.path
import pickle
import pytz
from datetime import datetime, timedelta
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from agents import function_tool

SCOPES = ["https://www.googleapis.com/auth/calendar"]

def get_calendar_service():
    creds = None
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    service = build("calendar", "v3", credentials=creds)
    return service

# Example: List upcoming events
def list_events():
    service = get_calendar_service()
    events_result = service.events().list(
        calendarId="primary", maxResults=10, singleEvents=True, orderBy="startTime"
    ).execute()

    events = events_result.get("items", [])

    if not events:
        print("No upcoming events found.")
        return

    for event in events:
        start = event["start"].get("dateTime", event["start"].get("date"))
        print(f"{start} - {event['summary']}")


@function_tool
def get_today_events():
    """Fetch events from Google Calendar for the current day."""
    
    service = get_calendar_service()

    # Get the current date in ISO format
    tz = pytz.timezone("UTC")  # Adjust to your timezone
    now = datetime.now(tz)
    start_of_day = datetime(now.year, now.month, now.day, 0, 0, 0, tzinfo=tz).isoformat()
    end_of_day = datetime(now.year, now.month, now.day, 23, 59, 59, tzinfo=tz).isoformat()

    # Fetch events for today
    events_result = service.events().list(
        calendarId="primary",  # Use "primary" for the main Google Calendar
        timeMin=start_of_day,
        timeMax=end_of_day,
        singleEvents=True,
        orderBy="startTime"
    ).execute()

    events = events_result.get("items", [])

    if not events:
        return "No events found for today."

    return [
        {
            "summary": event.get("summary", "No Title"),
            "start": event["start"].get("dateTime", event["start"].get("date")),
            "end": event["end"].get("dateTime", event["end"].get("date")),
        }
        for event in events
    ]

@function_tool
def get_week_events():
    """Fetch events from Google Calendar starting from today (or next Monday if today is the weekend) and skipping weekends."""
    
    service = get_calendar_service()

    # Set the timezone (adjust based on your needs)
    tz = pytz.timezone("UTC")  # Change to your local timezone if needed

    # Get the current date and time
    now = datetime.now(tz)
    
    # If today is Saturday (5) or Sunday (6), move to next Monday
    if now.weekday() >= 5:
        now += timedelta(days=(7 - now.weekday()))  # Move to next Monday
    
    # Start from the current time onward
    start_time_iso = now.isoformat()
    
    # Find the next Friday (end of workweek)
    days_until_friday = (4 - now.weekday()) if now.weekday() <= 4 else 4
    end_of_week = now + timedelta(days=days_until_friday)
    end_of_week_iso = datetime(end_of_week.year, end_of_week.month, end_of_week.day, 23, 59, 59, tzinfo=tz).isoformat()
    
    # Fetch events starting from now until the next Friday
    events_result = service.events().list(
        calendarId="primary",  # Use "primary" for the main Google Calendar
        timeMin=start_time_iso,
        timeMax=end_of_week_iso,
        singleEvents=True,
        orderBy="startTime"
    ).execute()
    
    events = events_result.get("items", [])
    
    if not events:
        return "No events found for the remaining workweek."

    return [
        {
            "summary": event.get("summary", "No Title"),
            "start": event["start"].get("dateTime", event["start"].get("date")),
            "end": event["end"].get("dateTime", event["end"].get("date")),
        }
        for event in events
    ]

@function_tool
def create_event(start_time: str, end_time: str, user_name: str, user_email: str):
    """
    Creates an event in Google Calendar and conditionally sends an email invitation.

    Args:
        start_time (str): Event start time in 'YYYY-MM-DDTHH:MM:SS' format
        end_time (str): Event end time in 'YYYY-MM-DDTHH:MM:SS' format
        user_name (str): Name of the guest
        user_email (str): Email of the guest
        send_email (bool): If True, sends an email invite to the guest

    Returns:
        str: HTML link to the event
    """

    service = get_calendar_service()

    event = {
        "summary": "Dentist Appointment",
        "start": {"dateTime": start_time, "timeZone": "America/New_York"},
        "end": {"dateTime": end_time, "timeZone": "America/New_York"},
        "attendees": [
            {"email": user_email, "displayName": user_name}
        ],
    }
    
    send_email = False
    # Conditionally send email invites
    send_updates_option = "all" if send_email else "none"

    # Create the event
    created_event = service.events().insert(
        calendarId="primary",
        body=event,
        sendUpdates=send_updates_option  # Only send invites if requested
    ).execute()

    return created_event['htmlLink']

@function_tool
def search_events_by_guest_email(guest_email: str):
    """
    Searches Google Calendar for future events where the given guest email is an attendee.
    
    :param guest_email: The email of the guest to search for.
    :return: List of matching events.
    """
    service = get_calendar_service()
    
    # Set timezone (adjust if needed)
    tz = pytz.timezone("UTC")  # Change to your local timezone if necessary
    now = datetime.now(tz).isoformat()  # Current date-time in ISO format

    events = []
    page_token = None

    while True:
        # Fetch events from the current time onward
        events_result = service.events().list(
            calendarId="primary",  # Change to a different calendar ID if necessary
            timeMin=now,  # Search from the current date-time onward
            singleEvents=True,
            orderBy="startTime",
            pageToken=page_token
        ).execute()

        for event in events_result.get("items", []):
            attendees = event.get("attendees", [])
            
            # Check if the guest email is in the attendees list
            if any(attendee.get("email") == guest_email for attendee in attendees):
                events.append({
                    "summary": event.get("summary", "No Title"),
                    "start": event["start"].get("dateTime", event["start"].get("date")),
                    "end": event["end"].get("dateTime", event["end"].get("date")),
                    "attendees": [att.get("email") for att in attendees if "email" in att]
                })

        page_token = events_result.get("nextPageToken")
        if not page_token:
            break  # Stop if there are no more pages of results

    return events

# Example usage:
# results = search_events_by_guest_email('khizar@email.com')
# print(results)