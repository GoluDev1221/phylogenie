from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from analysis_screen import AnalysisScreen
from home_screen import HomeScreen
from credits_screen import CreditsScreen

class PhyloGenieApp(App):
    def build(self):
        self.icon = 'phylogenie_logo.png'
        sm = ScreenManager()

        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(CreditsScreen(name='credits'))
        sm.add_widget(AnalysisScreen(name='analysis'))

        return sm

if __name__ == '__main__':
    PhyloGenieApp().run()
