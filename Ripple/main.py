# main.py
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from screens.start import StartScreen
from screens.signup import SignupScreen
from screens.login import LoginScreen
from screens.main_page import MainPage
from screens.create_event import CreateEventScreen
from screens.event_registration import EventRegistrationScreen
from screens.my_events import MyEventsScreen
import os

class RippleApp(App):
    def build(self):
        # Create data directory if it doesn't exist
        if not os.path.exists('data'):
            os.makedirs('data')
        
        sm = ScreenManager()

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
        return sm

if __name__ == '__main__':
    RippleApp().run()