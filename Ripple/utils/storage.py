# utils/storage.py (updated with better error handling)
import json
import os

USERS_FILE = "data/users.json"
EVENTS_FILE = "data/events.json"
REGISTRATIONS_FILE = "data/registrations.json"

def ensure_data_dir():
    if not os.path.exists("data"):
        os.makedirs("data")

# Users
def load_users():
    ensure_data_dir()
    if not os.path.exists(USERS_FILE):
        return []
    try:
        with open(USERS_FILE, "r") as f:
            content = f.read().strip()
            if not content:
                return []
            return json.loads(content)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def save_user(user):
    ensure_data_dir()
    users = load_users()
    users.append(user)
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)

# Events
def load_events():
    ensure_data_dir()
    if not os.path.exists(EVENTS_FILE):
        return []
    try:
        with open(EVENTS_FILE, "r") as f:
            content = f.read().strip()
            if not content:
                return []
            return json.loads(content)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def save_event(event):
    ensure_data_dir()
    events = load_events()
    events.append(event)
    with open(EVENTS_FILE, "w") as f:
        json.dump(events, f, indent=2)

# Registrations
def load_registrations():
    ensure_data_dir()
    if not os.path.exists(REGISTRATIONS_FILE):
        return []
    try:
        with open(REGISTRATIONS_FILE, "r") as f:
            content = f.read().strip()
            if not content:
                return []
            return json.loads(content)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def save_registration(registration):
    ensure_data_dir()
    registrations = load_registrations()
    registrations.append(registration)
    with open(REGISTRATIONS_FILE, "w") as f:
        json.dump(registrations, f, indent=2)