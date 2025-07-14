# screens/main_page.py (updated)
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.metrics import dp
from kivy.uix.popup import Popup
from utils.storage import load_events

class MainPage(Screen):
    def __init__(self, **kwargs):
        super(MainPage, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        # Title
        title_label = Label(text="Ripple - Community Events", font_size=24, size_hint=(1, 0.1))
        self.layout.add_widget(title_label)

        # Events scroll view
        self.scroll = ScrollView(size_hint=(1, 0.7))
        self.events_grid = GridLayout(cols=1, size_hint_y=None, spacing=10)
        self.events_grid.bind(minimum_height=self.events_grid.setter('height'))
        self.scroll.add_widget(self.events_grid)
        self.layout.add_widget(self.scroll)

        # Button layout
        button_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.2), spacing=10)
        
        plus_btn = Button(text="Create Event", background_color=(0, 0.5, 1, 1))
        plus_btn.bind(on_release=lambda x: setattr(self.manager, 'current', 'create_event'))
        button_layout.add_widget(plus_btn)

        my_events_btn = Button(text="My Events", background_color=(0.5, 0.5, 0.5, 1))
        my_events_btn.bind(on_release=lambda x: setattr(self.manager, 'current', 'my_events'))
        button_layout.add_widget(my_events_btn)

        self.layout.add_widget(button_layout)
        self.add_widget(self.layout)

    def on_enter(self):
        self.load_events()

    def load_events(self):
        self.events_grid.clear_widgets()
        events = load_events()
        if not events:
            self.events_grid.add_widget(Label(text="No events available yet.", size_hint_y=None, height=dp(40)))
            return

        for event in events:
            title = event.get('title', 'No Title')
            date = event.get('date', '')
            location = event.get('location', 'No Location')

            event_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(120), padding=10)
            
            event_btn = Button(
                text=f"[b]{title}[/b]\nDate: {date}\nLocation: {location}",
                markup=True,
                size_hint_y=None,
                height=dp(80),
                background_normal='',
                background_color=(0.9, 0.9, 0.9, 1),
                color=(0, 0, 0, 1),
                halign='left',
                valign='middle'
            )
            event_btn.bind(on_release=lambda btn, ev=event: self.show_event_details(ev))
            event_layout.add_widget(event_btn)

            self.events_grid.add_widget(event_layout)

    def show_event_details(self, event):
        content = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))

        details = f"""[b]{event.get('title', 'No Title')}[/b]

Date: {event.get('date', 'N/A')}
Location: {event.get('location', 'N/A')}
Organizer: {event.get('name', 'N/A')}
Contact: {event.get('contact', 'N/A')}

Description:
{event.get('description', 'No Description')}"""

        label = Label(text=details, markup=True, text_size=(None, None), size_hint_y=None)
        label.bind(texture_size=lambda instance, value: setattr(label, 'height', value[1]))
        content.add_widget(label)

        btn_register = Button(text='Register for this Event', size_hint=(1, 0.3), background_color=(0, 0.5, 1, 1))
        content.add_widget(btn_register)

        btn_close = Button(text='Close', size_hint=(1, 0.3), background_color=(0.7, 0.7, 0.7, 1))
        content.add_widget(btn_close)

        popup = Popup(title="Event Details", content=content, size_hint=(0.8, 0.7))
        btn_close.bind(on_release=popup.dismiss)
        btn_register.bind(on_release=lambda x: self.register_for_event(event, popup))
        popup.open()

    def register_for_event(self, event, popup):
        popup.dismiss()
        self.manager.get_screen('event_registration').set_event(event)
        self.manager.current = 'event_registration'