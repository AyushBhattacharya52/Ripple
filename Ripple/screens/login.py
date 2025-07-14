from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.metrics import dp
from kivy.uix.popup import Popup

from utils.storage import load_users

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)

        self.layout = BoxLayout(orientation='vertical', padding=dp(40), spacing=dp(20))
        
        self.layout.add_widget(Label(text="Login", font_size=32, size_hint=(1, 0.2)))

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

        login_btn = Button(text="Login", size_hint=(1, 0.15), background_color=(0, 0.5, 1, 1))
        login_btn.bind(on_release=self.validate_login)
        self.layout.add_widget(login_btn)

        signup_btn = Button(text="Don't have an account? Sign Up", size_hint=(1, 0.15), background_color=(0, 0, 0, 0))
        signup_btn.bind(on_release=lambda x: setattr(self.manager, 'current', 'signup'))
        self.layout.add_widget(signup_btn)

        self.add_widget(self.layout)

    def validate_login(self, instance):
        email = self.email_input.text.strip()
        password = self.password_input.text.strip()

        if not email or not password:
            self.show_popup("Error", "Please enter both email and password.")
            return

        users = load_users() or []
        clean_users = [u for u in users if u and isinstance(u, dict)]
        user = next((u for u in clean_users if u.get('email', '').lower() == email.lower() and u.get('password') == password), None)

        if user:
            # Successful login - switch to main page or dashboard
            self.manager.current = 'main'
        else:
            self.show_popup("Login Failed", "Incorrect email or password.")

    def show_popup(self, title, message):
        content = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        content.add_widget(Label(text=message))
        btn = Button(text='OK', size_hint=(1, 0.3))
        content.add_widget(btn)
        popup = Popup(title=title, content=content, size_hint=(0.7, 0.3))
        btn.bind(on_release=popup.dismiss)
        popup.open()
