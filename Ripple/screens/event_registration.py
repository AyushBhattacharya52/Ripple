# screens/event_registration.py
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.metrics import dp
from kivy.uix.popup import Popup
from utils.storage import save_registration

class EventRegistrationScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.event = None
        
        self.layout = BoxLayout(orientation='vertical', padding=dp(40), spacing=dp(15))
        
        self.title_label = Label(text="Event Registration", font_size=32, size_hint=(1, 0.15))
        self.layout.add_widget(self.title_label)
        
        self.event_info_label = Label(text="", font_size=16, size_hint=(1, 0.2))
        self.layout.add_widget(self.event_info_label)
        
        self.name_input = TextInput(hint_text="Your Name", multiline=False, size_hint=(1, 0.1))
        self.layout.add_widget(self.name_input)
        
        self.email_input = TextInput(hint_text="Your Email", multiline=False, size_hint=(1, 0.1))
        self.layout.add_widget(self.email_input)
        
        self.phone_input = TextInput(hint_text="Your Phone Number", multiline=False, size_hint=(1, 0.1))
        self.layout.add_widget(self.phone_input)
        
        register_btn = Button(text="Register", size_hint=(1, 0.15), background_color=(0, 0.5, 1, 1))
        register_btn.bind(on_release=self.register)
        self.layout.add_widget(register_btn)
        
        back_btn = Button(text="Back", size_hint=(1, 0.15), background_color=(0.7, 0.7, 0.7, 1))
        back_btn.bind(on_release=self.go_back)
        self.layout.add_widget(back_btn)
        
        self.add_widget(self.layout)
    
    def set_event(self, event):
        self.event = event
        self.event_info_label.text = f"Registering for: {event.get('title', 'N/A')}\nDate: {event.get('date', 'N/A')}"
    
    def register(self, instance):
        if not self.event:
            self.show_popup("Error", "No event selected.")
            return
            
        name = self.name_input.text.strip()
        email = self.email_input.text.strip()
        phone = self.phone_input.text.strip()
        
        if not (name and email and phone):
            self.show_popup("Error", "Please fill out all fields.")
            return
        
        registration = {
            'event_title': self.event.get('title', ''),
            'event_date': self.event.get('date', ''),
            'name': name,
            'email': email,
            'phone': phone
        }
        
        save_registration(registration)
        self.show_popup("Success", "Successfully registered for the event!")
        
        # Clear form
        self.name_input.text = ""
        self.email_input.text = ""
        self.phone_input.text = ""
        
        # Go back to main page
        self.manager.current = 'main'
    
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
