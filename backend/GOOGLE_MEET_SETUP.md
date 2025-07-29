# Google Meet Agent - Calendar Configuration Guide

## 📅 Service Account Calendar Behavior

When using the Google Meet agent with a service account JSON file, **events are created in the service account's own calendar** by default, not your personal Google Calendar.

### Current Behavior

- **Service Account Email**: `firebase-adminsdk-fbsvc@langgraph-825ec.iam.gserviceaccount.com`
- **Default Calendar**: Service account's primary calendar
- **Google Meet Support**: Limited (service accounts typically don't have Google Workspace features)

## 🎯 Calendar Configuration Options

### Option 1: Service Account Calendar (Current)

```python
# Events created in service account's calendar
calendar_id = "primary"  # Default behavior
```

- ✅ **Pros**: Simple setup, works immediately
- ❌ **Cons**: Events not in your personal calendar, limited Google Meet support

### Option 2: Your Personal Calendar

```python
# Events created in your personal Google Calendar
calendar_id = "your.email@gmail.com"
```

- ✅ **Pros**: Events appear in your calendar, better Google Meet support
- ❌ **Cons**: Requires calendar sharing with service account

### Option 3: Domain-Wide Delegation (Google Workspace)

```python
# Impersonate your user account
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
).with_subject('your.email@yourcompany.com')
```

- ✅ **Pros**: Full Google Workspace features, Google Meet support
- ❌ **Cons**: Requires Google Workspace admin setup

## 🔧 Setting Up Personal Calendar Access

### Step 1: Share Your Calendar with Service Account

1. Open Google Calendar (calendar.google.com)
2. Find your calendar in the left sidebar
3. Click the three dots → "Settings and sharing"
4. Under "Share with specific people", click "Add people"
5. Add: `firebase-adminsdk-fbsvc@langgraph-825ec.iam.gserviceaccount.com`
6. Set permission to: "Make changes to events"

### Step 2: Use Your Email as Calendar ID

The agent can be configured to use your personal calendar:

```python
calendar_id = "your.email@gmail.com"
```

### Step 3: Enable Google Meet (If Google Workspace)

- Ensure your Google Workspace admin has enabled Google Meet
- Check calendar conference settings in admin console

## 🚀 Quick Test

After setup, test with:

```bash
curl -X POST "http://localhost:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{"message": "Schedule a test meeting for tomorrow at 2 PM"}'
```

The response will show which calendar the event was created in.

## 🎯 For Full Google Meet Integration

To get working Google Meet links:

1. **Use Google Workspace account** (not personal Gmail)
2. **Enable domain-wide delegation** for the service account
3. **Configure Google Meet** in Google Workspace admin console
4. **Use your work email** as calendar_id

## 📝 Current Status

- ✅ **Calendar Event Creation**: Working in service account calendar
- ⚠️ **Google Meet Links**: Limited (requires Google Workspace)
- ✅ **Meeting Scheduling**: Fully functional
- ✅ **Natural Language Parsing**: Working perfectly

The agent works great for calendar scheduling and will automatically add Google Meet links when proper Google Workspace configuration is in place!
