# screens/main_page.py (enhanced)
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.metrics import dp
from kivy.uix.popup import Popup
from kivy.graphics import Color, RoundedRectangle, Line
from kivy.uix.widget import Widget
from utils.storage import load_events

class EventCard(BoxLayout):
    def __init__(self, event, callback, **kwargs):
        super().__init__(orientation='vertical', size_hint_y=None, height=dp(140), **kwargs)
        
        # Create card background
        with self.canvas.before:
            Color(1, 1, 1, 1)  # White background
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[10])
            Color(0.9, 0.9, 0.9, 1)  # Light gray border
            self.border = Line(rounded_rectangle=(self.x, self.y, self.width, self.height, 10), width=1)
        
        self.bind(size=self.update_graphics, pos=self.update_graphics)
        
        # Add shadow effect
        with self.canvas.before:
            Color(0, 0, 0, 0.1)  # Shadow color
            self.shadow = RoundedRectangle(
                size=(self.width, self.height), 
                pos=(self.x + 2, self.y - 2), 
                radius=[10]
            )
        
        # Event content
        content_layout = BoxLayout(orientation='vertical', padding=dp(15), spacing=dp(5))
        
        # Title
        title_label = Label(
            text=f"[b][color=2c3e50]{event.get('title', 'No Title')}[/color][/b]",
            markup=True,
            size_hint_y=None,
            height=dp(30),
            font_size=18,
            halign='left',
            valign='middle'
        )
        title_label.bind(size=title_label.setter('text_size'))
        content_layout.add_widget(title_label)
        
        # Date and location info
        info_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(20), spacing=dp(10))
        
        date_label = Label(
            text=f"[color=7f8c8d]📅 {event.get('date', 'N/A')}[/color]",
            markup=True,
            size_hint_x=0.5,
            font_size=14,
            halign='left',
            valign='middle'
        )
        date_label.bind(size=date_label.setter('text_size'))
        info_layout.add_widget(date_label)
        
        location_label = Label(
            text=f"[color=7f8c8d]📍 {event.get('location', 'N/A')}[/color]",
            markup=True,
            size_hint_x=0.5,
            font_size=14,
            halign='left',
            valign='middle'
        )
        location_label.bind(size=location_label.setter('text_size'))
        info_layout.add_widget(location_label)
        
        content_layout.add_widget(info_layout)
        
        # Description preview
        description = event.get('description', 'No Description')
        preview = description[:80] + "..." if len(description) > 80 else description
        desc_label = Label(
            text=f"[color=95a5a6]{preview}[/color]",
            markup=True,
            size_hint_y=None,
            height=dp(35),
            font_size=13,
            halign='left',
            valign='top'
        )
        desc_label.bind(size=desc_label.setter('text_size'))
        content_layout.add_widget(desc_label)
        
        # View details button
        details_btn = Button(
            text="View Details",
            size_hint_y=None,
            height=dp(35),
            background_normal='',
            background_color=(0.2, 0.6, 0.9, 1),
            color=(1, 1, 1, 1),
            font_size=14
        )
        details_btn.bind(on_release=lambda x: callback(event))
        
        with details_btn.canvas.before:
            Color(0.2, 0.6, 0.9, 1)
            details_btn.bg_rect = RoundedRectangle(size=details_btn.size, pos=details_btn.pos, radius=[5])
        
        details_btn.bind(size=lambda instance, value: setattr(instance.bg_rect, 'size', value))
        details_btn.bind(pos=lambda instance, value: setattr(instance.bg_rect, 'pos', value))
        
        content_layout.add_widget(details_btn)
        
        self.add_widget(content_layout)
    
    def update_graphics(self, instance, value):
        self.rect.size = self.size
        self.rect.pos = self.pos
        self.shadow.size = self.size
        self.shadow.pos = (self.x + 2, self.y - 2)
        self.border.rounded_rectangle = (self.x, self.y, self.width, self.height, 10)

class MainPage(Screen):
    def __init__(self, **kwargs):
        super(MainPage, self).__init__(**kwargs)
        
        # Set background color
        with self.canvas.before:
            Color(0.95, 0.95, 0.97, 1)  # Light gray background
            self.rect = RoundedRectangle(size=self.size, pos=self.pos)
        self.bind(size=self.update_rect, pos=self.update_rect)
        
        self.layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))

        # Header section
        header_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.15), spacing=dp(5))
        
        # Title with gradient effect
        title_label = Label(
            text="[b][color=2c3e50]Ripple[/color][/b]",
            markup=True,
            font_size=32,
            size_hint_y=0.6
        )
        header_layout.add_widget(title_label)
        
        subtitle_label = Label(
            text="[color=7f8c8d]Discover and join community events[/color]",
            markup=True,
            font_size=16,
            size_hint_y=0.4
        )
        header_layout.add_widget(subtitle_label)
        
        self.layout.add_widget(header_layout)

        # Events scroll view with enhanced styling
        scroll_container = BoxLayout(orientation='vertical', size_hint=(1, 0.65))
        
        # Events section header
        events_header = Label(
            text="[b][color=34495e]Upcoming Events[/color][/b]",
            markup=True,
            font_size=20,
            size_hint_y=None,
            height=dp(40),
            halign='left'
        )
        events_header.bind(size=events_header.setter('text_size'))
        scroll_container.add_widget(events_header)
        
        self.scroll = ScrollView()
        self.events_grid = GridLayout(cols=1, size_hint_y=None, spacing=dp(15))
        self.events_grid.bind(minimum_height=self.events_grid.setter('height'))
        self.scroll.add_widget(self.events_grid)
        scroll_container.add_widget(self.scroll)
        
        self.layout.add_widget(scroll_container)

        # Enhanced button layout
        button_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.2), spacing=dp(15))
        
        # Create Event button
        create_btn = Button(
            text="+ Create Event",
            background_normal='',
            background_color=(0.2, 0.7, 0.3, 1),
            color=(1, 1, 1, 1),
            font_size=16,
            bold=True
        )
        
        with create_btn.canvas.before:
            Color(0.2, 0.7, 0.3, 1)
            create_btn.bg_rect = RoundedRectangle(size=create_btn.size, pos=create_btn.pos, radius=[8])
        
        create_btn.bind(size=lambda instance, value: setattr(instance.bg_rect, 'size', value))
        create_btn.bind(pos=lambda instance, value: setattr(instance.bg_rect, 'pos', value))
        create_btn.bind(on_release=lambda x: setattr(self.manager, 'current', 'create_event'))
        button_layout.add_widget(create_btn)

        # My Events button
        my_events_btn = Button(
            text="My Events",
            background_normal='',
            background_color=(0.5, 0.5, 0.5, 1),
            color=(1, 1, 1, 1),
            font_size=16,
            bold=True
        )
        
        with my_events_btn.canvas.before:
            Color(0.5, 0.5, 0.5, 1)
            my_events_btn.bg_rect = RoundedRectangle(size=my_events_btn.size, pos=my_events_btn.pos, radius=[8])
        
        my_events_btn.bind(size=lambda instance, value: setattr(instance.bg_rect, 'size', value))
        my_events_btn.bind(pos=lambda instance, value: setattr(instance.bg_rect, 'pos', value))
        my_events_btn.bind(on_release=lambda x: setattr(self.manager, 'current', 'my_events'))
        button_layout.add_widget(my_events_btn)

        self.layout.add_widget(button_layout)
        self.add_widget(self.layout)

    def update_rect(self, instance, value):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def on_enter(self):
        self.load_events()

    def load_events(self):
        self.events_grid.clear_widgets()
        events = load_events()
        
        if not events:
            # Enhanced empty state
            empty_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(200), spacing=dp(10))
            
            empty_icon = Label(
                text="📅",
                font_size=48,
                size_hint_y=None,
                height=dp(60)
            )
            empty_layout.add_widget(empty_icon)
            
            empty_label = Label(
                text="[b][color=7f8c8d]No events available yet[/color][/b]",
                markup=True,
                font_size=18,
                size_hint_y=None,
                height=dp(30)
            )
            empty_layout.add_widget(empty_label)
            
            empty_sublabel = Label(
                text="[color=95a5a6]Be the first to create an event in your community![/color]",
                markup=True,
                font_size=14,
                size_hint_y=None,
                height=dp(20)
            )
            empty_layout.add_widget(empty_sublabel)
            
            self.events_grid.add_widget(empty_layout)
            return

        for event in events:
            event_card = EventCard(event, self.show_event_details)
            self.events_grid.add_widget(event_card)

    def show_event_details(self, event):
        content = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))

        # Enhanced event details
        details_text = f"""[b][size=20][color=2c3e50]{event.get('title', 'No Title')}[/color][/size][/b]

[b]📅 Date:[/b] [color=7f8c8d]{event.get('date', 'N/A')}[/color]
[b]📍 Location:[/b] [color=7f8c8d]{event.get('location', 'N/A')}[/color]
[b]👤 Organizer:[/b] [color=7f8c8d]{event.get('name', 'N/A')}[/color]
[b]📞 Contact:[/b] [color=7f8c8d]{event.get('contact', 'N/A')}[/color]

[b]Description:[/b]
[color=34495e]{event.get('description', 'No Description')}[/color]"""

        label = Label(
            text=details_text,
            markup=True,
            text_size=(None, None),
            size_hint_y=None,
            halign='left',
            valign='top'
        )
        label.bind(texture_size=lambda instance, value: setattr(label, 'height', value[1]))
        content.add_widget(label)

        # Enhanced buttons
        btn_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=dp(50), spacing=dp(10))
        
        btn_register = Button(
            text='Register for Event',
            background_normal='',
            background_color=(0.2, 0.7, 0.3, 1),
            color=(1, 1, 1, 1),
            font_size=16,
            bold=True
        )
        
        with btn_register.canvas.before:
            Color(0.2, 0.7, 0.3, 1)
            btn_register.bg_rect = RoundedRectangle(size=btn_register.size, pos=btn_register.pos, radius=[5])
        
        btn_register.bind(size=lambda instance, value: setattr(instance.bg_rect, 'size', value))
        btn_register.bind(pos=lambda instance, value: setattr(instance.bg_rect, 'pos', value))
        
        btn_close = Button(
            text='Close',
            background_normal='',
            background_color=(0.7, 0.7, 0.7, 1),
            color=(1, 1, 1, 1),
            font_size=16
        )
        
        with btn_close.canvas.before:
            Color(0.7, 0.7, 0.7, 1)
            btn_close.bg_rect = RoundedRectangle(size=btn_close.size, pos=btn_close.pos, radius=[5])
        
        btn_close.bind(size=lambda instance, value: setattr(instance.bg_rect, 'size', value))
        btn_close.bind(pos=lambda instance, value: setattr(instance.bg_rect, 'pos', value))
        
        btn_layout.add_widget(btn_register)
        btn_layout.add_widget(btn_close)
        content.add_widget(btn_layout)

        popup = Popup(
            title="Event Details",
            content=content,
            size_hint=(0.9, 0.8),
            separator_color=(0.2, 0.6, 0.9, 1)
        )
        
        btn_close.bind(on_release=popup.dismiss)
        btn_register.bind(on_release=lambda x: self.register_for_event(event, popup))
        popup.open()

    def register_for_event(self, event, popup):
        popup.dismiss()
        self.manager.get_screen('event_registration').set_event(event)
        self.manager.current = 'event_registration'