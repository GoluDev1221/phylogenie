from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.image import Image

class CreditsScreen(Screen):
    def __init__(self, **kwargs):
        super(CreditsScreen, self).__init__(**kwargs)

        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=30)

        title_layout = AnchorLayout(anchor_x='center', anchor_y='top')
        title_image = Image(
            source="credits_title_image.png",
            size_hint=(1, 1), 
            width=400, 
            height=100 
        )
        title_layout.add_widget(title_image)
        main_layout.add_widget(title_layout)
        
        credits_layout = AnchorLayout(anchor_x='center', anchor_y='top')
        credit_image = Image(
            source="Credits.png", 
            size_hint=(1, 1),
            width=1080, 
            height=1080
        )
        credits_layout.add_widget(credit_image)
        main_layout.add_widget(credits_layout)

        back_button_layout = BoxLayout(orientation='horizontal', size_hint=(None, None), size=(400, 100), padding=10)
        back_button_layout.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

        back_button = Button(
            text="Back",
            size_hint=(1, 1),
            size=(200, 50),
            font_size=30,
            background_color=(0, 0, 0.5, 1),
            color=(1, 1, 1, 1),
            on_press=self.go_back
        )
        back_button_layout.add_widget(back_button)
        main_layout.add_widget(back_button_layout)

        self.add_widget(main_layout)

    def go_back(self, instance):
        self.manager.current = 'home'

