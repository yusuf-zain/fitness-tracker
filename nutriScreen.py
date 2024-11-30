from kivymd.uix.list import OneLineListItem
from fatsecret import Fatsecret
from kivymd.uix.screen import MDScreen
from kivy.app import App

CONSUMER_KEY = '5bc06d27657c48c1bcb6c172aaf5b7ae'
CONSUMER_SECRET = 'c6272b2abf1446a196ba2e026f3dce1d'
fs = Fatsecret(CONSUMER_KEY, CONSUMER_SECRET)


class NutriScreen(MDScreen):
    def on_pre_enter(self):
        self.session_total_calories = 0
        self.session_total_fat = 0
        self.session_total_carbs = 0
        self.session_total_protein = 0
        self.added_foods = []
        self.ids.total_fat_label.text = "Total Fat: 0 g"
        self.ids.total_carbs_label.text = "Total Carbs: 0 g"
        self.ids.total_protein_label.text = "Total Protein: 0 g"
        self.ids.search_input.text = ""
        self.ids.results_list.clear_widgets()

    def searchFood(self):
        food_name = self.ids.search_input.text
        self.ids.results_list.clear_widgets()
        try:
            foods = fs.foods_search(food_name)
            if foods:
                for food in foods:
                    food_name = food.get('food_name', 'N/A')
                    brand_name = food.get('brand_name', '')
                    #food_description = food.get('food_description', 'N/A')
                    if brand_name:
                        primary_text = food_name + " (" + brand_name + ")"
                    else:
                        primary_text = food_name
                    self.ids.results_list.add_widget(
                        OneLineListItem(
                            text=primary_text,
                            on_release=lambda x, f=food: self.showFoodDetails(f)
                        )
                    )
            else:
                self.ids.results_list.add_widget(OneLineListItem(text="No results found."))
        except Exception as e:
            self.ids.results_list.add_widget(OneLineListItem(text=f"An error occurred: {str(e)}"))

    def showFoodDetails(self, food):
        food_name = food.get('food_name','N/A')
        brand_name = food.get('brand_name','')
        food_description = food.get('food_description','N/A')
        info = f"[b]Food:[/b] {food_name}\n"
        if brand_name:
            info += f"[b]Brand:[/b] {brand_name}\n"
        info += f"[b]Nutrition:[/b] {food_description}"
        from kivymd.uix.dialog import MDDialog
        from kivymd.uix.button import MDFlatButton
        self.dialog = MDDialog(
            title="Food Details",
            text=info,
            size_hint=(0.8, None),
            buttons=[MDFlatButton(text="ADD",on_release=lambda x: self.addFoodToList(food)),MDFlatButton(text="CLOSE",on_release=lambda x: self.dialog.dismiss()),],)
        self.dialog.open()

    def addFoodToList(self, food):
            self.added_foods.append(food)
            self.updateNutriTotals()
            self.dialog.dismiss()

    def extractNutritionalInfo(self):
        extracted_info = []
        for food in self.added_foods:
            info = {}
            info['food_name'] = food.get('food_name', 'N/A')
            food_id = food.get('food_id')
            if not food_id:
                continue
            try:
                detailed_food = fs.food_get(food_id)
                servings = detailed_food.get('servings', {})
                serving = servings.get('serving', {})
                if isinstance(serving, list):
                    serving = serving[0]
                info['calories'] = float(serving.get('calories', 0))
                info['fat'] = float(serving.get('fat', 0))
                info['carbs'] = float(serving.get('carbohydrate', 0))
                info['protein'] = float(serving.get('protein', 0))
            except Exception as e:
                print(f"Error retrieving detailed info for {info['food_name']}: {str(e)}")
                food_description = food.get('food_description', '')
                info.update(self.parseNutriInfo(food_description))
            extracted_info.append(info)
        return extracted_info

    def parseNutriInfo(self, description):
        nutrients = {'calories': 0,'fat': 0,'carbs': 0,'protein': 0}
        try:
            parts = description.split('-')[-1].strip().split('|')
            for part in parts:
                name, value = part.strip().split(':')
                name = name.strip().lower()
                value = value.strip().replace('kcal', '').replace('g', '')
                if name == 'calories':
                    nutrients['calories'] = float(value)
                elif name == 'fat':
                    nutrients['fat'] = float(value)
                elif name == 'carbs':
                    nutrients['carbs'] = float(value)
                elif name == 'protein':
                    nutrients['protein'] = float(value)
        except Exception as e:
            print(f"Error parsing nutrients: {str(e)}")
        return nutrients

    def updateNutriTotals(self):
        extracted_info = self.extractNutritionalInfo()
        self.session_total_calories = sum(info['calories'] for info in extracted_info)
        self.session_total_fat = sum(info['fat'] for info in extracted_info)
        self.session_total_carbs = sum(info['carbs'] for info in extracted_info)
        self.session_total_protein = sum(info['protein'] for info in extracted_info)
        self.ids.total_calories_label.text = f"Total Calories: {self.session_total_calories:.2f} kcal"
        self.ids.total_fat_label.text = f"Total Fat: {self.session_total_fat:.2f} g"
        self.ids.total_carbs_label.text = f"Total Carbs: {self.session_total_carbs:.2f} g"
        self.ids.total_protein_label.text = f"Total Protein: {self.session_total_protein:.2f} g"

    def loadHomeScreen(self):
        app = App.get_running_app()
        app.nutri_data['total_calories'] += self.session_total_calories
        app.nutri_data['total_fat'] += self.session_total_fat
        app.nutri_data['total_carbs'] += self.session_total_carbs
        app.nutri_data['total_protein'] += self.session_total_protein
        self.manager.current = 'home'
