from kivymd.uix.button import MDFlatButton
from kivymd.uix.screen import MDScreen
from kivy.animation import Animation
from kivy.app import App


class WelcomeScreen(MDScreen):
    id = 1
    def on_enter(self):
        self.start()

    def start(self, *args):
        anim = Animation(opacity=1,duration=1)
        anim += Animation(opacity=1, duration=2)
        anim += Animation(opacity=0, duration=1)
        anim.bind(on_complete=self.start)
        anim.start(self.ids[f"text{self.id}"])
        if self.id < 5:
            self.id += 1
        else:
            self.id = 1

    def current_slide(self, index):
        pass

    def next(self):
        self.ids.carousel.load_next(mode = "next")

    def getName(self):
        name = self.ids.name_input.text.strip()
        if name:
            app = App.get_running_app()
            app.user_data['name'] = name
            self.next()
        else:
            from kivymd.uix.dialog import MDDialog
            self.dialog = MDDialog(
                title="Error",
                text="Please enter your name.",
                size_hint=(0.8, None),
                buttons=[
                    MDFlatButton(
                        text="OK",
                        on_release=lambda x: self.dialog.dismiss()
                    ),
                ],
            )
            self.dialog.open()

    def getBiometrics(self):
        age = self.ids.age_input.text.strip()
        height_feet = self.ids.height_feet_input.text.strip()
        height_inches = self.ids.height_inches_input.text.strip()
        weight = self.ids.weight_input.text.strip()
        if age and height_feet and height_inches and weight:
            app = App.get_running_app()
            app.user_data['age'] = age
            app.user_data['height_feet'] = height_feet
            app.user_data['height_inches'] = height_inches
            app.user_data['weight'] = weight
            self.next()
        else:
            from kivymd.uix.dialog import MDDialog
            self.dialog = MDDialog(
                title="Error",
                text="Please complete biometrics.",
                size_hint=(0.8, None),
                buttons=[
                    MDFlatButton(
                        text="OK",
                        on_release=lambda x: self.dialog.dismiss()
                    ),
                ],
            )
            self.dialog.open()

    def genderMale(self):
        app = App.get_running_app()
        app.user_data['gender'] = "male"
        self.ids.carousel.load_next(mode="next")

    def genderFemale(self):
        app = App.get_running_app()
        app.user_data['gender'] = "female"
        self.ids.carousel.load_next(mode="next")

    def goalCut(self):
        app = App.get_running_app()
        app.user_data['goal'] = "Cut"
        self.loadLoadingScreen()

    def goalRecomp(self):
        app = App.get_running_app()
        app.user_data['goal'] = "Recomp"
        self.loadLoadingScreen()

    def goalBulk(self):
        app = App.get_running_app()
        app.user_data['goal'] = "Bulk"
        self.loadLoadingScreen()

    def loadLoadingScreen(self):
        self.manager.current = 'loading'