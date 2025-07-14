# screens/create_event.py (updated)
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.metrics import dp
from kivy.uix.popup import Popup

from utils.email_sender import send_event_email
from utils.storage import save_event

class CreateEventScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.layout = BoxLayout(orientation='vertical', padding=dp(40), spacing=dp(15))

        self.layout.add_widget(Label(text="Create Event", font_size=32, size_hint=(1, 0.15)))

        self.name_input = TextInput(hint_text="Organizer Name", multiline=False, size_hint=(1, 0.1))
        self.layout.add_widget(self.name_input)

        self.contact_input = TextInput(hint_text="Contact Info (email or phone)", multiline=False, size_hint=(1, 0.1))
        self.layout.add_widget(self.contact_input)

        self.date_input = TextInput(hint_text="Event Date (YYYY-MM-DD)", multiline=False, size_hint=(1, 0.1))
        self.layout.add_widget(self.date_input)

        self.title_input = TextInput(hint_text="Event Title", multiline=False, size_hint=(1, 0.1))
        self.layout.add_widget(self.title_input)

        self.location_input = TextInput(hint_text="Event Location", multiline=False, size_hint=(1, 0.1))
        self.layout.add_widget(self.location_input)

        self.description_input = TextInput(hint_text="Event Description", multiline=True, size_hint=(1, 0.25))
        self.layout.add_widget(self.description_input)

        submit_btn = Button(text="Submit", size_hint=(1, 0.15), background_color=(0, 0.5, 1, 1))
        submit_btn.bind(on_release=self.submit_event)
        self.layout.add_widget(submit_btn)

        back_btn = Button(text="Back", size_hint=(1, 0.15), background_color=(0.7, 0.7, 0.7, 1))
        back_btn.bind(on_release=self.go_back)
        self.layout.add_widget(back_btn)

        self.add_widget(self.layout)

    def submit_event(self, instance):
        name = self.name_input.text.strip()
        contact = self.contact_input.text.strip()
        date = self.date_input.text.strip()
        title = self.title_input.text.strip()
        location = self.location_input.text.strip()
        description = self.description_input.text.strip()

        if not (name and contact and date and title and location and description):
            self.show_popup("Error", "Please fill out all fields.")
            return

        event = {
            'name': name,
            'contact': contact,
            'date': date,
            'title': title,
            'location': location,
            'description': description
        }

        save_event(event)

        # Optional: Send email notification
        recipient_email = "admin@rippleapp.com"  # Change to actual admin email
        try:
            success = send_event_email(title, date, recipient_email)
            if success:
                self.show_popup("Success", "Event created and notification sent!")
            else:
                self.show_popup("Success", "Event created! (Email notification failed)")
        except:
            self.show_popup("Success", "Event created!")

        # Clear form
        self.name_input.text = ""
        self.contact_input.text = ""
        self.date_input.text = ""
        self.title_input.text = ""
        self.location_input.text = ""
        self.description_input.text = ""

    def go_back(self, instance):
        self.manager.current = 'main'

    def show_popup(self, title, message):
        content = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        content.add_widget(Label(text=message))
        btn = Button(text='OK', size_hint=(1, 0.3))
        content.add_widget(btn)
        popup = Popup(title=title, content=content, size_hint=(0.7, 0.3))
        btn.bind(on_release=popup.dismiss)
        popup.open()