# main.py
from kivy.config import Config
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
from kivy.app import App
from kivy.uix.label import Label
# other Kivy imports you already use
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.clock import Clock
from kivy.logger import Logger
from screens.start import StartScreen
from screens.signup import SignupScreen
from screens.login import LoginScreen
from screens.main_page import MainPage
from screens.create_event import CreateEventScreen
from screens.event_registration import EventRegistrationScreen
from screens.my_events import MyEventsScreen
from utils.data_manager import DataManager
from utils.location_services import LocationService
import os
from utils.data_manager import DataManager




class RippleApp(App):
    def __init__(self, **kwargs):
        
        super().__init__(**kwargs)
        self.data_manager = None
        self.location_service = None
        self.current_user = None
        self.user_location = None
        
    def build(self):
        self.setup_directories()
        self.initialize_services()
        
        # Create screen manager
        sm = ScreenManager()
        
        # Store reference to app in screen manager for easy access
        sm.app = self

        # Add all screens with correct names
        sm.add_widget(StartScreen(name='start'))
        sm.add_widget(SignupScreen(name='signup'))
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(MainPage(name='main'))
        sm.add_widget(CreateEventScreen(name='create_event'))
        sm.add_widget(EventRegistrationScreen(name='event_registration'))
        sm.add_widget(MyEventsScreen(name='my_events'))

        # Start with the start screen
        sm.current = 'start'
        
        # Schedule location update
        Clock.schedule_once(self.update_location, 2)
        
        return sm
    
    def setup_directories(self):
        """Create necessary directories for data storage"""
        directories = ['data', 'data/users', 'data/events', 'data/registrations']
        for directory in directories:
            if not os.path.exists(directory):
                os.makedirs(directory)
                Logger.info(f"RippleApp: Created directory {directory}")
    
    def initialize_services(self):
        """Initialize data manager and location service"""
        try:
            self.data_manager = DataManager()
            self.location_service = LocationService()
            Logger.info("RippleApp: Services initialized successfully")
        except Exception as e:
            Logger.error(f"RippleApp: Error initializing services: {e}")
    
    def update_location(self, dt=None):
        """Update user location for location-based features"""
        if self.location_service:
            self.location_service.get_location(self.on_location_update)
    
    def on_location_update(self, location_data):
        """Callback for location updates"""
        if location_data:
            self.user_location = location_data
            Logger.info(f"RippleApp: Location updated - {location_data.get('city', 'Unknown')}")
            
            # Refresh events in main screen if it's currently displayed
            if hasattr(self.root, 'current') and self.root.current == 'main':
                main_screen = self.root.get_screen('main')
                if hasattr(main_screen, 'refresh_events'):
                    main_screen.refresh_events()
    
    def get_events_by_location(self, radius_km=50):
        """Get events filtered by user location"""
        if not self.data_manager:
            return []
        
        all_events = self.data_manager.get_all_events()
        
        if not self.user_location or not all_events:
            return all_events
        
        # Filter events by location
        filtered_events = []
        user_lat = self.user_location.get('latitude')
        user_lon = self.user_location.get('longitude')
        
        if user_lat and user_lon:
            for event in all_events:
                event_lat = event.get('latitude')
                event_lon = event.get('longitude')
                
                if event_lat and event_lon:
                    distance = self.location_service.calculate_distance(
                        user_lat, user_lon, event_lat, event_lon
                    )
                    if distance <= radius_km:
                        event['distance'] = round(distance, 1)
                        filtered_events.append(event)
                else:
                    # Include events without location data
                    event['distance'] = None
                    filtered_events.append(event)
        else:
            filtered_events = all_events
        
        # Sort by distance (events with distance first, then others)
        filtered_events.sort(key=lambda x: (x['distance'] is None, x.get('distance', float('inf'))))
        
        return filtered_events
    
    def get_user_events(self):
        """Get events registered by current user"""
        if not self.current_user or not self.data_manager:
            return []
        
        return self.data_manager.get_user_registrations(self.current_user['id'])
    
    def create_event(self, event_data):
        """Create a new event"""
        if not self.data_manager or not self.current_user:
            return False
        
        # Add creator information
        event_data['creator_id'] = self.current_user['id']
        event_data['creator_name'] = self.current_user['name']
        
        # Add location if available
        if self.user_location:
            event_data.update({
                'latitude': self.user_location.get('latitude'),
                'longitude': self.user_location.get('longitude'),
                'city': self.user_location.get('city'),
                'country': self.user_location.get('country')
            })
        
        return self.data_manager.create_event(event_data)
    
    def register_for_event(self, event_id, registration_data):
        """Register user for an event"""
        if not self.data_manager or not self.current_user:
            return False
        
        registration_data['user_id'] = self.current_user['id']
        registration_data['event_id'] = event_id
        
        return self.data_manager.register_for_event(registration_data)
    
    def login_user(self, email, password):
        """Authenticate user login"""
        if not self.data_manager:
            return None
        
        user = self.data_manager.authenticate_user(email, password)
        if user:
            self.current_user = user
            Logger.info(f"RippleApp: User logged in - {user['name']}")
        
        return user
    
    def signup_user(self, user_data):
        """Register a new user"""
        if not self.data_manager:
            return None
        
        user = self.data_manager.create_user(user_data)
        if user:
            self.current_user = user
            Logger.info(f"RippleApp: New user registered - {user['name']}")
        
        return user
    
    def logout_user(self):
        """Logout current user"""
        if self.current_user:
            Logger.info(f"RippleApp: User logged out - {self.current_user['name']}")
            self.current_user = None
    
    def get_event_by_id(self, event_id):
        """Get specific event by ID"""
        if not self.data_manager:
            return None
        
        return self.data_manager.get_event_by_id(event_id)
    
    def search_events(self, query, category=None):
        """Search events by title, description, or category"""
        if not self.data_manager:
            return []
        
        return self.data_manager.search_events(query, category)
    
    def get_event_categories(self):
        """Get all available event categories"""
        if not self.data_manager:
            return []
        
        return self.data_manager.get_categories()
    
    def update_user_preferences(self, preferences):
        """Update user preferences for better event recommendations"""
        if not self.current_user or not self.data_manager:
            return False
        
        return self.data_manager.update_user_preferences(self.current_user['id'], preferences)
    
    def get_recommended_events(self):
        """Get recommended events based on user preferences and location"""
        if not self.current_user or not self.data_manager:
            return self.get_events_by_location()
        
        # Get events by location first
        location_events = self.get_events_by_location()
        
        # Apply user preferences filtering if available
        user_preferences = self.current_user.get('preferences', {})
        if user_preferences:
            preferred_categories = user_preferences.get('categories', [])
            if preferred_categories:
                filtered_events = [
                    event for event in location_events
                    if event.get('category') in preferred_categories
                ]
                if filtered_events:
                    return filtered_events
        
        return location_events
    
    def on_pause(self):
        """Handle app pause (mobile)"""
        return True
    
    def on_resume(self):
        """Handle app resume (mobile)"""
        # Update location when app resumes
        Clock.schedule_once(self.update_location, 1)

# App Store optimization
RippleApp.__version__ = '1.0.0'
RippleApp.title = 'Ripple Events'
RippleApp.icon = 'assets\logo.png'

# Make sure to add your app icon

if __name__ == '__main__':
    RippleApp().run()