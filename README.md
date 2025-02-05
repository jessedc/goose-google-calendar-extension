# Goose Google Calendar Plugin

A Goose plugin that provides integration with Google Calendar, allowing you to view and create calendar events.

## Prerequisites

1. You need to set up a Google Cloud Project and enable the Google Calendar API
2. Create OAuth 2.0 credentials (Desktop application type)
3. Download the credentials and save them as `credentials.json` in `~/.config/goose/calendar/`

## Installation

```bash
pip install .
```

## Features

The plugin provides two main tools:

1. `list_upcoming_events`: Lists your upcoming calendar events
   - Parameters:
     - `max_results`: Maximum number of events to return (default: 10)

2. `create_event`: Creates a new calendar event
   - Parameters:
     - `summary`: Title of the event (required)
     - `start_time`: Start time in ISO format or natural language (required)
     - `duration_minutes`: Duration in minutes (default: 60)
     - `description`: Event description (optional)

## Setup

1. First, set up a Google Cloud Project and enable the Calendar API:
   - Go to the [Google Cloud Console](https://console.cloud.google.com)
   - Create a new project or select an existing one
   - Enable the Google Calendar API
   - Create OAuth 2.0 credentials (Desktop application type)
   - Download the credentials

2. Place the credentials file:
   ```bash
   mkdir -p ~/.config/goose/calendar
   mv /path/to/downloaded/credentials.json ~/.config/goose/calendar/
   ```

3. Install the plugin:
   ```bash
   pip install .
   ```

4. On first use, the plugin will open a browser window for OAuth authentication

## Usage Examples

```python
# List upcoming events
list_upcoming_events(max_results=5)

# Create a new event
create_event(
    summary="Team Meeting",
    start_time="tomorrow at 2pm",
    duration_minutes=45,
    description="Weekly team sync"
)
```

## Development

This plugin demonstrates:
- OAuth2 authentication with Google APIs
- Handling credentials and token persistence
- Natural language date parsing
- Error handling for API interactions

Feel free to extend the functionality by adding more calendar operations!