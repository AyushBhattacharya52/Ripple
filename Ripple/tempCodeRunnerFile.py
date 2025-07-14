# main.py

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from screens.main_page import MainPage
from screens.create_event import CreateEventScreen
from screens.my_events import EventRegistrationScreen
from screens.my_events import MyEventsScreen

class RippleApp(App):
    def build(self):
        sm = ScreenManager()

        # Add all screens with correct names
        sm.add_widget(MainPage(name='main_page'))
        sm.add_widget(CreateEventScreen(name='create_event'))
        sm.add_widget(EventRegistrationScreen(name='event_registration'))
        sm.add_widget(MyEventsScreen(name='my_events'))

        return sm

if __name__ == '__main__':
    RippleApp().run()
