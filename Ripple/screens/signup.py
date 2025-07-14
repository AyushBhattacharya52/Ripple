from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.metrics import dp
from kivy.uix.popup import Popup
import re

from utils.storage import load_users, save_user

def is_valid_email(email):
    # Simple email regex
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email) is not None

class SignupScreen(Screen):
    def __init__(self, **kwargs):
        super(SignupScreen, self).__init__(**kwargs)

        self.layout = BoxLayout(orientation='vertical', padding=dp(40), spacing=dp(20))

        self.layout.add_widget(Label(text="Sign Up", font_size=32, size_hint=(1, 0.2)))

        self.username_input = TextInput(
            hint_text="Username",
            multiline=False,
            size_hint=(1, 0.15),
            write_tab=False
        )
        self.layout.add_widget(self.username_input)

        self.email_input = TextInput(
            hint_text="Email",
            multiline=False,
            size_hint=(1, 0.15),
            write_tab=False
        )
        self.layout.add_widget(self.email_input)

        self.password_input = TextInput(
            hint_text="Password",
            multiline=False,
            password=True,
            size_hint=(1, 0.15),
            write_tab=False
        )
        self.layout.add_widget(self.password_input)

        signup_btn = Button(text="Sign Up", size_hint=(1, 0.15), background_color=(0, 0.5, 1, 1))
        signup_btn.bind(on_release=self.sign_up)
        self.layout.add_widget(signup_btn)

        login_btn = Button(text="Already have an account? Login", size_hint=(1, 0.15), background_color=(0, 0, 0, 0))
        login_btn.bind(on_release=lambda x: setattr(self.manager, 'current', 'login'))
        self.layout.add_widget(login_btn)

        self.add_widget(self.layout)

    def sign_up(self, instance):
        username = self.username_input.text.strip()
        email = self.email_input.text.strip()
        password = self.password_input.text.strip()

        if not username or not email or not password:
            self.show_popup("Error", "All fields are required.")
            return

        if not is_valid_email(email):
            self.show_popup("Error", "Please enter a valid email address.")
            return

        users = load_users() or []
        clean_users = [u for u in users if u and isinstance(u, dict)]

        if any(u.get('username', '').lower() == username.lower() for u in clean_users):
            self.show_popup("Error", "Username already taken.")
            return

        if any(u.get('email', '').lower() == email.lower() for u in clean_users):
            self.show_popup("Error", "Email already registered.")
            return

        user = {
            'username': username,
            'email': email,
            'password': password
        }

        save_user(user)
        self.show_popup("Success", "Account created! Please log in.")
        self.manager.current = 'login'

    def show_popup(self, title, message):
        content = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        content.add_widget(Label(text=message))
        btn = Button(text='OK', size_hint=(1, 0.3))
        content.add_widget(btn)
        popup = Popup(title=title, content=content, size_hint=(0.7, 0.3))
        btn.bind(on_release=popup.dismiss)
        popup.open()
