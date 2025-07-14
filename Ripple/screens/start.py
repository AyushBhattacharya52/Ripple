from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image

class StartScreen(Screen):
    def __init__(self, **kwargs):
        super(StartScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=20, padding=40)
        layout.add_widget(Image(source='assets/logo.png'))
        layout.add_widget(Label(text="Every drop creates a ripple of change", font_size=24))
        layout.add_widget(Label(text="Ripple connects volunteers with organizations for real-world impact."))
        btn = Button(text="Get Started", size_hint=(1, 0.2))
        btn.bind(on_release=lambda x: setattr(self.manager, 'current', 'signup'))
        layout.add_widget(btn)
        self.add_widget(layout)
