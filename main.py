import os
from kivy.core.text import LabelBase
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from fitnessScreen import FitnessScreen
from progressScreen import ProgressScreen
from welcomeScreen import WelcomeScreen
from homeScreen import HomeScreen
from nutriScreen import NutriScreen
from loadingScreen import LoadingScreen

Builder.load_file('welcomeScreen.kv')
Builder.load_file('homeScreen.kv')
Builder.load_file('nutriScreen.kv')
Builder.load_file('loadingScreen.kv')

class MainApp(MDApp):
    user_data = {}
    nutri_data = {'total_calories': 0,'total_fat': 0,'total_carbs': 0,'total_protein': 0}
    exercise_logs = {}
    def build(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        fonts_dir = os.path.join(base_dir, 'assets', 'Fonts')
        LabelBase.register(name='NotoSans', fn_regular=os.path.join(fonts_dir, 'NotoSans_Condensed-Black.ttf'))
        LabelBase.register(name='NotoSansArabic', fn_regular=os.path.join(fonts_dir, 'NotoKufiArabic-Black.ttf'))
        LabelBase.register(name='NotoSansSC', fn_regular=os.path.join(fonts_dir, 'NotoSansSC-Black.ttf'))
        LabelBase.register(name='PoppinsRegular', fn_regular=os.path.join(fonts_dir, 'Poppins-Regular.ttf'))

        sm = ScreenManager()
        self.welcome_screen = WelcomeScreen(name='welcome')
        self.loading_screen = LoadingScreen(name='loading')
        self.home_screen = HomeScreen(name='home')
        self.nutri_screen = NutriScreen(name='nutri')
        self.fitness_screen = FitnessScreen(name='fit')
        self.progress_screen = ProgressScreen(name='progress')
        self.welcome_screen.app = self
        self.loading_screen.app = self
        self.home_screen.app = self
        self.nutri_screen.app = self
        self.fitness_screen.app = self
        self.progress_screen.app = self
        sm.add_widget(self.welcome_screen)
        sm.add_widget(self.loading_screen)
        sm.add_widget(self.home_screen)
        sm.add_widget(self.nutri_screen)
        sm.add_widget(self.fitness_screen)
        sm.add_widget(self.progress_screen)
        sm.current = 'welcome'

        return sm

if __name__ == '__main__':
    MainApp().run()
