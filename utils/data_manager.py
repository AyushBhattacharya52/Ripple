# utils/data_manager.py
import json
import os
import uuid
from datetime import datetime
from typing import List, Dict, Optional
import hashlib
from kivy.logger import Logger
import requests

FIREBASE_DB_URL = "https://ripple-7338e-default-rtdb.firebaseio.com/"
# Add these methods to your existing DataManager class in utils/data_manager.py

def register_user(self, user_data):
    """Register a new user - wrapper for your existing create_user method"""
    # Map the test suite's expected format to your create_user method
    mapped_data = {
        'name': user_data.get('full_name', user_data.get('name', '')),
        'email': user_data.get('email', ''),
        'password': user_data.get('password', ''),
        'phone': user_data.get('phone', ''),
        'preferences': user_data.get('preferences', {})
    }
    
    # Add username to the user data if it doesn't exist
    if 'username' in user_data:
        mapped_data['username'] = user_data['username']
    
    result = self.create_user(mapped_data)
    return result is not None

def authenticate_user(self, credentials):
    """Fix authenticate_user to accept a dictionary instead of separate parameters"""
    email = credentials.get('email') or credentials.get('username', '')
    password = credentials.get('password', '')
    
    if not email or not password:
        return None
    
    # Use your existing authenticate_user method (rename the current one to avoid conflict)
    return self.authenticate_user_internal(email, password)

def authenticate_user_internal(self, email: str, password: str):
    """Your existing authenticate_user method - renamed to avoid conflict"""
    users = self.load_json(self.users_file)
    hashed_password = self.hash_password(password)
    
    for user in users:
        if user['email'].lower() == email.lower() and user['password'] == hashed_password:
            # Return user without password
            user_return = user.copy()
            del user_return['password']
            return user_return
    
    return None

def get_events_by_category(self, category):
    """Get events filtered by category"""
    events = self.get_all_events()
    return [event for event in events if event.get('category') == category]

def get_events_by_creator(self, creator_id):
    """Get events created by a specific user"""
    events = self.get_all_events()
    return [event for event in events if event.get('creator_id') == creator_id]

def get_user_created_events(self, user_id):
    """Get events created by a user - alias for get_events_by_creator"""
    return self.get_events_by_creator(user_id)

def get_user_registered_events(self, user_id):
    """Get events a user is registered for"""
    registrations = self.get_user_registrations(user_id)
    
    # Get full event details for each registration
    registered_events = []
    for reg in registrations:
        event = self.get_event_by_id(reg['event_id'])
        if event:
            registered_events.append(event)
    
    return registered_events

def register_for_event(self, user_id, event_id):
    """Register user for event - simplified version of your existing method"""
    # Get user and event details
    users = self.load_json(self.users_file)
    user = None
    for u in users:
        if u['id'] == user_id or u.get('username') == user_id:
            user = u
            break
    
    if not user:
        return False
    
    event = self.get_event_by_id(event_id)
    if not event:
        return False
    
    # Use your existing registration method
    registration_data = {
        'user_id': user_id,
        'event_id': event_id,
        'name': user.get('name', user.get('username', '')),
        'email': user.get('email', ''),
        'phone': user.get('phone', '')
    }
    
    result = self.register_for_event_internal(registration_data)
    return result is not None

def register_for_event_internal(self, registration_data):
    """Your existing register_for_event method - renamed to avoid conflict"""
    registrations = self.load_json(self.registrations_file)
    
    # Check if user already registered for this event
    if any(reg['user_id'] == registration_data['user_id'] and 
           reg['event_id'] == registration_data['event_id'] 
           for reg in registrations):
        return None
    
    # Get event details
    event = self.get_event_by_id(registration_data['event_id'])
    if not event:
        return None
    
    # Check if event is full
    if event['current_participants'] >= event['max_participants']:
        return None
    
    new_registration = {
        'id': self.generate_id(),
        'user_id': registration_data['user_id'],
        'event_id': registration_data['event_id'],
        'event_title': event['title'],
        'event_date': event['date'],
        'event_time': event['time'],
        'event_location': event['location'],
        'name': registration_data['name'],
        'email': registration_data['email'],
        'phone': registration_data['phone'],
        'registered_at': self.get_timestamp()
    }
    
    registrations.append(new_registration)
    if self.save_json(self.registrations_file, registrations):
        # Update event participant count
        self.update_event_participants(registration_data['event_id'], 1)
        return new_registration
    
    return None

def update_event(self, event_id, update_data):
    """Update an existing event"""
    events = self.load_json(self.events_file)
    
    for event in events:
        if event['id'] == event_id:
            # Update the fields provided in update_data
            for key, value in update_data.items():
                if key in event:
                    event[key] = value
            
            return self.save_json(self.events_file, events)
    
    return False

def cancel_event(self, event_id):
    """Cancel/delete an event"""
    events = self.load_json(self.events_file)
    
    for event in events:
        if event['id'] == event_id:
            event['is_active'] = False  # Mark as inactive instead of deleting
            return self.save_json(self.events_file, events)
    
    return False

# Fix your existing create_event method to work with Firebase and JSON
def create_event(self, event_data):
    """Enhanced create_event method that works with both Firebase and JSON"""
    # Try Firebase first
    firebase_result = firebase_post("events", event_data)
    firebase_success = firebase_result is not None
    
    # Also save to JSON as backup/local storage
    events = self.load_json(self.events_file)
    
    # If the event doesn't have an ID, generate one
    if 'id' not in event_data:
        event_data['id'] = self.generate_id()
    
    new_event = {
        'id': event_data.get('id', self.generate_id()),
        'title': event_data['title'],
        'description': event_data['description'],
        'date': event_data['date'],
        'time': event_data['time'],
        'location': event_data['location'],
        'category': event_data.get('category', 'General'),
        'max_participants': event_data.get('max_participants', 50),
        'current_participants': 0,
        'creator_id': event_data['creator_id'],
        'creator_name': event_data.get('creator_name', ''),
        'latitude': event_data.get('latitude'),
        'longitude': event_data.get('longitude'),
        'city': event_data.get('city', ''),
        'country': event_data.get('country', ''),
        'created_at': self.get_timestamp(),
        'is_active': True
    }
    
    events.append(new_event)
    json_success = self.save_json(self.events_file, events)
    
    # Return True if either Firebase or JSON succeeded
    return firebase_success or json_success

def get_all_events(self):
    """Enhanced get_all_events that tries Firebase first, falls back to JSON"""
    # Try Firebase first
    firebase_events = firebase_get("events")
    if firebase_events:
        events_list = []
        for event_id, event_data in firebase_events.items():
            if isinstance(event_data, dict):
                event_data['id'] = event_data.get('id', event_id)
                events_list.append(event_data)
        
        # Also sync with local JSON
        self.save_json(self.events_file, events_list)
        return events_list
    
    # Fallback to JSON
    events = self.load_json(self.events_file)
    return [event for event in events if event.get('is_active', True)]



def firebase_get(path):
    url = f"{FIREBASE_DB_URL}{path}.json"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Firebase GET error: {e}")
        return None

def firebase_put(path, data):
    url = f"{FIREBASE_DB_URL}{path}.json"
    try:
        response = requests.put(url, json=data)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Firebase PUT error: {e}")
        return None

def firebase_post(path, data):
    url = f"{FIREBASE_DB_URL}{path}.json"
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Firebase POST error: {e}")
        return None

def firebase_patch(path, data):
    url = f"{FIREBASE_DB_URL}{path}.json"
    try:
        response = requests.patch(url, json=data)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Firebase PATCH error: {e}")
        return None


class DataManager:
    def create_event(self, event_data):
        result = firebase_post("events", event_data)
        return result is not None
    
    def get_all_events(self):
        events = firebase_get("events")
        if events:
            return [v for v in events.values()]
        return []
    def __init__(self):
        self.data_dir = 'data'
        self.users_file = os.path.join(self.data_dir, 'users.json')
        self.events_file = os.path.join(self.data_dir, 'events.json')
        self.registrations_file = os.path.join(self.data_dir, 'registrations.json')
        self.categories_file = os.path.join(self.data_dir, 'categories.json')
        
        self.initialize_files()
    
    def initialize_files(self):
        """Initialize JSON files if they don't exist"""
        files_data = {
            self.users_file: [],
            self.events_file: [],
            self.registrations_file: [],
            self.categories_file: [
                "Technology", "Business", "Education", "Health & Wellness",
                "Arts & Culture", "Sports & Fitness", "Food & Drink",
                "Music & Entertainment", "Community", "Professional Development",
                "Travel", "Gaming", "Photography", "Science", "Environment"
            ]
        }
        
        for file_path, default_data in files_data.items():
            if not os.path.exists(file_path):
                self.save_json(file_path, default_data)
                Logger.info(f"DataManager: Initialized {file_path}")
    
    def load_json(self, file_path: str) -> List[Dict]:
        """Load data from JSON file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            Logger.error(f"DataManager: Error loading {file_path}: {e}")
            return []
    
    def save_json(self, file_path: str, data: List[Dict]):
        """Save data to JSON file"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            Logger.error(f"DataManager: Error saving {file_path}: {e}")
            return False
    
    def hash_password(self, password: str) -> str:
        """Hash password for secure storage"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def generate_id(self) -> str:
        """Generate unique ID"""
        return str(uuid.uuid4())
    
    def get_timestamp(self) -> str:
        """Get current timestamp"""
        return datetime.now().isoformat()
    
    # User management
    def create_user(self, user_data: Dict) -> Optional[Dict]:
        """Create a new user"""
        users = self.load_json(self.users_file)
        
        # Check if user already exists
        if any(user['email'].lower() == user_data['email'].lower() for user in users):
            return None
        
        new_user = {
            'id': self.generate_id(),
            'name': user_data['name'],
            'email': user_data['email'].lower(),
            'password': self.hash_password(user_data['password']),
            'phone': user_data.get('phone', ''),
            'preferences': user_data.get('preferences', {}),
            'created_at': self.get_timestamp()
        }
        
        users.append(new_user)
        if self.save_json(self.users_file, users):
            # Return user without password
            user_return = new_user.copy()
            del user_return['password']
            return user_return
        
        return None
    
    def authenticate_user(self, email: str, password: str) -> Optional[Dict]:
        """Authenticate user login"""
        users = self.load_json(self.users_file)
        hashed_password = self.hash_password(password)
        
        for user in users:
            if user['email'].lower() == email.lower() and user['password'] == hashed_password:
                # Return user without password
                user_return = user.copy()
                del user_return['password']
                return user_return
        
        return None
    
    def update_user_preferences(self, user_id: str, preferences: Dict) -> bool:
        """Update user preferences"""
        users = self.load_json(self.users_file)
        
        for user in users:
            if user['id'] == user_id:
                user['preferences'] = preferences
                return self.save_json(self.users_file, users)
        
        return False
    
    # Event management
    def create_event(self, event_data: Dict) -> Optional[Dict]:
        """Create a new event"""
        events = self.load_json(self.events_file)
        
        new_event = {
            'id': self.generate_id(),
            'title': event_data['title'],
            'description': event_data['description'],
            'date': event_data['date'],
            'time': event_data['time'],
            'location': event_data['location'],
            'category': event_data.get('category', 'General'),
            'max_participants': event_data.get('max_participants', 50),
            'current_participants': 0,
            'creator_id': event_data['creator_id'],
            'creator_name': event_data['creator_name'],
            'latitude': event_data.get('latitude'),
            'longitude': event_data.get('longitude'),
            'city': event_data.get('city', ''),
            'country': event_data.get('country', ''),
            'created_at': self.get_timestamp(),
            'is_active': True
        }
        
        events.append(new_event)
        if self.save_json(self.events_file, events):
            return new_event
        
        return None
    
    def get_all_events(self) -> List[Dict]:
        """Get all active events"""
        events = self.load_json(self.events_file)
        return [event for event in events if event.get('is_active', True)]
    
    def get_event_by_id(self, event_id: str) -> Optional[Dict]:
        """Get specific event by ID"""
        events = self.load_json(self.events_file)
        
        for event in events:
            if event['id'] == event_id and event.get('is_active', True):
                return event
        
        return None
    
    def search_events(self, query: str, category: str = None) -> List[Dict]:
        """Search events by query and/or category"""
        events = self.get_all_events()
        results = []
        
        query_lower = query.lower() if query else ""
        
        for event in events:
            # Check category filter
            if category and event.get('category') != category:
                continue
            
            # Check query in title, description, or location
            if (query_lower in event['title'].lower() or 
                query_lower in event['description'].lower() or
                query_lower in event['location'].lower()):
                results.append(event)
        
        return results
    
    def update_event_participants(self, event_id: str, increment: int = 1) -> bool:
        """Update event participant count"""
        events = self.load_json(self.events_file)
        
        for event in events:
            if event['id'] == event_id:
                event['current_participants'] = max(0, event['current_participants'] + increment)
                return self.save_json(self.events_file, events)
        
        return False
    
    # Registration management
    def register_for_event(self, registration_data: Dict) -> Optional[Dict]:
        """Register user for an event"""
        registrations = self.load_json(self.registrations_file)
        
        # Check if user already registered for this event
        if any(reg['user_id'] == registration_data['user_id'] and 
               reg['event_id'] == registration_data['event_id'] 
               for reg in registrations):
            return None
        
        # Get event details
        event = self.get_event_by_id(registration_data['event_id'])
        if not event:
            return None
        
        # Check if event is full
        if event['current_participants'] >= event['max_participants']:
            return None
        
        new_registration = {
            'id': self.generate_id(),
            'user_id': registration_data['user_id'],
            'event_id': registration_data['event_id'],
            'event_title': event['title'],
            'event_date': event['date'],
            'event_time': event['time'],
            'event_location': event['location'],
            'name': registration_data['name'],
            'email': registration_data['email'],
            'phone': registration_data['phone'],
            'registered_at': self.get_timestamp()
        }
        
        registrations.append(new_registration)
        if self.save_json(self.registrations_file, registrations):
            # Update event participant count
            self.update_event_participants(registration_data['event_id'], 1)
            return new_registration
        
        return None
    
    def get_user_registrations(self, user_id: str) -> List[Dict]:
        """Get all registrations for a user"""
        registrations = self.load_json(self.registrations_file)
        return [reg for reg in registrations if reg['user_id'] == user_id]
    
    def get_event_registrations(self, event_id: str) -> List[Dict]:
        """Get all registrations for an event"""
        registrations = self.load_json(self.registrations_file)
        return [reg for reg in registrations if reg['event_id'] == event_id]
    
    def cancel_registration(self, user_id: str, event_id: str) -> bool:
        """Cancel user registration for an event"""
        registrations = self.load_json(self.registrations_file)
        
        for i, reg in enumerate(registrations):
            if reg['user_id'] == user_id and reg['event_id'] == event_id:
                registrations.pop(i)
                if self.save_json(self.registrations_file, registrations):
                    # Update event participant count
                    self.update_event_participants(event_id, -1)
                    return True
                break
        
        return False
    
    # Category management
    def get_categories(self) -> List[str]:
        """Get all event categories"""
        return self.load_json(self.categories_file)
    
    def add_category(self, category: str) -> bool:
        """Add new category"""
        categories = self.load_json(self.categories_file)
        
        if category not in categories:
            categories.append(category)
            categories.sort()
            return self.save_json(self.categories_file, categories)
        
        return False
    
    # Analytics and insights
    def get_popular_events(self, limit: int = 10) -> List[Dict]:
        """Get most popular events by registration count"""
        events = self.get_all_events()
        events.sort(key=lambda x: x['current_participants'], reverse=True)
        return events[:limit]
    
    def get_events_by_date_range(self, start_date: str, end_date: str) -> List[Dict]:
        """Get events within date range"""
        events = self.get_all_events()
        return [
            event for event in events 
            if start_date <= event['date'] <= end_date
        ]