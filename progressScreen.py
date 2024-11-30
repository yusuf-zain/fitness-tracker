from kivymd.uix.screen import MDScreen
from kivy.app import App
from kivy.properties import StringProperty
from kivy.lang import Builder
from kivy.core.image import Image as CoreImage
from io import BytesIO
import matplotlib.pyplot as plt
from datetime import datetime

# Load the KV file
Builder.load_file('progressScreen.kv')

class ProgressScreen(MDScreen):
    exercise_name = StringProperty('')

    def on_enter(self):
        self.app = App.get_running_app()
        self.display_progress()

    def display_progress(self):
        if hasattr(self.app, 'exercise_logs') and self.exercise_name in self.app.exercise_logs:
            entries = self.app.exercise_logs[self.exercise_name]
            # Sort entries by date
            entries.sort(key=lambda x: x['date'])
            dates = [datetime.strptime(entry['date'], '%Y-%m-%d') for entry in entries]
            weights = [entry['weight'] for entry in entries]
            plt.figure()
            plt.plot(dates, weights, marker='o', linestyle='-', color='b')
            plt.title(f"Weight Progression for {self.exercise_name}")
            plt.xlabel("Date")
            plt.ylabel("Weight (lb)")
            plt.xticks(rotation=45)
            plt.gcf().autofmt_xdate()
            plt.tight_layout()

            # Save plot to a buffer
            buf = BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            plt.close()

            # Load buffer into Kivy Image
            im = CoreImage(buf, ext='png').texture
            # Update the Image widget in the KV file
            self.ids.progress_image.texture = im
            self.ids.progress_image.opacity = 1
            self.ids.no_data_label.text = ''
            self.ids.no_data_label.opacity = 0
        else:
            # Display a message that there's no data
            self.ids.progress_image.texture = None
            self.ids.progress_image.opacity = 0
            self.ids.no_data_label.text = f"No data found for {self.exercise_name}."
            self.ids.no_data_label.opacity = 1
