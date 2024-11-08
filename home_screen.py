from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.anchorlayout import AnchorLayout

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        main_layout = BoxLayout(orientation='vertical', spacing=20, padding=20)

        logo_layout = AnchorLayout(anchor_x='center', anchor_y='center')
        logo = Image(source='phylogenie_logo.png', size_hint=(None, None), size=(250, 250)) 
        logo_layout.add_widget(logo)
        main_layout.add_widget(logo_layout)

        start_button_layout = AnchorLayout(anchor_x='center', anchor_y='center')
        start_button = Button(
            text="Start Analysis",
            size_hint=(0.5, 0.5),
            background_color=(0.1, 0.6, 0.2, 1),
            color=(1, 1, 1, 1),
            font_size=35,
            on_press=self.start_analysis
        )
        start_button_layout.add_widget(start_button)
        main_layout.add_widget(start_button_layout)

        credits_button_layout = AnchorLayout(anchor_x='center', anchor_y='center')
        credits_button = Button(
            text="Credits",
            size_hint=(0.5, 0.5),
            background_color=(0.1, 0.4, 0.8, 1),
            color=(1, 1, 1, 1),
            font_size=35,
            on_press=self.view_credits
        )
        credits_button_layout.add_widget(credits_button)
        main_layout.add_widget(credits_button_layout)
        
        self.add_widget(main_layout)

    def start_analysis(self, instance):
        self.manager.current = 'analysis'

    def view_credits(self, instance):
        self.manager.current = 'credits'

