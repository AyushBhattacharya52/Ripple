from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.config import Config

# Configure the app before importing other modules
Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '600')
Config.set('graphics', 'minimum_width', '350')
Config.set('graphics', 'minimum_height', '500')

# Import your screen classes
from screens.start import StartScreen
from screens.signup import SignupScreen
from screens.login import LoginScreen
from screens.main_page import MainPage
from screens.create_event import CreateEventScreen
from screens.my_events import MyEventsScreen
from screens.event_registration import EventRegistrationScreen

class RippleApp(App):
    def build(self):
        # Create the screen manager
        sm = ScreenManager()
        
        # Add the start screen (first screen)
        start_screen = StartScreen(name='start')
        sm.add_widget(start_screen)
        
        # Add the signup screen
        signup_screen = SignupScreen(name='signup')
        sm.add_widget(signup_screen)
        
        # Add the login screen
        login_screen = LoginScreen(name='login')
        sm.add_widget(login_screen)
        
        # Add the main page (home/events list)
        main_page = MainPage(name='main')
        sm.add_widget(main_page)
        
        # Add the create event screen
        create_event_screen = CreateEventScreen(name='create_event')
        sm.add_widget(create_event_screen)
        
        # Add the my events screen
        my_events_screen = MyEventsScreen(name='my_events')
        sm.add_widget(my_events_screen)
        
        # Add the event registration screen
        event_registration_screen = EventRegistrationScreen(name='event_registration')
        sm.add_widget(event_registration_screen)
        
        # Set the initial screen
        sm.current = 'start'  # Start with the start screen
        
        return sm

if __name__ == '__main__':
    RippleApp().run()