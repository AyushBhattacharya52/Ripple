from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.widget import Widget
from kivy.graphics import Color, RoundedRectangle, Rectangle, Ellipse
from kivy.metrics import dp, sp
from kivy.animation import Animation
from kivy.clock import Clock

class ModernStartButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_down = ''
        
        # Create gradient background effect
        with self.canvas.before:
            Color(0.2, 0.6, 0.9, 1)  # Primary blue
            self.bg_rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[dp(25)])
            
        # Add subtle shadow
        with self.canvas.before:
            Color(0, 0, 0, 0.1)  # Shadow
            self.shadow_rect = RoundedRectangle(
                size=(self.width, self.height), 
                pos=(self.x + dp(2), self.y - dp(2)), 
                radius=[dp(25)]
            )
        
        self.bind(size=self._update_graphics, pos=self._update_graphics)
        self.bind(on_press=self._on_press, on_release=self._on_release)
    
    def _update_graphics(self, *args):
        self.bg_rect.size = self.size
        self.bg_rect.pos = self.pos
        self.shadow_rect.size = self.size
        self.shadow_rect.pos = (self.x + dp(2), self.y - dp(2))
    
    def _on_press(self, *args):
        # Scale down effect on press
        anim = Animation(size=(self.width * 0.95, self.height * 0.95), duration=0.1)
        anim.start(self)
        self.canvas.before.children[0].rgba = (0.15, 0.5, 0.8, 1)  # Darker blue
    
    def _on_release(self, *args):
        # Scale back up
        anim = Animation(size=(self.width / 0.95, self.height / 0.95), duration=0.1)
        anim.start(self)
        Clock.schedule_once(lambda dt: setattr(self.canvas.before.children[0], 'rgba', (0.2, 0.6, 0.9, 1)), 0.1)

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

class StartScreen(Screen):
    def __init__(self, **kwargs):
        super(StartScreen, self).__init__(**kwargs)
        
        # Create gradient background
        with self.canvas.before:
            # Background gradient from light blue to white
            Color(0.97, 0.99, 1, 1)  # Very light blue
            self.bg_rect = Rectangle(size=self.size, pos=self.pos)
        
        self.bind(size=self._update_bg, pos=self._update_bg)
        
        # Main container
        main_layout = FloatLayout()
        
        # Add floating background elements for visual interest
        self._add_floating_elements(main_layout)
        
        # Content container
        content_container = BoxLayout(
            orientation='vertical',
            spacing=dp(24),
            padding=[dp(32), dp(48)],
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            size_hint=(1, 1)
        )
        
        # Logo section with enhanced styling
        logo_container = AnchorLayout(
            size_hint=(1, 0.35),
            anchor_x='center',
            anchor_y='center'
        )
        
        # Create logo placeholder or use actual logo
        logo_widget = self._create_logo_widget()
        logo_container.add_widget(logo_widget)
        content_container.add_widget(logo_container)
        
        # Brand name with modern typography
        brand_container = BoxLayout(
            orientation='vertical',
            size_hint=(1, 0.2),
            spacing=dp(8)
        )
        
        # App name
        app_name = Label(
            text="[b]Ripple[/b]",
            markup=True,
            font_size=sp(36),
            color=(0.17, 0.24, 0.31, 1),  # Dark blue-gray
            size_hint_y=None,
            height=dp(48)
        )
        brand_container.add_widget(app_name)
        
        # Version or tagline
        version_label = Label(
            text="Community Impact Platform",
            font_size=sp(14),
            color=(0.2, 0.6, 0.9, 1),  # Brand blue
            size_hint_y=None,
            height=dp(20),
            bold=True
        )
        brand_container.add_widget(version_label)
        
        content_container.add_widget(brand_container)
        
        # Tagline section with better typography
        tagline_container = BoxLayout(
            orientation='vertical',
            size_hint=(1, 0.25),
            spacing=dp(12)
        )
        
        # Main tagline
        main_tagline = Label(
            text="[b]Every drop creates a\nripple of change[/b]",
            markup=True,
            font_size=sp(22),
            color=(0.17, 0.24, 0.31, 1),
            size_hint_y=None,
            height=dp(60),
            halign='center',
            valign='middle'
        )
        main_tagline.bind(size=main_tagline.setter('text_size'))
        tagline_container.add_widget(main_tagline)
        
        # Descriptive text
        description = Label(
            text="Connect volunteers with organizations\nfor real-world community impact",
            font_size=sp(16),
            color=(0.5, 0.55, 0.6, 1),
            size_hint_y=None,
            height=dp(48),
            halign='center',
            valign='middle'
        )
        description.bind(size=description.setter('text_size'))
        tagline_container.add_widget(description)
        
        content_container.add_widget(tagline_container)
        
        # CTA button section
        button_container = AnchorLayout(
            size_hint=(1, 0.2),
            anchor_x='center',
            anchor_y='center'
        )
        
        get_started_btn = ModernStartButton(
            text="Get Started",
            size_hint=(None, None),
            size=(dp(200), dp(56)),
            font_size=sp(18),
            color=(0.2, 0.2, 0.2, 1),
            bold=True
        )
        get_started_btn.bind(on_release=lambda x: setattr(self.manager, 'current', 'signup'))
        button_container.add_widget(get_started_btn)
        
        content_container.add_widget(button_container)
        
        main_layout.add_widget(content_container)
        
        # Add bottom navigation hint
        bottom_container = AnchorLayout(
            size_hint=(1, None),
            height=dp(60),
            anchor_x='center',
            anchor_y='bottom',
            pos_hint={'bottom': 1}
        )
        
        login_hint = BoxLayout(
            orientation='horizontal',
            size_hint=(None, None),
            size=(dp(200), dp(32)),
            spacing=dp(8)
        )
        
        already_label = Label(
            text="Already have an account?",
            font_size=sp(13),
            color=(0.5, 0.55, 0.6, 1),
            size_hint=(None, None),
            size=(dp(140), dp(32))
        )
        login_hint.add_widget(already_label)
        
        login_btn = Button(
            text="Login",
            font_size=sp(13),
            size_hint=(None, None),
            size=(dp(52), dp(32)),
            background_normal='',
            background_down='',
            color=(0.2, 0.6, 0.9, 1),
            bold=True
        )
        login_btn.bind(on_release=lambda x: setattr(self.manager, 'current', 'login'))
        login_hint.add_widget(login_btn)
        
        bottom_container.add_widget(login_hint)
        main_layout.add_widget(bottom_container)
        
        self.add_widget(main_layout)
        
        # Start entrance animation
        Clock.schedule_once(self._start_entrance_animation, 0.1)
    
    def _create_logo_widget(self):
        """Create logo widget - tries to load image, falls back to icon"""
        logo_layout = BoxLayout(orientation='vertical', spacing=dp(8))
        
        try:
            # Try to load the actual logo
            logo_img = Image(
                source='assets/logo.png',
                size_hint=(None, None),
                size=(dp(120), dp(120))
            )
            #logo_layout.add_widget(logo_img)
        except:
            # Fallback to text-based logo
            logo_container = Widget(size_hint=(None, None), size=(dp(120), dp(120)))
            
            with logo_container.canvas:
                # Create circular background
                Color(0.2, 0.6, 0.9, 0.15)
                Ellipse(size=(dp(120), dp(120)), pos=logo_container.pos)
                
                # Inner circle
                Color(0.2, 0.6, 0.9, 0.3)
                Ellipse(size=(dp(80), dp(80)), pos=(logo_container.x + dp(20), logo_container.y + dp(20)))
            
            logo_container.bind(pos=self._update_logo_graphics)
            
            # Add logo text overlay
            logo_text = Label(
                text="💧",
                font_size=sp(48),
                pos_hint={'center_x': 0.5, 'center_y': 0.5}
            )
            logo_container.add_widget(logo_text)
            logo_layout.add_widget(logo_container)
        
        return logo_layout
    
    def _update_logo_graphics(self, instance, pos):
        """Update logo graphics when position changes"""
        if hasattr(instance, 'canvas'):
            instance.canvas.clear()
            with instance.canvas:
                Color(0.2, 0.6, 0.9, 0.15)
                Ellipse(size=(dp(120), dp(120)), pos=pos)
                Color(0.2, 0.6, 0.9, 0.3)
                Ellipse(size=(dp(80), dp(80)), pos=(pos[0] + dp(20), pos[1] + dp(20)))
    
    def _add_floating_elements(self, layout):
        """Add floating decorative elements"""
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
        self.bg_rect.size = self.size
        self.bg_rect.pos = self.pos
    
    def _start_entrance_animation(self, dt):
        """Animate elements on screen entry"""
        # Fade in the entire screen
        self.opacity = 0
        anim = Animation(opacity=1, duration=0.8)
        anim.start(self)