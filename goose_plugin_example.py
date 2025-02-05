import os
import json
import datetime
from typing import Any, Dict, List, Optional
from pathlib import Path
from datetime import datetime, timedelta
import pytz

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from dateutil.parser import parse
from goose.api.extension import Extension, Tool

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly',
          'https://www.googleapis.com/auth/calendar.events',
          'https://www.googleapis.com/auth/calendar.freebusy']

class CalendarExtension(Extension):
    """A Google Calendar integration for Goose."""

    def __init__(self) -> None:
        super().__init__()
        self.name = "calendar"
        self.description = "Google Calendar integration for Goose"
        self._service = None
        self._setup_credentials()

    def _setup_credentials(self) -> None:
        """Set up Google Calendar credentials."""
        creds = None
        # Token file stores the user's access and refresh tokens
        token_path = Path.home() / '.config' / 'goose' / 'calendar' / 'token.json'
        credentials_path = Path.home() / '.config' / 'goose' / 'calendar' / 'credentials.json'

        # Ensure directory exists
        token_path.parent.mkdir(parents=True, exist_ok=True)

        if token_path.exists():
            creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not credentials_path.exists():
                    raise FileNotFoundError(
                        "credentials.json not found. Please place your Google Calendar API credentials in "
                        f"{credentials_path}"
                    )
                flow = InstalledAppFlow.from_client_secrets_file(str(credentials_path), SCOPES)
                creds = flow.run_local_server(port=0)
            
            # Save the credentials for the next run
            with open(token_path, 'w') as token:
                token.write(creds.to_json())

        self._service = build('calendar', 'v3', credentials=creds)

    def get_tools(self) -> List[Tool]:
        """Return the list of tools provided by this extension."""
        return [
            Tool(
                name="list_upcoming_events",
                description="List upcoming calendar events",
                function=self.list_upcoming_events,
                parameters={
                    "type": "object",
                    "properties": {
                        "max_results": {
                            "type": "integer",
                            "description": "Maximum number of events to return",
                            "default": 10
                        }
                    }
                }
            ),
            Tool(
                name="create_event",
                description="Create a new calendar event",
                function=self.create_event,
                parameters={
                    "type": "object",
                    "properties": {
                        "summary": {
                            "type": "string",
                            "description": "Title of the event"
                        },
                        "start_time": {
                            "type": "string",
                            "description": "Start time in ISO format or natural language (e.g., '2023-12-25T10:00:00' or 'tomorrow at 3pm')"
                        },
                        "duration_minutes": {
                            "type": "integer",
                            "description": "Duration of the event in minutes",
                            "default": 60
                        },
                        "description": {
                            "type": "string",
                            "description": "Description of the event",
                            "default": ""
                        }
                    },
                    "required": ["summary", "start_time"]
                }
            ),
            Tool(
                name="find_free_slots",
                description="Find available time slots in calendars for yourself and/or other people",
                function=self.find_free_slots,
                parameters={
                    "type": "object",
                    "properties": {
                        "start_date": {
                            "type": "string",
                            "description": "Start date to look for free slots (e.g., 'today', 'tomorrow', '2024-02-05')"
                        },
                        "days_to_check": {
                            "type": "integer",
                            "description": "Number of days to look ahead",
                            "default": 5
                        },
                        "duration_minutes": {
                            "type": "integer",
                            "description": "Duration needed for the meeting in minutes",
                            "default": 30
                        },
                        "working_hours": {
                            "type": "object",
                            "description": "Working hours to consider (24-hour format)",
                            "properties": {
                                "start_hour": {
                                    "type": "integer",
                                    "default": 9
                                },
                                "end_hour": {
                                    "type": "integer",
                                    "default": 17
                                }
                            }
                        },
                        "timezone": {
                            "type": "string",
                            "description": "Timezone for the search (e.g., 'America/New_York')",
                            "default": "UTC"
                        },
                        "emails": {
                            "type": "array",
                            "description": "List of email addresses to check availability for. If empty, checks your own calendar.",
                            "items": {
                                "type": "string"
                            },
                            "default": []
                        }
                    },
                    "required": ["start_date"]
                }
            )
        ]

    def list_upcoming_events(self, max_results: int = 10) -> str:
        """List upcoming calendar events."""
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        events_result = self._service.events().list(
            calendarId='primary',
            timeMin=now,
            maxResults=max_results,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        events = events_result.get('items', [])

        if not events:
            return "No upcoming events found."

        result = []
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            result.append(f"{start}: {event['summary']}")

        return "\n".join(result)

    def create_event(self, summary: str, start_time: str, duration_minutes: int = 60, description: str = "") -> str:
        """Create a new calendar event."""
        try:
            # Parse the start time (handles both ISO format and natural language)
            start = parse(start_time)
            end = start + datetime.timedelta(minutes=duration_minutes)

            event = {
                'summary': summary,
                'description': description,
                'start': {
                    'dateTime': start.isoformat(),
                    'timeZone': 'UTC',
                },
                'end': {
                    'dateTime': end.isoformat(),
                    'timeZone': 'UTC',
                },
            }

            event = self._service.events().insert(calendarId='primary', body=event).execute()
            return f"Event created: {event.get('htmlLink')}"
        except Exception as e:
            return f"Failed to create event: {str(e)}"

    def find_free_slots(self, 
                       start_date: str,
                       days_to_check: int = 5,
                       duration_minutes: int = 30,
                       working_hours: Dict[str, int] = {"start_hour": 9, "end_hour": 17},
                       timezone: str = "UTC",
                       emails: List[str] = None) -> str:
        """
        Find available time slots in calendars for multiple people.
        
        Args:
            start_date: Start date to look for free slots (can be 'today', 'tomorrow', or a date)
            days_to_check: Number of days to look ahead
            duration_minutes: Duration needed for the meeting in minutes
            working_hours: Dictionary with start_hour and end_hour (24-hour format)
            timezone: Timezone for the search
            emails: List of email addresses to check availability for (optional)
        
        Returns:
            String containing available time slots that work for all participants
        """
        try:
            # Initialize emails list if None
            emails = emails or []
            
            # Parse start date
            if start_date.lower() == 'today':
                start = datetime.now()
            elif start_date.lower() == 'tomorrow':
                start = datetime.now() + timedelta(days=1)
            else:
                start = parse(start_date)

            # Set to beginning of day in specified timezone
            tz = pytz.timezone(timezone)
            start = start.replace(hour=0, minute=0, second=0, microsecond=0)
            start = tz.localize(start)

            # Calculate end time
            end = start + timedelta(days=days_to_check)

            # Prepare calendar items for query
            calendar_items = [{"id": "primary"}]  # Always include the current user
            calendar_items.extend([{"id": email} for email in emails])

            # Get busy periods
            body = {
                "timeMin": start.isoformat(),
                "timeMax": end.isoformat(),
                "timeZone": timezone,
                "items": calendar_items
            }

            free_busy = self._service.freebusy().query(body=body).execute()
            
            # Check calendar access and collect busy periods
            all_busy_periods = []
            inaccessible_calendars = []
            
            # Process primary calendar first
            if 'primary' not in free_busy['calendars']:
                return "Could not access your calendar. Please check your permissions."
            all_busy_periods.extend([
                (
                    parse(period['start']).astimezone(tz),
                    parse(period['end']).astimezone(tz)
                )
                for period in free_busy['calendars']['primary']['busy']
            ])
            
            # Process other calendars
            for email in emails:
                if email not in free_busy['calendars']:
                    inaccessible_calendars.append(email)
                    continue
                
                all_busy_periods.extend([
                    (
                        parse(period['start']).astimezone(tz),
                        parse(period['end']).astimezone(tz)
                    )
                    for period in free_busy['calendars'][email]['busy']
                ])

            # Report any inaccessible calendars
            if inaccessible_calendars:
                return f"Could not access calendars for: {', '.join(inaccessible_calendars)}. " \
                       "Please check the email addresses and calendar sharing permissions."

            # Merge overlapping busy periods
            if all_busy_periods:
                all_busy_periods.sort(key=lambda x: x[0])  # Sort by start time
                merged_busy_periods = []
                current_start, current_end = all_busy_periods[0]
                
                for busy_start, busy_end in all_busy_periods[1:]:
                    if busy_start <= current_end:
                        current_end = max(current_end, busy_end)
                    else:
                        merged_busy_periods.append((current_start, current_end))
                        current_start, current_end = busy_start, busy_end
                merged_busy_periods.append((current_start, current_end))
                all_busy_periods = merged_busy_periods

            # Find free slots
            free_slots = []
            current_day = start
            
            while current_day < end:
                # Set working hours for the day
                day_start = current_day.replace(
                    hour=working_hours['start_hour'],
                    minute=0,
                    second=0
                )
                day_end = current_day.replace(
                    hour=working_hours['end_hour'],
                    minute=0,
                    second=0
                )

                # Skip if it's weekend (Saturday = 5, Sunday = 6)
                if current_day.weekday() >= 5:
                    current_day += timedelta(days=1)
                    continue

                time_slot = day_start
                while time_slot + timedelta(minutes=duration_minutes) <= day_end:
                    slot_end = time_slot + timedelta(minutes=duration_minutes)
                    
                    # Check if slot conflicts with any busy period
                    is_free = True
                    for busy_start, busy_end in all_busy_periods:
                        if (time_slot < busy_end and slot_end > busy_start):
                            is_free = False
                            break
                    
                    if is_free:
                        free_slots.append(time_slot)
                    
                    time_slot += timedelta(minutes=30)  # 30-minute increments
                
                current_day += timedelta(days=1)

            # Format results
            if not free_slots:
                participants = "everyone" if emails else "you"
                return f"No free slots found for {participants} in the specified time range."

            # Create participant list for message
            if not emails:
                participants = "your calendar"
            else:
                participants = f"calendars of: you, {', '.join(emails)}"

            result = [f"Available {duration_minutes}-minute slots for {participants}:"]
            for slot in free_slots[:10]:  # Limit to first 10 slots
                result.append(f"- {slot.strftime('%Y-%m-%d %I:%M %p %Z')}")
            
            if len(free_slots) > 10:
                result.append(f"\n(Showing first 10 of {len(free_slots)} available slots)")

            return "\n".join(result)

        except Exception as e:
            participants = "your calendar" if not emails else f"calendars for {', '.join(['you'] + emails)}"
            return f"Error finding free slots in {participants}: {str(e)}"