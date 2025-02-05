# Goose Google Calendar Plugin

A Goose plugin that provides integration with Google Calendar, allowing for calendar management, event scheduling, and availability checking.

## Available Tools

### 1. `list_upcoming_events`
Lists upcoming calendar events.

**Parameters:**
- `max_results` (int, default=10): Maximum number of events to return

**Example:**
```python
# List next 5 events
list_upcoming_events(max_results=5)
```

### 2. `create_event`
Creates a new calendar event.

**Parameters:**
- `summary` (str, required): Title of the event
- `start_time` (str, required): Start time in ISO format or natural language (e.g., '2024-02-25T10:00:00' or 'tomorrow at 3pm')
- `duration_minutes` (int, default=60): Duration of the event in minutes
- `description` (str, default=""): Event description

**Examples:**
```python
# Create an event using natural language
create_event(
    summary="Team Meeting",
    start_time="tomorrow at 2pm",
    duration_minutes=45,
    description="Weekly team sync"
)

# Create an event using ISO format
create_event(
    summary="Project Review",
    start_time="2024-02-25T14:00:00",
    duration_minutes=60,
    description="Q1 project review meeting"
)
```

### 3. `find_free_slots`
Find available time slots in calendars for multiple people.

**Parameters:**
- `start_date` (str, required): When to start looking (e.g., 'today', 'tomorrow', '2024-02-05')
- `days_to_check` (int, default=5): Number of days to look ahead
- `duration_minutes` (int, default=30): Length of meeting needed
- `working_hours` (dict, default={"start_hour": 9, "end_hour": 17}): Business hours to consider
- `timezone` (str, default="UTC"): Timezone for the search
- `emails` (list[str], default=[]): List of email addresses to check availability for

**Features:**
- Finds slots that work for all participants
- Respects working hours and weekends
- Merges overlapping busy periods
- Returns results in specified timezone
- Handles multiple calendars simultaneously

**Examples:**
```python
# Find slots for your own calendar
find_free_slots(
    start_date="tomorrow",
    duration_minutes=30,
    timezone="America/New_York"
)

# Find slots for a team meeting
find_free_slots(
    start_date="2024-02-10",
    days_to_check=3,
    duration_minutes=45,
    working_hours={"start_hour": 10, "end_hour": 16},
    timezone="America/New_York",
    emails=["team1@example.com", "team2@example.com"]
)
```

## Setup and Installation

1. **Set up Google Cloud Project:**
   ```bash
   # Create config directory
   mkdir -p ~/.config/goose/calendar
   
   # Move credentials
   mv ~/Downloads/credentials.json ~/.config/goose/calendar/
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Plugin:**
   ```bash
   pip install -e .
   ```

## Authentication

The plugin uses OAuth2 for authentication:
1. First use will open a browser window
2. Log in with your Google account
3. Grant calendar permissions
4. Token is saved for future use

## Common Use Cases

### 1. Quick Meeting Scheduling
```python
# Find available slots
slots = find_free_slots(
    start_date="today",
    duration_minutes=30,
    timezone="America/New_York"
)

# Create the meeting
create_event(
    summary="Quick Sync",
    start_time="today at 3pm",
    duration_minutes=30
)
```

### 2. Team Meeting Coordination
```python
# Find slots that work for the whole team
find_free_slots(
    start_date="next monday",
    duration_minutes=60,
    emails=[
        "manager@example.com",
        "team1@example.com",
        "team2@example.com"
    ],
    working_hours={"start_hour": 9, "end_hour": 17},
    timezone="America/New_York"
)
```

### 3. Multi-day Event Planning
```python
# Check availability across multiple days
find_free_slots(
    start_date="2024-03-01",
    days_to_check=5,
    duration_minutes=120,
    working_hours={"start_hour": 10, "end_hour": 16}
)
```

## Best Practices

1. **Timezone Handling**
   - Always specify the timezone for clarity
   - Use IANA timezone names (e.g., "America/New_York", "Europe/London")

2. **Working Hours**
   - Consider team working hours when scheduling
   - Default is 9 AM to 5 PM
   - Can be customized per query

3. **Calendar Permissions**
   - Ensure necessary calendar sharing permissions
   - Handle inaccessible calendars gracefully

4. **Date/Time Formats**
   - ISO format: "2024-02-25T14:00:00"
   - Natural language: "tomorrow at 2pm", "next monday at 10am"

## Error Handling

The plugin handles common errors:
- Inaccessible calendars
- Invalid email addresses
- Permission issues
- Invalid date/time formats

## Limitations

1. **Google Sheets Integration**
   - Only first sheet is accessible

2. **Calendar Access**
   - Requires appropriate sharing permissions
   - Read-only access to other calendars

3. **Free/Busy Information**
   - Limited to available/busy status
   - No access to private event details

## Future Enhancements

Planned features:
1. Support for recurring events
2. Priority-based scheduling
3. Preferred time ranges
4. Multiple calendar support
5. Meeting room booking