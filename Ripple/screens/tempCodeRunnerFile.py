from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.metrics import dp
from kivy.uix.popup import Popup
from utils.storage import load_events, save_registration, load_registrations

class MainPage(Screen):
    def __init__(self, **kwargs):
        super(MainPage, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        self.scroll = ScrollView(size_hint=(1, 0.9))
        self.events_grid = GridLayout(cols=1, size_hint_y=None, spacing=10)
        self.events_grid.bind(minimum_height=self.events_grid.setter('height'))
        self.scroll.add_widget(self.events_grid)

        self.layout.add_widget(self.scroll)

        plus_btn = Button(text="+", size_hint=(1, 0.1), font_size=40, background_color=(0, 0.5, 1, 1))
        plus_btn.bind(on_release=lambda x: setattr(self.manager, 'current', 'create_event'))
        self.layout.add_widget(plus_btn)

        # Add a button to go to MyEvents screen (registered events)
        my_events_btn = Button(text="My Events", size_hint=(1, 0.1))
        my_events_btn.bind(on_release=lambda x: setattr(self.manager, 'current', 'my_events'))
        self.layout.add_widget(my_events_btn)

        self.add_widget(self.layout)

    def on_enter(self):
        self.load_events()

    def load_events(self):
        self.events_grid.clear_widgets()
        events = load_events()
        if not events:
            self.events_grid.add_widget(Label(text="No approved events yet.", size_hint_y=None, height=dp(40)))
            return

        for event in events:
            title = event.get('title', 'No Title')
            date = event.get('date', '')
            location = event.get('location', '')

            event_btn = Button(
                text=f"[b]{title}[/b]\nDate: {date}\nLocation: {location}",
                markup=True,
                size_hint_y=None,
                height=dp(80),
                background_normal='',
                background_color=(0, 0, 0, 0),
                halign='left',
                valign='middle'
            )
            event_btn.text_size = (self.width - 40, None)
            event_btn.bind(on_release=lambda btn, ev=event: self.show_event_details(ev))

            self.events_grid.add_widget(event_btn)

    def show_event_details(self, event):
        content = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))

        details = f"""
[b]{event.get('title', 'No Title')}[/b]

Date: {event.get('date', 'N/A')}
Name: {event.get('name', 'N/A')}
Contact: {event.get('contact', 'N/A')}
Description:
{event.get('description', 'No Description')}
"""
        label = Label(text=details, markup=True, size_hint_y=None)
        label.bind(texture_size=lambda instance, value: setattr(label, 'height', value[1]))
        content.add_widget(label)

        btn_register = Button(text='Register for this Event', size_hint=(1, 0.3))
        content.add_widget(btn_register)

        btn_close = Button(text='Close', size_hint=(1, 0.3))
        content.add_widget(btn_close)

        popup = Popup(title="Event Details", content=content, size_hint=(0.8, 0.6))
        btn_close.bind(on_release=popup.dismiss)
        btn_register.bind(on_release=lambda x: self.register_for_event(event, popup))
        popup.open()

    def register_for_event(self, event, popup):
        popup.dismiss()
        # Switch to registration screen with the selected event info
        self.manager.get_screen('event_registration').set_event(event)
        self.manager.current = 'event_registration'
