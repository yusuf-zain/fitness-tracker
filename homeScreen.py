from kivymd.uix.screen import MDScreen
from kivy.uix.image import Image
from kivy.app import App
from kivy.core.image import Image as CoreImage
import matplotlib.pyplot as plt
from io import BytesIO
from kivy.properties import ObjectProperty, StringProperty
from kivymd.uix.list import OneLineListItem
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton


class SelectableItem(OneLineListItem):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bg_color = (1, 1, 1, 1)

    def select(self):
        self.bg_color = (0.5, 0.5, 1, 1)

    def deselect(self):
        self.bg_color = (1, 1, 1, 1)


class HomeScreen(MDScreen):
    exercises = {'Chest':["Bar Bell Bench Press","Dumbbell Bench Press","Cable Bench Press","Smith Machine Bench Press","Cable Chest Fly","Cable Crossover","Chest Dip","Chest Fly","Dumbbell Chest Fly","Machine Chest Press","Decline Barbell Bench Press","Decline Dumbbell Bench Press","Decline Smith Machine Bench Press","Barbell Floor Press","Incline Barbell Bench Press","Incline Cable Bench Press","Incline Dumbbell Bench Press","Incline Smith Machine Bench Press","Incline Dumbbell Chest Fly","Iso-Lateral Chest Press","Incline Chest Press","Pec Deck","Plate Loaded Incline Chest Press","Dumbbell Pullover","Machine Pullover","Pushup","Supine Press"],'Back':["Back Extension","Dumbbell Bent Over One Arm Row","Barbell Bent Over Row","Dumbbell Bent Over Row","Chin Up","Assisted Chin Up","Deadlift","Good Morning","Incline Row","Inverted Row","Iso-Lateral Row","Kneeling Pulldown","Cable Lat Pulldown","Machine Lat Pulldown","Single Arm Lat Pulldown","Pendlay Row","Pull Up","Assisted Pull Up","Rack Pull","Romanian Deadlift","Cable Seated Row","Machine Seated Row","Machine Shrugs","Dumbbell Shrugs","Sumo Deadlift","T Bar Rows","Upright Rows"],'Legs':["Box Squat","Bulgarian Split Squat","Calf Press on Leg Press","Calf Press on Seated Leg Press","Dumbbell Deadlift","Smith Machine Deadlift","Front Squat","Glute Ham Raise","Glute Kickback","Goblet Squat","Hack Squat","Hip Abductor","Hip Adductor","Hip Thrust","Leg Extension","Leg Press","Barbell Lunge","Lying Leg Curl","Pistol Squats","Plate Loaded Seated Calf Raises","Seated Leg Curl","Seated Leg Press","Squat","Standing Calf Raise"],'Arms':["Dumbell Bicep Curl","Barbell Bicep Curl","Cable Bicep Curl","Machine Bicep Curl","Cable Kickback","Cable Hammer Curl","Dumbbell Hammer Curl","Incline Curl","Barbell Preacher Curl","Dumbbell Preacher Curl","Barbell Reverse Curls","Barbell Skull Crushers","Dumbbell Skul Crushers","Triceps Dips","Triceps Extension","Barbell Triceps Extension","Cable Triceps Extension","Dumbbell Triceps Extension","Tricep Pushdown","Wrist Roller"]}
    selected_exercise = ObjectProperty(None)
    selected_exercise_name = StringProperty('')
    def on_enter(self):
        app = App.get_running_app()
        name = app.user_data.get('name','User')
        goal = app.user_data.get('goal','Goal')
        total_calories = app.nutri_data['total_calories']
        total_fat = app.nutri_data['total_fat']
        total_carbs = app.nutri_data['total_carbs']
        total_protein = app.nutri_data['total_protein']
        self.ids.display_name.text = f"Hi {name}!"
        self.ids.display_goal.text = f"Your Goal: {goal}"
        self.ids.home_total_calories.text = f"Calories: {total_calories:.2f} kcal"
        self.ids.home_total_fat.text = f"Fat: {total_fat:.2f} g"
        self.ids.home_total_carbs.text = f"Carbs: {total_carbs:.2f} g"
        self.ids.home_total_protein.text = f"Protein: {total_protein:.2f} g"
        self.calculateBMR()
        self.calculateBMIGoal()
        self.calorieGoal()
        self.nutriDeficiency()
        self.buildExerciseList()
        self.createPieChart(total_fat, total_carbs, total_protein)

    def createPieChart(self, fat, carbs, protein):
        labels = 'Fat', 'Carbs', 'Protein'
        sizes = [fat, carbs, protein]
        colors = ['gold', 'lightcoral', 'lightskyblue']
        if sum(sizes) == 0:
            sizes = [1, 1, 1]
        plt.figure(figsize=(5, 5))
        plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
        plt.axis('equal')
        buf = BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close()
        im = CoreImage(buf, ext='png').texture
        if hasattr(self.ids, 'pie_chart_image'):
            self.ids.pie_chart_image.texture = im
        else:
            image_widget = Image(texture=im)
            image_widget.size_hint = (0.6, 0.6)
            image_widget.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
            image_widget.id = 'pie_chart_image'
            self.ids.pie_chart_image = image_widget
            self.add_widget(image_widget)

    def calculateBMR(self):
        app = App.get_running_app()
        gender = app.user_data.get('gender','0')
        weight = int(app.user_data.get('weight', 0))
        age = int(app.user_data.get('age', 0))
        height_inches = int(app.user_data.get('height_inches', 0))
        height_feet = int(app.user_data.get('height_feet', 0))
        weightKG = 0.453592 * weight
        heightMeters = ((height_feet * 12) + height_inches) * 0.0254
        heightCenti = heightMeters * 100
        if gender == 'male':
            BMR_Mifflin_St_Jeor = (10 * weightKG) + (6.25 * heightCenti) - (5 * age) + 5
            BMR_Harris_Benedict = (13.397 * weightKG) + (4.799 * heightCenti) - (5.677 * age) + 88.362
            BMR_average = (BMR_Mifflin_St_Jeor + BMR_Harris_Benedict) / 2
        elif gender == 'female':
            BMR_Mifflin_St_Jeor = (10 * weightKG) + (6.25 * heightCenti) - (5 * age) - 161
            BMR_Harris_Benedict = (9.247 * weightKG) + (3.098 * heightCenti) - (4.330 * age) + 447.593
            BMR_average = (BMR_Mifflin_St_Jeor + BMR_Harris_Benedict) / 2
        return BMR_average

    def calculateBMIGoal(self):
        app = App.get_running_app()
        weight = int(app.user_data.get('weight', 0))
        height_inches = int(app.user_data.get('height_inches', 0))
        height_feet = int(app.user_data.get('height_feet', 0))
        weightKG = 0.453592 * weight
        heightMeters = ((height_feet * 12) + height_inches) * 0.0254
        BMI = weightKG / (heightMeters ** 2)
        self.ids.display_BMI.text = f"BMI: {BMI:.2f} kg/m²"
        if BMI > 24.9:
            BMI_goal = "> 24.9 - You should Cut!"
        elif BMI < 18.5:
            BMI_goal = "< 18.5 - You should Bulk!"
        else:
            BMI_goal = "You should Recomp"
        self.ids.BMI_goal.text = f"BMI {BMI_goal}"

    def calorieGoal(self):
        app = App.get_running_app()
        goal = app.user_data.get('goal', 'Goal')
        total_calories = app.nutri_data['total_calories']
        BMR = self.calculateBMR()
        if goal == 'Bulk':
            calorie_goal = BMR + 500
        elif goal == 'Cut':
            calorie_goal = BMR - 600
        else:
            calorie_goal = BMR
        self.ids.calorie_goal.text = f"Calorie Goal: {calorie_goal:.2f} calories"
        self.ids.calorie_count.text = f"{total_calories:.2f}/{calorie_goal:.2f}"

    def nutriDeficiency(self):
        app = App.get_running_app()
        total_fat = float(app.nutri_data.get('total_fat', 0))
        total_carbs = float(app.nutri_data.get('total_carbs', 0))
        total_protein = float(app.nutri_data.get('total_protein', 0))
        total = total_fat + total_carbs + total_protein
        if total == 0:
            total = 1
        carb_percentage = (total_carbs / total) * 100
        fat_percentage = (total_fat / total) * 100
        protein_percentage = (total_protein / total) * 100
        deficiencies = []
        if carb_percentage < 30:
            deficiencies.append("carbs")
        if fat_percentage < 20:
            deficiencies.append("fats")
        if protein_percentage < 25:
            deficiencies.append("protein")
        if deficiencies:
            nutri_deficiency = "Consume more " + ", ".join(deficiencies) + "!"
        else:
            nutri_deficiency = "Nutrients are balanced"
        self.ids.nutrient_deficiency.text = nutri_deficiency

    def openNutriScreen(self):
        self.manager.current = 'nutri'

    def buildExerciseList(self):
        self.ids.exercise_list.clear_widgets()
        for muscle_group in self.exercises:
            header = OneLineListItem(text=f"{muscle_group} Exercises")
            header.font_style = 'Subtitle1'
            header.disabled = True
            self.ids.exercise_list.add_widget(header)
            for exercise in self.exercises[muscle_group]:
                item = SelectableItem(text=exercise, on_release=self.selectedExercise)
                self.ids.exercise_list.add_widget(item)

    def selectedExercise(self, instance):
        if instance.disabled:
            return
        if self.selected_exercise:
            self.selected_exercise.deselect()
        instance.select()
        self.selected_exercise = instance
        self.selected_exercise_name = instance.text

    def selectedExercise(self, instance):
        if self.selected_exercise:
            self.selected_exercise.bg_color = (1, 1, 1, 1)
        instance.bg_color = (0.5, 0.5, 1, 1)
        self.selected_exercise = instance
        self.selected_exercise_name = instance.text

    def startWorkout(self):
        if self.selected_exercise_name:
            self.openFitnessScreen(self.selected_exercise_name)
        else:
            self.dialog = MDDialog(
                title="No Exercise Selected",
                text="Please select an exercise to proceed.",
                buttons=[MDRaisedButton(text="OK", on_release=lambda x: self.dialog.dismiss())])
            self.dialog.open()

    def showProgress(self):
        if self.selected_exercise_name:
            self.openProgressScreen(self.selected_exercise_name)
        else:
            self.dialog = MDDialog(
                title="No Exercise Selected",
                text="Please select an exercise to proceed.",
                buttons=[MDRaisedButton(text="OK", on_release=lambda x: self.dialog.dismiss())])
            self.dialog.open()

    def openFitnessScreen(self, exercise_name):
        fitness_screen = self.manager.get_screen('fit')
        fitness_screen.exercise_name = exercise_name
        self.manager.current = 'fit'

    def openProgressScreen(self, exercise_name):
        progress_screen = self.manager.get_screen('progress')
        progress_screen.exercise_name = exercise_name
        self.manager.current = 'progress'