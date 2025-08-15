from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.metrics import dp, sp
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle, Ellipse
from kivy.animation import Animation
import re

from utils.storage import load_users, save_user

def is_valid_email(email):
    # Simple email regex
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email) is not None

class FloatingElement(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            Color(0.2, 0.6, 0.9, 0.1)
            self.circle = Ellipse(size=(dp(60), dp(60)), pos=self.pos)
        
        self.bind(pos=self._update_circle)
        
        # Start floating animation
        self.start_animation()
    
    def _update_circle(self, *args):
        self.circle.pos = self.pos
    
    def start_animation(self):
        # Create floating effect
        anim = Animation(y=self.y + dp(20), duration=2.0) + Animation(y=self.y - dp(20), duration=2.0)
        anim.repeat = True
        anim.start(self)

class SignupScreen(Screen):
    def __init__(self, **kwargs):
        super(SignupScreen, self).__init__(**kwargs)
        
        # Create light background to match theme
        with self.canvas.before:
            Color(0.97, 0.99, 1, 1)  # Very light blue background
            self.bg_rect = Rectangle(size=self.size, pos=self.pos)
        
        self.bind(size=self._update_bg, pos=self._update_bg)
        
        # Create main container with floating elements
        main_container = FloatLayout()
        
        # Add floating background elements
        self._add_floating_elements(main_container)
        
        # Main scrollable container for mobile compatibility
        main_layout = BoxLayout(
            orientation='vertical', 
            padding=[dp(30), dp(40), dp(30), dp(40)], 
            spacing=dp(25)
        )
        
        # Top spacer for vertical centering
        main_layout.add_widget(Widget(size_hint_y=0.2))
        
        # Header section
        header_layout = BoxLayout(
            orientation='vertical', 
            spacing=dp(10), 
            size_hint_y=None, 
            height=dp(100)
        )
        
        # App title
        title_label = Label(
            text="Join Ripple",
            font_size=sp(32),
            bold=True,
            color=(0.17, 0.24, 0.31, 1),  # Matching theme dark blue-gray
            size_hint_y=None,
            height=dp(50)
        )
        header_layout.add_widget(title_label)
        
        # Subtitle
        subtitle_label = Label(
            text="Create your account to start making a difference",
            font_size=sp(16),
            color=(0.2, 0.6, 0.9, 1),  # Matching theme brand blue
            size_hint_y=None,
            height=dp(30)
        )
        header_layout.add_widget(subtitle_label)
        
        main_layout.add_widget(header_layout)
        
        # Form container
        form_layout = BoxLayout(
            orientation='vertical', 
            spacing=dp(20),
            size_hint_y=None
        )
        form_layout.bind(minimum_height=form_layout.setter('height'))
        
        # Username section
        username_section = BoxLayout(orientation='vertical', spacing=dp(8), size_hint_y=None, height=dp(80))
        
        username_label = Label(
            text="Username",
            font_size=sp(16),
            color=(0.3, 0.3, 0.3, 1),
            size_hint_y=None,
            height=dp(25),
            halign='left',
            bold=True
        )
        username_label.bind(size=username_label.setter('text_size'))
        username_section.add_widget(username_label)
        
        self.username_input = TextInput(
            hint_text="Choose a username",
            multiline=False,
            size_hint_y=None,
            height=dp(50),
            font_size=sp(16),
            padding=[dp(15), dp(15)],
            background_color=(0.97, 0.97, 0.97, 1),
            foreground_color=(0.2, 0.2, 0.2, 1),
            cursor_color=(0.2, 0.6, 0.9, 1),
            selection_color=(0.2, 0.6, 0.9, 0.3),
            write_tab=False
        )
        username_section.add_widget(self.username_input)
        form_layout.add_widget(username_section)
        
        # Email section
        email_section = BoxLayout(orientation='vertical', spacing=dp(8), size_hint_y=None, height=dp(80))
        
        email_label = Label(
            text="Email Address",
            font_size=sp(16),
            color=(0.3, 0.3, 0.3, 1),
            size_hint_y=None,
            height=dp(25),
            halign='left',
            bold=True
        )
        email_label.bind(size=email_label.setter('text_size'))
        email_section.add_widget(email_label)
        
        self.email_input = TextInput(
            hint_text="Enter your email address",
            multiline=False,
            size_hint_y=None,
            height=dp(50),
            font_size=sp(16),
            padding=[dp(15), dp(15)],
            background_color=(0.97, 0.97, 0.97, 1),
            foreground_color=(0.2, 0.2, 0.2, 1),
            cursor_color=(0.2, 0.6, 0.9, 1),
            selection_color=(0.2, 0.6, 0.9, 0.3),
            write_tab=False
        )
        email_section.add_widget(self.email_input)
        form_layout.add_widget(email_section)
        
        # Password section
        password_section = BoxLayout(orientation='vertical', spacing=dp(8), size_hint_y=None, height=dp(80))
        
        password_label = Label(
            text="Password",
            font_size=sp(16),
            color=(0.3, 0.3, 0.3, 1),
            size_hint_y=None,
            height=dp(25),
            halign='left',
            bold=True
        )
        password_label.bind(size=password_label.setter('text_size'))
        password_section.add_widget(password_label)
        
        self.password_input = TextInput(
            hint_text="Create a secure password",
            multiline=False,
            password=True,
            size_hint_y=None,
            height=dp(50),
            font_size=sp(16),
            padding=[dp(15), dp(15)],
            background_color=(0.97, 0.97, 0.97, 1),
            foreground_color=(0.2, 0.2, 0.2, 1),
            cursor_color=(0.2, 0.6, 0.9, 1),
            selection_color=(0.2, 0.6, 0.9, 0.3),
            write_tab=False
        )
        password_section.add_widget(self.password_input)
        form_layout.add_widget(password_section)
        
        # Password requirements hint
        password_hint = Label(
            text="Password should be at least 6 characters long",
            font_size=sp(12),
            color=(0.5, 0.55, 0.6, 1),
            size_hint_y=None,
            height=dp(20),
            halign='left'
        )
        password_hint.bind(size=password_hint.setter('text_size'))
        form_layout.add_widget(password_hint)
        
        # Buttons section
        button_layout = BoxLayout(orientation='vertical', spacing=dp(15), size_hint_y=None, height=dp(120))
        
        # Signup button
        self.signup_btn = Button(
            text="Create Account",
            size_hint_y=None,
            height=dp(50),
            font_size=sp(18),
            bold=True,
            background_color=(0.2, 0.6, 0.9, 1),  # Matching theme
            color=(1, 1, 1, 1)
        )
        self.signup_btn.bind(on_release=self.sign_up)
        button_layout.add_widget(self.signup_btn)
        
        # Login button
        login_btn = Button(
            text="Already have an account? Sign In",
            size_hint_y=None,
            height=dp(50),
            font_size=sp(18),
            bold=True,
            background_color=(0.2, 0.6, 0.9, 1),  # Matching theme
            color=(1, 1, 1, 1)
        )
        login_btn.bind(on_release=lambda x: setattr(self.manager, 'current', 'login'))
        button_layout.add_widget(login_btn)
        
        form_layout.add_widget(button_layout)
        main_layout.add_widget(form_layout)
        
        # Bottom spacer
        main_layout.add_widget(Widget(size_hint_y=0.2))
        
        # Footer
        footer_label = Label(
            text="By signing up, you agree to make a positive impact",
            font_size=sp(12),
            color=(0.6, 0.6, 0.6, 1),
            size_hint_y=None,
            height=dp(25)
        )
        main_layout.add_widget(footer_label)
        
        # Add main layout to container
        main_container.add_widget(main_layout)
        self.add_widget(main_container)
        
        # Keyboard navigation
        self.username_input.bind(on_text_validate=self.focus_email)
        self.email_input.bind(on_text_validate=self.focus_password)
        self.password_input.bind(on_text_validate=self.sign_up)
    
    def _add_floating_elements(self, layout):
        """Add floating decorative elements matching the theme"""
        positions = [
            (0.15, 0.85), (0.85, 0.75), (0.05, 0.4), (0.9, 0.25), (0.1, 0.1)
        ]
        
        for pos in positions:
            element = FloatingElement(
                size_hint=(None, None),
                size=(dp(60), dp(60)),
                pos_hint={'x': pos[0], 'y': pos[1]}
            )
            layout.add_widget(element)
    
    def _update_bg(self, *args):
        """Update background when screen size changes"""
        self.bg_rect.size = self.size
        self.bg_rect.pos = self.pos
    
    def focus_email(self, instance):
        """Move focus to email field when enter is pressed in username field"""
        self.email_input.focus = True
    
    def focus_password(self, instance):
        """Move focus to password field when enter is pressed in email field"""
        self.password_input.focus = True
    
    def sign_up(self, instance):
        username = self.username_input.text.strip()
        email = self.email_input.text.strip()
        password = self.password_input.text.strip()

        # Show loading state
        self.show_loading_state(True)

        # Validation
        if not username or not email or not password:
            self.show_loading_state(False)
            self.show_popup("Missing Information", "All fields are required.")
            return

        if len(username) < 3:
            self.show_loading_state(False)
            self.show_popup("Invalid Username", "Username must be at least 3 characters long.")
            return

        if not is_valid_email(email):
            self.show_loading_state(False)
            self.show_popup("Invalid Email", "Please enter a valid email address.")
            return

        if len(password) < 6:
            self.show_loading_state(False)
            self.show_popup("Weak Password", "Password must be at least 6 characters long.")
            return

        # Check for existing users
        try:
            users = load_users() or []
            clean_users = [u for u in users if u and isinstance(u, dict)]

            if any(u.get('username', '').lower() == username.lower() for u in clean_users):
                self.show_loading_state(False)
                self.show_popup("Username Taken", "This username is already taken. Please choose another.")
                return

            if any(u.get('email', '').lower() == email.lower() for u in clean_users):
                self.show_loading_state(False)
                self.show_popup("Email Registered", "This email is already registered. Please use a different email or sign in.")
                return

            # Create new user
            user = {
                'username': username,
                'email': email,
                'password': password
            }

            save_user(user)
            
            # Simulate brief delay for better UX
            Clock.schedule_once(lambda dt: self.complete_signup(), 0.5)
            
        except Exception as e:
            self.show_loading_state(False)
            self.show_popup("Error", f"An error occurred: {str(e)}")
    
    def complete_signup(self):
        self.show_loading_state(False)
        self.show_popup("Welcome to Ripple!", "Account created successfully! Please sign in to continue.")
        # Clear form
        self.username_input.text = ""
        self.email_input.text = ""
        self.password_input.text = ""
        # Redirect to login after showing success
        Clock.schedule_once(lambda dt: setattr(self.manager, 'current', 'login'), 2.0)
    
    def show_loading_state(self, loading):
        """Show/hide loading state by disabling inputs and changing button text"""
        self.username_input.disabled = loading
        self.email_input.disabled = loading
        self.password_input.disabled = loading
        self.signup_btn.disabled = loading
        
        if loading:
            self.signup_btn.text = "Creating Account..."
            self.signup_btn.background_color = (0.7, 0.7, 0.7, 1)
        else:
            self.signup_btn.text = "Create Account"
            self.signup_btn.background_color = (0.2, 0.6, 0.9, 1)

    def show_popup(self, title, message):
        """Show a themed popup message"""
        content = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
        
        # Message label with text wrapping
        msg_label = Label(
            text=message,
            font_size=sp(16),
            color=(0, 0, 0, 1),  # Black text
            text_size=(dp(250), None),
            halign='center',
            valign='middle'
        )
        content.add_widget(msg_label)
        
        # OK button
        ok_btn = Button(
            text='OK',
            size_hint_y=None,
            height=dp(45),
            font_size=sp(16),
            background_color=(0.2, 0.6, 0.9, 1),  # Matching theme
            color=(1, 1, 1, 1)
        )
        content.add_widget(ok_btn)
        
        popup = Popup(
            title=title,
            title_size=sp(18),
            title_color=(0, 0, 0, 1),  # Black title
            content=content,
            size_hint=(0.8, None),
            height=dp(180),
            auto_dismiss=False
        )
        
        ok_btn.bind(on_release=popup.dismiss)
        popup.open()