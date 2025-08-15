# screens/my_events.py (enhanced)
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.metrics import dp
from kivy.uix.button import Button
from kivy.graphics import Color, RoundedRectangle
from utils.storage import load_registrations

class EventCard(BoxLayout):
    def __init__(self, event_data, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.height = dp(140)
        self.padding = dp(15)
        self.spacing = dp(8)
        
        # Create card background
        with self.canvas.before:
            Color(1, 1, 1, 1)  # White background
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[10])
        
        # Add shadow effect
        with self.canvas.before:
            Color(0, 0, 0, 0.1)  # Light shadow
            self.shadow = RoundedRectangle(
                size=(self.width + dp(4), self.height + dp(4)), 
                pos=(self.x - dp(2), self.y - dp(2)), 
                radius=[10]
            )
        
        self.bind(size=self.update_graphics, pos=self.update_graphics)
        
        # Event title
        title_label = Label(
            text=f"[b][color=2c3e50]{event_data.get('event_title', 'No Title')}[/color][/b]",
            markup=True,
            size_hint_y=None,
            height=dp(30),
            font_size=18,
            halign='left',
            valign='middle'
        )
        title_label.bind(size=title_label.setter('text_size'))
        self.add_widget(title_label)
        
        # Event details container
        details_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(80))
        
        # Left column - Event info
        left_column = BoxLayout(orientation='vertical', size_hint_x=0.5)
        
        date_label = Label(
            text=f"[color=7f8c8d]📅 Date: [/color][color=34495e]{event_data.get('event_date', 'N/A')}[/color]",
            markup=True,
            size_hint_y=None,
            height=dp(25),
            font_size=14,
            halign='left',
            valign='middle'
        )
        date_label.bind(size=date_label.setter('text_size'))
        left_column.add_widget(date_label)
        
        status_label = Label(
            text="[color=27ae60]✓ Registered[/color]",
            markup=True,
            size_hint_y=None,
            height=dp(25),
            font_size=14,
            halign='left',
            valign='middle'
        )
        status_label.bind(size=status_label.setter('text_size'))
        left_column.add_widget(status_label)
        
        # Right column - Personal info
        right_column = BoxLayout(orientation='vertical', size_hint_x=0.5)
        
        name_label = Label(
            text=f"[color=7f8c8d]👤 Name: [/color][color=34495e]{event_data.get('name', 'N/A')}[/color]",
            markup=True,
            size_hint_y=None,
            height=dp(20),
            font_size=12,
            halign='left',
            valign='middle'
        )
        name_label.bind(size=name_label.setter('text_size'))
        right_column.add_widget(name_label)
        
        email_label = Label(
            text=f"[color=7f8c8d]📧 Email: [/color][color=34495e]{event_data.get('email', 'N/A')}[/color]",
            markup=True,
            size_hint_y=None,
            height=dp(20),
            font_size=12,
            halign='left',
            valign='middle'
        )
        email_label.bind(size=email_label.setter('text_size'))
        right_column.add_widget(email_label)
        
        phone_label = Label(
            text=f"[color=7f8c8d]📱 Phone: [/color][color=34495e]{event_data.get('phone', 'N/A')}[/color]",
            markup=True,
            size_hint_y=None,
            height=dp(20),
            font_size=12,
            halign='left',
            valign='middle'
        )
        phone_label.bind(size=phone_label.setter('text_size'))
        right_column.add_widget(phone_label)
        
        details_layout.add_widget(left_column)
        details_layout.add_widget(right_column)
        self.add_widget(details_layout)
    
    def update_graphics(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos
        self.shadow.size = (self.width + dp(4), self.height + dp(4))
        self.shadow.pos = (self.x - dp(2), self.y - dp(2))

class EmptyStateCard(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.height = dp(200)
        self.padding = dp(30)
        self.spacing = dp(15)
        
        # Create card background
        with self.canvas.before:
            Color(0.98, 0.98, 0.98, 1)  # Light gray background
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[15])
        
        self.bind(size=self.update_graphics, pos=self.update_graphics)
        
        # Empty state icon
        icon_label = Label(
            text="📅",
            font_size=48,
            size_hint_y=None,
            height=dp(60),
            halign='center',
            valign='middle'
        )
        self.add_widget(icon_label)
        
        # Empty state message
        message_label = Label(
            text="[color=7f8c8d]No events registered yet[/color]",
            markup=True,
            font_size=18,
            size_hint_y=None,
            height=dp(30),
            halign='center',
            valign='middle'
        )
        self.add_widget(message_label)
        
        # Subtitle
        subtitle_label = Label(
            text="[color=95a5a6]Browse events and register to see them here[/color]",
            markup=True,
            font_size=14,
            size_hint_y=None,
            height=dp(40),
            halign='center',
            valign='middle'
        )
        subtitle_label.bind(size=subtitle_label.setter('text_size'))
        self.add_widget(subtitle_label)
    
    def update_graphics(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

class MyEventsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Create gradient background
        with self.canvas.before:
            Color(0.95, 0.96, 0.98, 1)  # Light blue-gray background
            self.bg_rect = RoundedRectangle(size=self.size, pos=self.pos)
        
        self.bind(size=self.update_bg, pos=self.update_bg)
        
        self.layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))

        # Header section
        header_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.15), spacing=dp(5))
        
        # Title with icon
        title_label = Label(
            text="[color=2c3e50]📋 My Registered Events[/color]",
            markup=True,
            font_size=26,
            size_hint_y=None,
            height=dp(40),
            halign='center',
            valign='middle'
        )
        header_layout.add_widget(title_label)
        
        # Subtitle
        subtitle_label = Label(
            text="[color=7f8c8d]View and manage your event registrations[/color]",
            markup=True,
            font_size=14,
            size_hint_y=None,
            height=dp(25),
            halign='center',
            valign='middle'
        )
        header_layout.add_widget(subtitle_label)
        
        self.layout.add_widget(header_layout)

        # Events scroll view
        self.scroll = ScrollView(size_hint=(1, 0.75))
        self.events_grid = GridLayout(cols=1, size_hint_y=None, spacing=dp(15), padding=(0, dp(10)))
        self.events_grid.bind(minimum_height=self.events_grid.setter('height'))
        self.scroll.add_widget(self.events_grid)
        self.layout.add_widget(self.scroll)

        # Back button with improved styling
        back_btn = Button(
            text="← Back to Events",
            size_hint=(1, 0.1),
            font_size=16,
            background_color=(0.3, 0.4, 0.8, 1),
            color=(1, 1, 1, 1)
        )
        back_btn.bind(on_release=lambda x: setattr(self.manager, 'current', 'main'))
        self.layout.add_widget(back_btn)

        self.add_widget(self.layout)
    
    def update_bg(self, *args):
        self.bg_rect.size = self.size
        self.bg_rect.pos = self.pos

    def on_enter(self):
        self.load_my_events()

    def load_my_events(self):
        self.events_grid.clear_widgets()
        
        try:
            registrations = load_registrations()
            
            if not registrations:
                # Show empty state
                empty_card = EmptyStateCard()
                self.events_grid.add_widget(empty_card)
                return

            # Show registered events
            for reg in registrations:
                event_card = EventCard(reg)
                self.events_grid.add_widget(event_card)
                
        except Exception as e:
            # Error handling
            error_label = Label(
                text=f"[color=e74c3c]Error loading events: {str(e)}[/color]",
                markup=True,
                size_hint_y=None,
                height=dp(50),
                halign='center',
                valign='middle'
            )
            self.events_grid.add_widget(error_label)