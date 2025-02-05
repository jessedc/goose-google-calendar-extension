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

## External References

### Google Calendar API
- [Calendar API Overview](https://developers.google.com/calendar/api/guides/overview)
- [Calendar API Reference](https://developers.google.com/calendar/api/v3/reference)
- [Google Calendar Auth Guide](https://developers.google.com/calendar/api/quickstart/python)
- [FreeBusy API Reference](https://developers.google.com/calendar/api/v3/reference/freebusy)
- [Events API Reference](https://developers.google.com/calendar/api/v3/reference/events)
- [Python Client Library](https://googleapis.dev/python/google-api-python-client/latest/docs/dyn/calendar_v3.html)

### Goose Documentation
- [Goose Extension Development Guide](https://goose.ai/docs/extensions)
- [Tool Definition Reference](https://goose.ai/docs/tools)
- [Extension Best Practices](https://goose.ai/docs/best-practices)

## Future Enhancements

Planned features for this plugin:
1. Support for recurring events
2. Priority-based scheduling
3. Preferred time ranges
4. Multiple calendar support
5. Meeting room booking

## Ideas for Additional Goose Extensions

### 1. Calendar Integration Extensions
- **Microsoft Outlook Calendar**: Similar functionality for Microsoft 365
- **Apple Calendar**: Native macOS calendar integration
- **Calendly**: Automated scheduling and availability management
- **Meeting Room Manager**: Smart conference room booking system

### 2. Productivity Extensions
- **Task Manager**: Integration with tools like Asana, Trello, or Jira
- **Note Taking**: Connect with Evernote, OneNote, or Notion
- **Time Tracking**: Integrate with Toggl, RescueTime, or other time trackers
- **Document Management**: Google Drive, Dropbox, or OneDrive integration

### 3. Communication Extensions
- **Email Manager**: Gmail, Outlook, or other email service integration
- **Chat Integration**: Slack, Microsoft Teams, or Discord
- **Video Conferencing**: Zoom, Google Meet, or Teams meeting management
- **Contact Manager**: Smart contact organization and scheduling

### 4. Development Tools
- **GitHub Manager**: Repository, PR, and issue management
- **CI/CD Controller**: Pipeline management for various CI systems
- **Code Review Assistant**: Automated code review scheduling
- **Documentation Manager**: Auto-update documentation based on code changes

### 5. Project Management
- **Resource Scheduler**: Team capacity and resource allocation
- **Sprint Planner**: Agile sprint planning assistance
- **Timeline Manager**: Project timeline and milestone tracking
- **Budget Tracker**: Project budget and resource cost tracking

### 6. Smart Office Extensions
- **Smart Light Controller**: Office lighting automation
- **Temperature Control**: Smart thermostat integration
- **Office Music**: Shared music playlist management
- **Desk Booking**: Hot desk reservation system

### 7. Knowledge Management
- **Wiki Manager**: Team knowledge base organization
- **Document Summarizer**: Auto-summarize documents and meetings
- **Learning Resources**: Track and schedule training materials
- **Research Assistant**: Literature and web research automation

### 8. Analytics and Reporting
- **Dashboard Creator**: Automated report generation
- **Data Visualizer**: Create charts and graphs from data
- **Metrics Tracker**: KPI and metrics monitoring
- **Performance Reporter**: Automated performance report generation

### 9. Customer Relationship
- **CRM Integration**: Salesforce, HubSpot, or other CRM tools
- **Support Ticket Manager**: Help desk and ticket scheduling
- **Customer Meeting Scheduler**: Automated customer meeting setup
- **Follow-up Manager**: Track and schedule follow-up actions

### 10. Health and Wellness
- **Break Scheduler**: Smart break and rest period planning
- **Exercise Planner**: Workout scheduling around meetings
- **Mental Health**: Meditation and mindfulness session scheduling
- **Team Building**: Automated team activity planning

Each of these extensions could leverage Goose's capabilities to:
- Automate repetitive tasks
- Integrate multiple services
- Provide natural language interfaces
- Handle complex scheduling and coordination
- Manage permissions and access control
- Generate reports and analytics
- Facilitate team collaboration

Development Considerations:
1. Focus on user experience and natural language interaction
2. Implement robust error handling and recovery
3. Consider security and privacy implications
4. Design for extensibility and modularity
5. Include comprehensive documentation
6. Add testing and validation
7. Consider cross-platform compatibility