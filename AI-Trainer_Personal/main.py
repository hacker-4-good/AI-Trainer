from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.text import LabelBase
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import StringProperty, ObjectProperty
from kivymd.app import MDApp
from kivymd.uix.behaviors import MagicBehavior
from kivymd.uix.button import MDRoundFlatButton, MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.hero import MDHeroFrom
from screens.signup import SignUp
from screens.start import Start
from screens.login import Login
from screens.motive import Motive

import database

Window.size = (340, 580)


# Window.size = (580, 300)


class MagicButton(MagicBehavior, MDRoundFlatButton):
    pass


class HeroItem(MDHeroFrom):
    source = StringProperty()
    text = StringProperty()
    manager = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_transform_in(self, instance_hero_widget, duration):
        Animation(
            radius=[0, 0, 0, 0],
            box_radius=[0, 0, 0, 0],
            duration=duration,
        ).start(instance_hero_widget)

    def on_transform_out(self, instance_hero_widget, duration):
        Animation(
            radius=[24, 24, 24, 24],
            box_radius=[0, 0, 24, 24],
            duration=duration,
        ).start(instance_hero_widget)

    def on_release(self):
        def switch_screen(*args):
            self.manager.ids.screen_manager.current_heroes = [self.tag]
            self.manager.ids.hero_to.tag = self.tag
            self.manager.ids.screen_manager.current = "desc_screen_1"

        Clock.schedule_once(switch_screen, 0.2)


Builder.load_file("kv/get_started.kv")
Builder.load_file("kv/signup.kv")
Builder.load_file("kv/start.kv")
Builder.load_file("kv/login.kv")
Builder.load_file("kv/motive.kv")



class AITrainer(MDApp):
    dialog = None
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.user = "User"
        self.email = "User@gmail.com"

    def build(self):
        self.theme_cls.material_style = "M3"
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Red"
        self.theme_cls.accent_palette = "Green"

        return Builder.load_file('main.kv')

    def on_start(self):
        for name_image in [
            "JumpingJacks", "Dumbbells", "Squats"
        ]:
            hero_item = HeroItem(
                text=f"{name_image}",
                tag=f"{name_image}",
                source=f"assets/images/cards/{name_image}.png",
                manager=self.root
            )
            self.root.ids.box.add_widget(hero_item)

    def on_tap_button_close(self) -> None:
        self.manager.current = "screen_1"

    def show_alert_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                text="Discard draft?",
                buttons=[
                    MDFlatButton(
                        text="CANCEL",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                    ),
                    MDFlatButton(
                        text="DISCARD",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                    ),
                ],
            )
        self.dialog.open()


if __name__ == "__main__":
    LabelBase.register(name="MPoppins", fn_regular="Roboto-Medium.ttf")
    LabelBase.register(name="BPoppins", fn_regular="Roboto-Bold.ttf")
    LabelBase.register(name="Courier", fn_regular="courier.ttf")
    AITrainer().run()
