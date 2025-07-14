# screens/my_events.py (updated)
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.metrics import dp
from kivy.uix.button import Button
from utils.storage import load_registrations

class MyEventsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))

        # Title
        title_label = Label(text="My Registered Events", font_size=24, size_hint=(1, 0.1))
        self.layout.add_widget(title_label)

        # Events scroll view
        self.scroll = ScrollView(size_hint=(1, 0.8))
        self.events_grid = GridLayout(cols=1, size_hint_y=None, spacing=dp(10))
        self.events_grid.bind(minimum_height=self.events_grid.setter('height'))
        self.scroll.add_widget(self.events_grid)
        self.layout.add_widget(self.scroll)

        # Back button
        back_btn = Button(text="Back to Events", size_hint=(1, 0.1), background_color=(0.7, 0.7, 0.7, 1))
        back_btn.bind(on_release=lambda x: setattr(self.manager, 'current', 'main'))
        self.layout.add_widget(back_btn)

        self.add_widget(self.layout)

    def on_enter(self):
        self.load_my_events()

    def load_my_events(self):
        self.events_grid.clear_widgets()
        registrations = load_registrations()
        if not registrations:
            self.events_grid.add_widget(Label(text="You have not registered for any events yet.", size_hint_y=None, height=dp(40)))
            return

        for reg in registrations:
            event_title = reg.get('event_title', 'No Title')
            event_date = reg.get('event_date', 'N/A')
            name = reg.get('name', 'N/A')
            email = reg.get('email', 'N/A')
            phone = reg.get('phone', 'N/A')

            text = f"[b]{event_title}[/b]\nDate: {event_date}\nRegistered as: {name}\nEmail: {email}\nPhone: {phone}"
            
            event_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(120), padding=10)
            
            label = Label(
                text=text, 
                markup=True, 
                size_hint_y=None, 
                height=dp(100),
                background_color=(0.9, 0.9, 0.9, 1),
                color=(0, 0, 0, 1)
            )
            event_layout.add_widget(label)
            self.events_grid.add_widget(event_layout)
