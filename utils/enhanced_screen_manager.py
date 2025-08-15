# utils/enhanced_screen_manager.py
from kivy.uix.screenmanager import ScreenManager, SlideTransition, FadeTransition, SwapTransition
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.logger import Logger
from kivy.metrics import dp
from kivy.graphics import Color, RoundedRectangle
from typing import Dict, Any, Optional, Callable
import traceback

class EnhancedScreenManager(ScreenManager):
    """Enhanced screen manager with transitions, error handling, and navigation history"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = None
        self.navigation_history = []
        self.transition_map = {
            'start': SlideTransition(direction='right'),
            'signup': SlideTransition(direction='left'),
            'login': SlideTransition(direction='left'),
            'main': FadeTransition(),
            'create_event': SlideTransition(direction='up'),
            'event_registration': SlideTransition(direction='left'),
            'my_events': SlideTransition(direction='left')
        }
        
        # Error handling
        self.error_popup = None
        self.loading_popup = None
        
    def switch_to_screen(self, screen_name: str, direction: str = None, save_history: bool = True):
        """Switch to screen with custom transition and error handling"""
        try:
            if save_history and self.current != screen_name:
                self.navigation_history.append(self.current)
                
                # Limit history size
                if len(self.navigation_history) > 10:
                    self.navigation_history.pop(0)
            
            # Set custom transition
            if direction:
                if direction in ['left', 'right', 'up', 'down']:
                    self.transition = SlideTransition(direction=direction)
                elif direction == 'fade':
                    self.transition = FadeTransition()
                elif direction == 'swap':
                    self.transition = SwapTransition()
            elif screen_name in self.transition_map:
                self.transition = self.transition_map[screen_name]
            else:
                self.transition = SlideTransition(direction='left')
            
            # Switch screen
            self.current = screen_name
            Logger.info(f"ScreenManager: Switched to {screen_name}")
            
        except Exception as e:
            Logger.error(f"ScreenManager: Error switching to {screen_name}: {e}")
            self.show_error("Navigation Error", f"Could not switch to {screen_name}")
    
    def go_back(self):
        """Navigate back to previous screen"""
        if self.navigation_history:
            previous_screen = self.navigation_history.pop()
            self.switch_to_screen(previous_screen, direction='right', save_history=False)
            return True
        return False
    
    def clear_history(self):
        """Clear navigation history"""
        self.navigation_history.clear()
    
    def show_error(self, title: str, message: str, callback: Callable = None):
        """Show error popup with custom styling"""
        if self.error_popup:
            self.error_popup.dismiss()
        
        # Create popup content
        content = BoxLayout(orientation='vertical', spacing=dp(15), padding=dp(20))
        
        # Error message
        error_label = Label(
            text=f"[color=e74c3c][b]{title}[/b][/color]\n\n{message}",
            markup=True,
            text_size=(dp(300), None),
            halign='center',
            valign='middle'
        )
        content.add_widget(error_label)
        
        # OK button
        ok_button = Button(
            text="OK",
            size_hint=(1, None),
            height=dp(50),
            background_color=(0.9, 0.3, 0.3, 1)
        )
        
        # Create popup
        self.error_popup = Popup(
            title="",
            content=content,
            size_hint=(0.8, 0.4),
            auto_dismiss=True,
            separator_height=0
        )
        
        # Style popup background
        with self.error_popup.canvas.before:
            Color(1, 1, 1, 1)
            self.error_popup.bg_rect = RoundedRectangle(
                size=self.error_popup.size,
                pos=self.error_popup.pos,
                radius=[15]
            )
        
        def on_ok_press(instance):
            self.error_popup.dismiss()
            if callback:
                callback()
        
        ok_button.bind(on_release=on_ok_press)
        content.add_widget(ok_button)
        
        self.error_popup.bind(size=self._update_popup_bg)
        self.error_popup.open()
        
        Logger.error(f"ScreenManager: Showed error - {title}: {message}")
    
    def show_loading(self, message: str = "Loading..."):
        """Show loading popup"""
        if self.loading_popup:
            self.loading_popup.dismiss()
        
        # Create loading content
        content = BoxLayout(orientation='vertical', spacing=dp(15), padding=dp(30))
        
        # Loading spinner (using label with animated text)
        spinner_label = Label(
            text="⟳",
            font_size=30,
            size_hint_y=None,
            height=dp(50)
        )
        content.add_widget(spinner_label)
        
        # Loading message
        message_label = Label(
            text=f"[color=2c3e50]{message}[/color]",
            markup=True,
            size_hint_y=None,
            height=dp(30)
        )
        content.add_widget(message_label)
        
        # Create popup
        self.loading_popup = Popup(
            title="",
            content=content,
            size_hint=(0.6, 0.3),
            auto_dismiss=False,
            separator_height=0
        )
        
        # Style popup background
        with self.loading_popup.canvas.before:
            Color(1, 1, 1, 1)
            self.loading_popup.loading_bg_rect = RoundedRectangle(
                size=self.loading_popup.size,
                pos=self.loading_popup.pos,
                radius=[15]
            )
        
        self.loading_popup.bind(size=self._update_loading_popup_bg)
        
        # Animate spinner
        def rotate_spinner(dt):
            current_text = spinner_label.text
            spinner_chars = ["⟳", "⟲", "⟳", "⟲"]
            try:
                current_index = spinner_chars.index(current_text)
                next_index = (current_index + 1) % len(spinner_chars)
                spinner_label.text = spinner_chars[next_index]
            except ValueError:
                spinner_label.text = "⟳"
        
        self.spinner_event = Clock.schedule_interval(rotate_spinner, 0.2)
        self.loading_popup.open()
    
    def hide_loading(self):
        """Hide loading popup"""
        if self.loading_popup:
            if hasattr(self, 'spinner_event'):
                self.spinner_event.cancel()
            self.loading_popup.dismiss()
            self.loading_popup = None
    
    def show_success(self, title: str, message: str, callback: Callable = None):
        """Show success popup"""
        content = BoxLayout(orientation='vertical', spacing=dp(15), padding=dp(20))
        
        # Success message
        success_label = Label(
            text=f"[color=27ae60][b]✓ {title}[/b][/color]\n\n{message}",
            markup=True,
            text_size=(dp(300), None),
            halign='center',
            valign='middle'
        )
        content.add_widget(success_label)
        
        # OK button
        ok_button = Button(
            text="OK",
            size_hint=(1, None),
            height=dp(50),
            background_color=(0.2, 0.7, 0.5, 1)
        )
        
        # Create popup
        success_popup = Popup(
            title="",
            content=content,
            size_hint=(0.8, 0.4),
            auto_dismiss=True,
            separator_height=0
        )
        
        # Style popup background
        with success_popup.canvas.before:
            Color(1, 1, 1, 1)
            success_popup.success_bg_rect = RoundedRectangle(
                size=success_popup.size,
                pos=success_popup.pos,
                radius=[15]
            )
        
        def on_ok_press(instance):
            success_popup.dismiss()
            if callback:
                callback()
        
        ok_button.bind(on_release=on_ok_press)
        content.add_widget(ok_button)
        
        success_popup.bind(size=lambda instance, value: setattr(
            success_popup.success_bg_rect, 'size', value) or setattr(
            success_popup.success_bg_rect, 'pos', instance.pos))
        
        success_popup.open()
        
        # Auto-dismiss after 3 seconds
        Clock.schedule_once(lambda dt: success_popup.dismiss(), 3)
    
    def _update_popup_bg(self, instance, value):
        """Update popup background graphics"""
        if hasattr(instance, 'bg_rect'):
            instance.bg_rect.size = value
            instance.bg_rect.pos = instance.pos
    
    def _update_loading_popup_bg(self, instance, value):
        """Update loading popup background graphics"""
        if hasattr(instance, 'loading_bg_rect'):
            instance.loading_bg_rect.size = value
            instance.loading_bg_rect.pos = instance.pos
    
    def handle_screen_error(self, screen_name: str, error: Exception):
        """Handle screen-specific errors"""
        error_msg = str(error)
        tb = traceback.format_exc()
        
        Logger.error(f"ScreenManager: Error in {screen_name}: {error_msg}\n{tb}")
        
        # Show user-friendly error message
        friendly_messages = {
            'network': "Please check your internet connection and try again.",
            'location': "Location services are not available. Some features may be limited.",
            'storage': "Unable to save data. Please check available storage space.",
            'permission': "This feature requires additional permissions to work properly."
        }
        
        # Determine error type
        error_type = 'general'
        if 'network' in error_msg.lower() or 'connection' in error_msg.lower():
            error_type = 'network'
        elif 'location' in error_msg.lower() or 'gps' in error_msg.lower():
            error_type = 'location'
        elif 'storage' in error_msg.lower() or 'disk' in error_msg.lower():
            error_type = 'storage'
        elif 'permission' in error_msg.lower():
            error_type = 'permission'
        
        friendly_msg = friendly_messages.get(error_type, "An unexpected error occurred. Please try again.")
        
        self.show_error("Error", friendly_msg)
    
    def get_current_screen_instance(self):
        """Get current screen instance"""
        try:
            return self.get_screen(self.current)
        except:
            return None
    
    def refresh_current_screen(self):
        """Refresh current screen data"""
        screen = self.get_current_screen_instance()
        if screen and hasattr(screen, 'on_enter'):
            try:
                screen.on_enter()
            except Exception as e:
                self.handle_screen_error(self.current, e)