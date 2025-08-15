# utils/storage.py - Enhanced storage with better error handling and app store optimizations
import json
import os
import hashlib
import uuid
from datetime import datetime
from typing import List, Dict, Optional
from kivy.logger import Logger

# File paths
USERS_FILE = "data/users.json"
EVENTS_FILE = "data/events.json"  
REGISTRATIONS_FILE = "data/registrations.json"

def ensure_data_dir():
    """Ensure data directory exists"""
    if not os.path.exists("data"):
        os.makedirs("data")
        Logger.info("Storage: Created data directory")

# Enhanced user functions
def load_users():
    """Load users with enhanced error handling"""
    ensure_data_dir()
    if not os.path.exists(USERS_FILE):
        return []
    try:
        with open(USERS_FILE, "r", encoding='utf-8') as f:
            content = f.read().strip()
            if not content:
                return []
            return json.loads(content)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        Logger.error(f"Storage: Error loading users - {e}")
        return []

def save_user(user):
    """Save single user with enhanced error handling"""
    ensure_data_dir()
    try:
        users = load_users()
        
        # Check if user already exists (by email)
        for i, existing_user in enumerate(users):
            if existing_user.get('email', '').lower() == user.get('email', '').lower():
                users[i] = user  # Update existing user
                break
        else:
            # Add ID if not present
            if 'id' not in user:
                user['id'] = str(uuid.uuid4())
            # Add timestamp
            if 'created_at' not in user:
                user['created_at'] = datetime.now().isoformat()
            users.append(user)
        
        with open(USERS_FILE, "w", encoding='utf-8') as f:
            json.dump(users, f, indent=2, ensure_ascii=False)
        Logger.info(f"Storage: Saved user {user.get('email', 'unknown')}")
        return True
    except Exception as e:
        Logger.error(f"Storage: Error saving user - {e}")
        return False

def authenticate_user(email, password):
    """Authenticate user with hashed password"""
    users = load_users()
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    
    for user in users:
        if (user.get('email', '').lower() == email.lower() and 
            user.get('password') == hashed_password):
            # Return user without password
            safe_user = user.copy()
            safe_user.pop('password', None)
            return safe_user
    return None

# Enhanced event functions  
def load_events():
    """Load events with enhanced error handling"""
    ensure_data_dir()
    if not os.path.exists(EVENTS_FILE):
        return []
    try:
        with open(EVENTS_FILE, "r", encoding='utf-8') as f:
            content = f.read().strip()
            if not content:
                return []
            events = json.loads(content)
            # Filter only active events
            return [event for event in events if event.get('is_active', True)]
    except (json.JSONDecodeError, FileNotFoundError) as e:
        Logger.error(f"Storage: Error loading events - {e}")
        return []

def save_event(event):
    """Save single event with enhanced error handling"""
    ensure_data_dir()
    try:
        events = load_all_events()  # Load all events including inactive
        
        # Add ID if not present
        if 'id' not in event:
            event['id'] = str(uuid.uuid4())
        # Add timestamp
        if 'created_at' not in event:
            event['created_at'] = datetime.now().isoformat()
        # Set as active by default
        if 'is_active' not in event:
            event['is_active'] = True
        # Initialize participant count
        if 'current_participants' not in event:
            event['current_participants'] = 0
            
        events.append(event)
        
        with open(EVENTS_FILE, "w", encoding='utf-8') as f:
            json.dump(events, f, indent=2, ensure_ascii=False)
        Logger.info(f"Storage: Saved event {event.get('title', 'unknown')}")
        return True
    except Exception as e:
        Logger.error(f"Storage: Error saving event - {e}")
        return False

def load_all_events():
    """Load all events including inactive ones"""
    ensure_data_dir()
    if not os.path.exists(EVENTS_FILE):
        return []
    try:
        with open(EVENTS_FILE, "r", encoding='utf-8') as f:
            content = f.read().strip()
            if not content:
                return []
            return json.loads(content)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        Logger.error(f"Storage: Error loading all events - {e}")
        return []

def get_event_by_id(event_id):
    """Get specific event by ID"""
    events = load_events()
    for event in events:
        if event.get('id') == event_id:
            return event
    return None

def update_event_participants(event_id, increment=1):
    """Update event participant count"""
    try:
        events = load_all_events()
        for event in events:
            if event.get('id') == event_id:
                current = event.get('current_participants', 0)
                event['current_participants'] = max(0, current + increment)
                break
        
        with open(EVENTS_FILE, "w", encoding='utf-8') as f:
            json.dump(events, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        Logger.error(f"Storage: Error updating event participants - {e}")
        return False

# Enhanced registration functions
def load_registrations():
    """Load registrations with enhanced error handling"""
    ensure_data_dir()
    if not os.path.exists(REGISTRATIONS_FILE):
        return []
    try:
        with open(REGISTRATIONS_FILE, "r", encoding='utf-8') as f:
            content = f.read().strip()
            if not content:
                return []
            return json.loads(content)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        Logger.error(f"Storage: Error loading registrations - {e}")
        return []

def save_registration(registration):
    """Save single registration with enhanced error handling"""
    ensure_data_dir()
    try:
        registrations = load_registrations()
        
        # Check if already registered
        user_id = registration.get('user_id')
        event_id = registration.get('event_id')
        
        if user_id and event_id:
            for existing in registrations:
                if (existing.get('user_id') == user_id and 
                    existing.get('event_id') == event_id):
                    Logger.warning("Storage: User already registered for this event")
                    return False
        
        # Add ID if not present
        if 'id' not in registration:
            registration['id'] = str(uuid.uuid4())
        # Add timestamp
        if 'registered_at' not in registration:
            registration['registered_at'] = datetime.now().isoformat()
            
        registrations.append(registration)
        
        with open(REGISTRATIONS_FILE, "w", encoding='utf-8') as f:
            json.dump(registrations, f, indent=2, ensure_ascii=False)
        
        # Update event participant count
        if event_id:
            update_event_participants(event_id, 1)
            
        Logger.info(f"Storage: Saved registration for event {event_id}")
        return True
    except Exception as e:
        Logger.error(f"Storage: Error saving registration - {e}")
        return False

def get_user_registrations(user_id):
    """Get all registrations for a specific user"""
    registrations = load_registrations()
    return [reg for reg in registrations if reg.get('user_id') == user_id]

def cancel_registration(user_id, event_id):
    """Cancel a user's registration for an event"""
    try:
        registrations = load_registrations()
        original_count = len(registrations)
        
        registrations = [reg for reg in registrations 
                        if not (reg.get('user_id') == user_id and 
                               reg.get('event_id') == event_id)]
        
        if len(registrations) < original_count:
            with open(REGISTRATIONS_FILE, "w", encoding='utf-8') as f:
                json.dump(registrations, f, indent=2, ensure_ascii=False)
            
            # Update event participant count
            update_event_participants(event_id, -1)
            Logger.info(f"Storage: Cancelled registration for event {event_id}")
            return True
        
        return False
    except Exception as e:
        Logger.error(f"Storage: Error cancelling registration - {e}")
        return False

# Search and filter functions
def search_events(query, category=None):
    """Search events by title, description, or category"""
    events = load_events()
    if not query and not category:
        return events
    
    results = []
    query_lower = query.lower() if query else ""
    
    for event in events:
        # Category filter
        if category and event.get('category') != category:
            continue
            
        # Text search in title, description, location
        if query_lower:
            searchable_text = f"{event.get('title', '')} {event.get('description', '')} {event.get('location', '')}".lower()
            if query_lower not in searchable_text:
                continue
        
        results.append(event)
    
    return results

def get_events_by_category(category):
    """Get events filtered by category"""
    events = load_events()
    return [event for event in events if event.get('category') == category]

def get_popular_events(limit=10):
    """Get events sorted by participant count"""
    events = load_events()
    events.sort(key=lambda x: x.get('current_participants', 0), reverse=True)
    return events[:limit]

# Data management and cleanup functions
def get_data_stats():
    """Get statistics about stored data"""
    stats = {
        'users_count': len(load_users()),
        'events_count': len(load_events()),
        'registrations_count': len(load_registrations()),
        'total_files': 0,
        'total_size_mb': 0
    }
    
    files = [USERS_FILE, EVENTS_FILE, REGISTRATIONS_FILE]
    for file_path in files:
        if os.path.exists(file_path):
            stats['total_files'] += 1
            stats['total_size_mb'] += os.path.getsize(file_path) / (1024 * 1024)
    
    stats['total_size_mb'] = round(stats['total_size_mb'], 2)
    return stats

def cleanup_old_events(days_old=30):
    """Remove old events to save storage space"""
    try:
        from datetime import datetime, timedelta
        cutoff_date = datetime.now() - timedelta(days=days_old)
        
        all_events = load_all_events()
        active_events = []
        removed_count = 0
        
        for event in all_events:
            try:
                event_date = datetime.fromisoformat(event.get('created_at', ''))
                # Keep events that are recent or have participants
                if (event_date > cutoff_date or 
                    event.get('current_participants', 0) > 0 or
                    event.get('is_active', True)):
                    active_events.append(event)
                else:
                    removed_count += 1
            except:
                # Keep events with invalid dates
                active_events.append(event)
        
        if removed_count > 0:
            with open(EVENTS_FILE, "w", encoding='utf-8') as f:
                json.dump(active_events, f, indent=2, ensure_ascii=False)
            Logger.info(f"Storage: Cleaned up {removed_count} old events")
        
        return removed_count
    except Exception as e:
        Logger.error(f"Storage: Error during cleanup - {e}")
        return 0

def backup_data():
    """Create backup of all data files"""
    try:
        import shutil
        from datetime import datetime
        
        backup_dir = f"data/backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        os.makedirs(backup_dir, exist_ok=True)
        
        files_backed_up = 0
        for file_path in [USERS_FILE, EVENTS_FILE, REGISTRATIONS_FILE]:
            if os.path.exists(file_path):
                filename = os.path.basename(file_path)
                shutil.copy2(file_path, os.path.join(backup_dir, filename))
                files_backed_up += 1
        
        Logger.info(f"Storage: Backed up {files_backed_up} files to {backup_dir}")
        return backup_dir
    except Exception as e:
        Logger.error(f"Storage: Error creating backup - {e}")
        return None

# Legacy compatibility functions (for existing code)
def save_registrations(registrations):
    """Save all registrations at once (legacy compatibility)"""
    ensure_data_dir()
    try:
        with open(REGISTRATIONS_FILE, "w", encoding='utf-8') as f:
            json.dump(registrations, f, indent=2, ensure_ascii=False)
        Logger.info("Storage: Saved all registrations")
        return True
    except Exception as e:
        Logger.error(f"Storage: Error saving registrations - {e}")
        return False

def save_events(events):
    """Save all events at once (legacy compatibility)"""
    ensure_data_dir()
    try:
        with open(EVENTS_FILE, "w", encoding='utf-8') as f:
            json.dump(events, f, indent=2, ensure_ascii=False)
        Logger.info("Storage: Saved all events")
        return True
    except Exception as e:
        Logger.error(f"Storage: Error saving events - {e}")
        return False

def save_users(users):
    """Save all users at once (legacy compatibility)"""
    ensure_data_dir()
    try:
        with open(USERS_FILE, "w", encoding='utf-8') as f:
            json.dump(users, f, indent=2, ensure_ascii=False)
        Logger.info("Storage: Saved all users")
        return True
    except Exception as e:
        Logger.error(f"Storage: Error saving users - {e}")
        return False

# Additional helper functions for app optimization
def validate_user_data(user_data):
    """Validate user data before saving"""
    required_fields = ['name', 'email', 'password']
    
    for field in required_fields:
        if not user_data.get(field):
            return False, f"Missing required field: {field}"
    
    # Email validation (basic)
    email = user_data.get('email', '')
    if '@' not in email or '.' not in email:
        return False, "Invalid email format"
    
    # Password strength (basic)
    password = user_data.get('password', '')
    if len(password) < 6:
        return False, "Password must be at least 6 characters"
    
    return True, "Valid"

def validate_event_data(event_data):
    """Validate event data before saving"""
    required_fields = ['title', 'description', 'date', 'location']
    
    for field in required_fields:
        if not event_data.get(field):
            return False, f"Missing required field: {field}"
    
    # Date validation (basic format check)
    date_str = event_data.get('date', '')
    if len(date_str) < 8:  # Basic length check
        return False, "Invalid date format"
    
    # Title length check
    title = event_data.get('title', '')
    if len(title) > 100:
        return False, "Title too long (max 100 characters)"
    
    # Description length check
    description = event_data.get('description', '')
    if len(description) > 1000:
        return False, "Description too long (max 1000 characters)"
    
    return True, "Valid"

def get_events_by_date_range(start_date, end_date):
    """Get events within a date range"""
    events = load_events()
    filtered_events = []
    
    for event in events:
        event_date = event.get('date', '')
        if start_date <= event_date <= end_date:
            filtered_events.append(event)
    
    return filtered_events

def get_upcoming_events(days_ahead=30):
    """Get upcoming events within specified days"""
    from datetime import datetime, timedelta
    
    today = datetime.now().date()
    end_date = today + timedelta(days=days_ahead)
    
    events = load_events()
    upcoming = []
    
    for event in events:
        try:
            # Assuming date format is YYYY-MM-DD
            event_date = datetime.strptime(event.get('date', ''), '%Y-%m-%d').date()
            if today <= event_date <= end_date:
                upcoming.append(event)
        except ValueError:
            # Skip events with invalid date format
            continue
    
    # Sort by date
    upcoming.sort(key=lambda x: x.get('date', ''))
    return upcoming

def is_user_registered(user_id, event_id):
    """Check if user is already registered for an event"""
    registrations = load_registrations()
    
    for reg in registrations:
        if (reg.get('user_id') == user_id and 
            reg.get('event_id') == event_id):
            return True
    
    return False

def get_registration_count(event_id):
    """Get number of registrations for an event"""
    registrations = load_registrations()
    count = 0
    
    for reg in registrations:
        if reg.get('event_id') == event_id:
            count += 1
    
    return count

# Privacy and GDPR compliance
def export_user_data(user_id):
    """Export all data for a specific user (GDPR compliance)"""
    try:
        user_data = {
            'events_created': [],
            'registrations': [],
            'export_date': datetime.now().isoformat()
        }
        
        # Get user's events
        events = load_events()
        user_events = [event for event in events if event.get('creator_id') == user_id]
        user_data['events_created'] = user_events
        
        # Get user's registrations
        registrations = load_registrations()
        user_registrations = [reg for reg in registrations if reg.get('user_id') == user_id]
        user_data['registrations'] = user_registrations
        
        return user_data
    except Exception as e:
        Logger.error(f"Storage: Error exporting user data - {e}")
        return None

def delete_user_data(user_id):
    """Delete all data for a specific user (GDPR compliance)"""
    try:
        deleted_items = {'users': 0, 'registrations': 0, 'events_deactivated': 0}
        
        # Remove user from users file
        users = load_users()
        original_user_count = len(users)
        users = [user for user in users if user.get('id') != user_id]
        deleted_items['users'] = original_user_count - len(users)
        
        if deleted_items['users'] > 0:
            with open(USERS_FILE, "w", encoding='utf-8') as f:
                json.dump(users, f, indent=2, ensure_ascii=False)
        
        # Remove user registrations
        registrations = load_registrations()
        original_reg_count = len(registrations)
        registrations = [reg for reg in registrations if reg.get('user_id') != user_id]
        deleted_items['registrations'] = original_reg_count - len(registrations)
        
        if deleted_items['registrations'] > 0:
            with open(REGISTRATIONS_FILE, "w", encoding='utf-8') as f:
                json.dump(registrations, f, indent=2, ensure_ascii=False)
        
        # Deactivate user's created events (don't delete to preserve other users' registrations)
        events = load_all_events()
        for event in events:
            if event.get('creator_id') == user_id:
                event['is_active'] = False
                event['creator_name'] = 'Deleted User'
                deleted_items['events_deactivated'] += 1
        
        if deleted_items['events_deactivated'] > 0:
            with open(EVENTS_FILE, "w", encoding='utf-8') as f:
                json.dump(events, f, indent=2, ensure_ascii=False)
        
        Logger.info(f"Storage: Deleted user data - {deleted_items}")
        return deleted_items
    except Exception as e:
        Logger.error(f"Storage: Error deleting user data - {e}")
        return None

# New helper functions for app store optimization
def get_app_data_size() -> Dict[str, int]:
    """Get size of app data for storage management"""
    sizes = {}
    data_files = ['events.json', 'users.json', 'registrations.json', 'categories.json']
    
    for filename in data_files:
        filepath = os.path.join('data', filename)
        if os.path.exists(filepath):
            sizes[filename] = os.path.getsize(filepath)
        else:
            sizes[filename] = 0
    
    return sizes

def cleanup_old_data(days_old: int = 30) -> bool:
    """Clean up old data for storage optimization"""
    try:
        from datetime import datetime, timedelta
        cutoff_date = datetime.now() - timedelta(days=days_old)
        
        # Clean up old events
        events = load_events()
        current_events = []
        
        for event in events:
            try:
                event_date = datetime.fromisoformat(event.get('date', ''))
                if event_date > cutoff_date or event.get('current_participants', 0) > 0:
                    current_events.append(event)
            except:
                # Keep events with invalid dates
                current_events.append(event)
        
        if len(current_events) != len(events):
            save_events(current_events)
            Logger.info(f"Storage: Cleaned up {len(events) - len(current_events)} old events")
        
        return True
    except Exception as e:
        Logger.error(f"Storage: Error cleaning up data - {e}")
        return False

def export_user_data(user_id: str) -> Optional[Dict]:
    """Export user data for privacy compliance"""
    try:
        user_data = {
            'events': [],
            'registrations': []
        }
        
        # Get user registrations
        registrations = load_registrations()
        user_registrations = [reg for reg in registrations if reg.get('user_id') == user_id]
        user_data['registrations'] = user_registrations
        
        # Get user created events
        events = load_events()
        user_events = [event for event in events if event.get('creator_id') == user_id]
        user_data['events'] = user_events
        
        return user_data
    except Exception as e:
        Logger.error(f"Storage: Error exporting user data - {e}")
        return None

def delete_user_data(user_id: str) -> bool:
    """Delete all user data for privacy compliance"""
    try:
        # Remove user registrations
        registrations = load_registrations()
        updated_registrations = [reg for reg in registrations if reg.get('user_id') != user_id]
        save_registrations(updated_registrations)
        
        # Remove user from users file
        users = load_users()
        updated_users = [user for user in users if user.get('id') != user_id]
        save_users(updated_users)
        
        Logger.info(f"Storage: Deleted data for user {user_id}")
        return True
    except Exception as e:
        Logger.error(f"Storage: Error deleting user data - {e}")
        return False