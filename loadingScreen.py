from kivy.clock import Clock
from kivymd.uix.screen import MDScreen


class LoadingScreen(MDScreen):
    def on_enter(self):
        Clock.schedule_once(self.go_to_home, 5)

    def go_to_home(self, dt):
        self.manager.current = 'home'