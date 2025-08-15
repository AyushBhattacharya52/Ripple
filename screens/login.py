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

from utils.storage import load_users

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

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        
        # Create light background to match start screen
        from kivy.graphics import Color, Rectangle
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
        main_layout.add_widget(Widget(size_hint_y=0.3))
        
        # Header section
        header_layout = BoxLayout(
            orientation='vertical', 
            spacing=dp(10), 
            size_hint_y=None, 
            height=dp(100)
        )
        
        # App title
        title_label = Label(
            text="Welcome Back",
            font_size=sp(32),
            bold=True,
            color=(0.17, 0.24, 0.31, 1),  # Matching start screen dark blue-gray
            size_hint_y=None,
            height=dp(50)
        )
        header_layout.add_widget(title_label)
        
        # Subtitle
        subtitle_label = Label(
            text="Sign in to continue",
            font_size=sp(18),
            color=(0.2, 0.6, 0.9, 1),  # Matching start screen brand blue
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
            cursor_color=(0.3, 0.6, 1, 1),
            selection_color=(0.3, 0.6, 1, 0.3),
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
            hint_text="Enter your password",
            multiline=False,
            password=True,
            size_hint_y=None,
            height=dp(50),
            font_size=sp(16),
            padding=[dp(15), dp(15)],
            background_color=(0.97, 0.97, 0.97, 1),
            foreground_color=(0.2, 0.2, 0.2, 1),
            cursor_color=(0.3, 0.6, 1, 1),
            selection_color=(0.3, 0.6, 1, 0.3),
            write_tab=False
        )
        password_section.add_widget(self.password_input)
        form_layout.add_widget(password_section)
        
        # Buttons section
        button_layout = BoxLayout(orientation='vertical', spacing=dp(15), size_hint_y=None, height=dp(120))
        
        # Login button
        self.login_btn = Button(
            text="Sign In",
            size_hint_y=None,
            height=dp(50),
            font_size=sp(18),
            bold=True,
            background_color=(0.2, 0.6, 0.9, 1),  # Matching your start screen theme
            color=(1, 1, 1, 1)
        )
        self.login_btn.bind(on_release=self.validate_login)
        button_layout.add_widget(self.login_btn)
        
        # Sign up button
        signup_btn = Button(
            text="Create New Account",
            size_hint_y=None,
            height=dp(50),
            font_size=sp(18),
            bold=True,
            background_color=(0.2, 0.6, 0.9, 1),  # Matching your start screen theme
            color=(1, 1, 1, 1)
        )
    
        signup_btn.bind(on_release=lambda x: setattr(self.manager, 'current', 'signup'))
        button_layout.add_widget(signup_btn)
        
        form_layout.add_widget(button_layout)
        main_layout.add_widget(form_layout)
        
        # Bottom spacer
        main_layout.add_widget(Widget(size_hint_y=0.3))
        
        # Footer
        footer_label = Label(
            text="Secure • Private • Reliable",
            font_size=sp(14),
            color=(0.6, 0.6, 0.6, 1),
            size_hint_y=None,
            height=dp(25)
        )
        main_layout.add_widget(footer_label)
        
        # Add main layout to container
        main_container.add_widget(main_layout)
        self.add_widget(main_container)
        
        # Keyboard navigation
        self.email_input.bind(on_text_validate=self.focus_password)
        self.password_input.bind(on_text_validate=self.validate_login)
    
    def _add_floating_elements(self, layout):
        """Add floating decorative elements like in start screen"""
        positions = [
            (0.1, 0.8), (0.9, 0.7), (0.05, 0.3), (0.85, 0.2)
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
    
    def focus_password(self, instance):
        """Move focus to password field when enter is pressed in email field"""
        self.password_input.focus = True
    
    def validate_login(self, instance):
        email = self.email_input.text.strip()
        password = self.password_input.text.strip()

        # Show loading state
        self.show_loading_state(True)

        # Debug: Print input values
        print(f"DEBUG: Email input: '{email}'")
        print(f"DEBUG: Password input: '{password}'")

        if not email or not password:
            self.show_loading_state(False)
            self.show_popup("Missing Information", "Please enter both email and password.")
            return

        # Basic email validation
        if '@' not in email or '.' not in email.split('@')[-1]:
            self.show_loading_state(False)
            self.show_popup("Invalid Email", "Please enter a valid email address.")
            return

        # Debug: Try to load users
        try:
            users = load_users()
            print(f"DEBUG: Raw users data: {users}")
            print(f"DEBUG: Users type: {type(users)}")
        except Exception as e:
            print(f"DEBUG: Error loading users: {e}")
            self.show_loading_state(False)
            self.show_popup("Connection Error", f"Could not load user data: {str(e)}")
            return

        # Handle case where users is None or not a list
        if users is None:
            print("DEBUG: No users data found")
            self.show_loading_state(False)
            self.show_popup("No Accounts Found", "No user accounts found. Please sign up first.")
            return
        
        if not isinstance(users, list):
            print(f"DEBUG: Users data is not a list, it's: {type(users)}")
            self.show_loading_state(False)
            self.show_popup("Data Error", "Invalid user data format.")
            return

        # Clean and debug users
        clean_users = [u for u in users if u and isinstance(u, dict)]
        print(f"DEBUG: Clean users count: {len(clean_users)}")
        
        for i, user in enumerate(clean_users):
            print(f"DEBUG: User {i}: {user}")
        
        # Try to find matching user with detailed debugging
        matching_user = None
        for user in clean_users:
            user_email = user.get('email', '').lower().strip()
            user_password = user.get('password', '').strip()
            
            print(f"DEBUG: Comparing '{email.lower()}' with '{user_email}'")
            print(f"DEBUG: Comparing passwords: '{password}' with '{user_password}'")
            
            if user_email == email.lower() and user_password == password:
                matching_user = user
                break
        
        # Simulate a brief delay for better UX
        Clock.schedule_once(lambda dt: self.complete_login(matching_user), 0.5)
    
    def complete_login(self, matching_user):
        self.show_loading_state(False)
        
        if matching_user:
            print("DEBUG: Login successful!")
            self.show_popup("Success", "Login successful! Welcome back.")
            # Redirect after showing success message
            Clock.schedule_once(lambda dt: setattr(self.manager, 'current', 'main'), 1.5)
        else:
            print("DEBUG: Login failed - no matching user found")
            self.show_popup("Login Failed", "Incorrect email or password. Please try again.")
    
    def show_loading_state(self, loading):
        """Show/hide loading state by disabling inputs and changing button text"""
        self.email_input.disabled = loading
        self.password_input.disabled = loading
        self.login_btn.disabled = loading
        
        if loading:
            self.login_btn.text = "Signing In..."
            self.login_btn.background_color = (0.7, 0.7, 0.7, 1)
        else:
            self.login_btn.text = "Sign In"
            self.login_btn.background_color = (0.2, 0.6, 0.9, 1)  # Matching theme
    
    def show_popup(self, title, message):
        """Show a simple, clean popup message"""
        content = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
        
        # Message label with text wrapping
        msg_label = Label(
            text=message,
            font_size=sp(16),
            color=(0, 0, 0, 1),  # Changed to black
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
            background_color=(0.2, 0.6, 0.9, 1),  # Matching your start screen theme
            color=(1, 1, 1, 1)
        )
        content.add_widget(ok_btn)
        
        popup = Popup(
            title=title,
            title_size=sp(18),
            title_color=(0, 0, 0, 1),  # Changed title to black
            content=content,
            size_hint=(0.8, None),
            height=dp(180),
            auto_dismiss=False
        )
        
        ok_btn.bind(on_release=popup.dismiss)
        popup.open()