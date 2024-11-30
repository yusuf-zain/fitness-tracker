import kivy
import kivymd
import requests

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView



from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivymd.uix.button import MDButton,MDButtonIcon,MDButtonText
from kivymd.uix.screen import MDScreen
from kivy.uix.screenmanager import Screen,ScreenManager

screen_helper = """
ScreenManager:
    HomeScreen:
    MenuScreen:
    ProfileScreen:

<HomeScreen>:
    name: 'home'
    MDRectangleFlatButton:
        text: 'Home Screen'
        pos_hint: {'center_x':0.5,'center_y':0.5}
<MenuScreen>:
    name: 'menu'
    MDRectangleFlatButton:
        text: 'Menu'
        pos_hint: {'center_x':0.5,'center_y':0.5}
<ProfileScreen>:
    name: 'profile'
    MDRectangleFlatButton:
        text: 'Profile'
        pos_hint: {'center_x':0.5,'center_y':0.5}

"""


class NutriFit(MDApp):
    def build(self):
        return

NutriFit().run()
    


'''
class Example(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Green"
        return (
            MDScreen(
                MDButton(
                    MDButtonIcon(
                        icon="circle",
                    ),
                    MDButtonText(
                        text="Get Started",
                    ),
                    style="elevated",
                    pos_hint={"center_x": 0.5, "center_y": 0.5},
                ),
                md_bg_color=self.theme_cls.surfaceColor,
            )
        )


Example().run()'''

from fatsecret import Fatsecret
CONSUMER_KEY = '5bc06d27657c48c1bcb6c172aaf5b7ae'
CONSUMER_SECRET = 'c6272b2abf1446a196ba2e026f3dce1d'
fs = Fatsecret(CONSUMER_KEY,CONSUMER_SECRET)


class myLayout(BoxLayout):
    def __init__(self,**kwargs):
        super(myLayout,self).__init__(**kwargs)
        self.orientation = 'vertical' # Makes widgets appear vertically

        # This is the Search bar
        self.search_input = TextInput(hint_text='Enter food name',size_hint=(1,0.1))
        self.add_widget(self.search_input)

        # This is the Search button
        self.search_button = Button(text='Search',size_hint=(1, 0.1))
        self.search_button.bind(on_press=self.search_food)
        self.add_widget(self.search_button)
        
        # test button
        self.test_button = Button(text='test',size_hint=(1,0.1))
        self.test_button.bind(on_press=self.display_results)

        # ScrollView to display results
        self.results_view = ScrollView(size_hint=(1, 0.8))
        self.results_label = Label(
            size_hint_y=None,text='',markup=True)
        self.results_label.bind(texture_size=self.results_label.setter('size'))
        self.results_view.add_widget(self.results_label)
        self.add_widget(self.results_view)

    def search_food(self,instance):
        # Placeholder for search functionality
        food_name = self.search_input.text
        # Call the function to search and display results
        self.display_results(food_name)
        
    def display_results(self,food_name):
        # Clear previous results
        self.results_label.text = ''
        # Search for foods using the FatSecret API
        try:
            foods = fs.foods_search(food_name)
            if foods:
                result_text = ''
                for food in foods:
                    result_text += f"[b]Food:[/b] {food.get('food_name', 'N/A')}\n"
                    if 'brand_name' in food:
                        result_text += f"[b]Brand:[/b] {food['brand_name']}\n"
                    result_text += f"[b]Nutrition:[/b] {food.get('food_description', 'N/A')}\n\n"
                self.results_label.text = result_text
            else:
                self.results_label.text = 'No results found.'
        except Exception as e:
            self.results_label.text = f'An error occurred:\n{str(e)}'

class FoodSearchApp(App):
    def build(self):
        return myLayout()

if __name__ == '__main__':
    FoodSearchApp().run()

def searchFoods(foodSearch):
    foods = fs.foods_search(foodSearch)
    for i in range(len(foods)):
        print(i+1)
        currentDict = foods[i]
        print("Food:",currentDict['food_name'])
        if 'brand_name' in currentDict:
            print("Brand:",currentDict['brand_name'])
        print("Nutrition:",currentDict['food_description'])
        #print("ID:",currentDict['food_id'])
        print("")
    while True:
        try:
            index = int(input("Enter the number of the food you consumed: "))
            if 0 < index < len(foods)+1:
                return foods[index-1]
            else:
                print("Please enter a number between 0 and",len(foods))
        except ValueError:
            print("Invalid input, please enter a number")


'''
numFoods = int(input("How many foods did you eat: "))
calSum = 0
fatSum = 0
carbSum = 0
proteinSum = 0
for i in range(numFoods):
    foodSearch = input("Enter the food you are looking for: ")
    selectedFood = searchFoods(foodSearch)
    nutritionalInformation = selectedFood['food_description']
    nutritionalInformation = nutritionalInformation.strip().split('- ')
    nutritionalInformation = nutritionalInformation[1].strip().split(' | ')
    calSum += float(nutritionalInformation[0].replace('Calories: ', '').replace('kcal', '').strip())
    fatSum += float(nutritionalInformation[1].replace('Fat: ', '').replace('g', '').strip())
    carbSum += float(nutritionalInformation[1].replace('Carbs: ', '').replace('g', '').strip())
    proteinSum += float(nutritionalInformation[1].replace('Protein: ', '').replace('g', '').strip())
print("kcal:",calSum)
print("fats:",fatSum)
print("carbs:",carbSum)
print("proteins:",proteinSum)'''













