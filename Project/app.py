from kivy.core.text import LabelBase
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from kivy.lang  import Builder
from kivy.core.window import Window
from kivy.properties import StringProperty
from kivymd.uix.relativelayout import MDRelativeLayout

Window.size = (310,580)



class ClickableTextFieldRound(MDRelativeLayout):
    text = StringProperty()
    hint_text = StringProperty()


class AITrainer(MDApp):

    def build(self):

        screen_manager = ScreenManager()
        screen_manager.add_widget(Builder.load_file("getstarted.kv"))
        screen_manager.add_widget(Builder.load_file("signup.kv"))
        screen_manager.add_widget(Builder.load_file("login.kv"))
        screen_manager.add_widget(Builder.load_file("main.kv"))
        return screen_manager
    
if __name__ =="__main__":
    LabelBase.register(name="MPoppins", fn_regular="Project/Roboto-Medium.ttf")
    LabelBase.register(name="BPoppins", fn_regular="Project/Roboto-Bold.ttf")
    AITrainer().run()