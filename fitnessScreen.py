from datetime import datetime
from kivymd.uix.screen import MDScreen
from kivy.app import App
from kivy.properties import StringProperty
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton
from kivy.lang import Builder

Builder.load_file('fitnessScreen.kv')


class FitnessScreen(MDScreen):
    exercise_name = StringProperty('')
    def on_pre_enter(self):
        if not self.exercise_name:
            pass
        else:
            pass

    def logExercise(self):
        weight = self.ids.weight_input.text
        sets = self.ids.sets_input.text
        reps = self.ids.reps_input.text
        try:
            weight = float(weight)
            sets = int(sets)
            reps = int(reps)
            date_today = datetime.today().strftime('%Y-%m-%d')
            app = App.get_running_app()
            if not hasattr(app, 'exercise_logs'):
                app.exercise_logs = {}
            if self.exercise_name not in app.exercise_logs:
                app.exercise_logs[self.exercise_name] = []
            app.exercise_logs[self.exercise_name].append({'date': date_today,'weight': weight,'sets': sets,'reps': reps})
            dialog = MDDialog(title="Success",text=f"Logged: {sets} sets of {reps} reps with {weight} lb for {self.exercise_name}!",buttons=[MDRaisedButton(text="OK", on_release=lambda x: dialog.dismiss())])
            dialog.open()
        except ValueError:
            dialog = MDDialog(title="Error",text="Please enter valid numeric values for weight, sets, and reps.",buttons=[MDRaisedButton(text="OK", on_release=lambda x: dialog.dismiss())])
            dialog.open()

    def loadHomeScreen(self):
        self.manager.current = 'home'