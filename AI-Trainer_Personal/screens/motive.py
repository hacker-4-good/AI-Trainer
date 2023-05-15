from kivy.core.window import Animation
from kivymd.uix.chip import MDChip
from kivymd.uix.screen import MDScreen


class MyChip(MDChip):
    icon_check_color = (0, 0, 0, 1)
    text_color = (0, 0, 0, 0.7)
    _no_ripple_effect = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(active=self.set_chip_bg_color)

    def on_press(self, *args):
        if self.active:
            self.active = False
        else:
            self.active = True

    def set_chip_bg_color(self, instance_chip, active_value: int):
        '''
        Will be called every time the chip is activated/deactivated.
        Sets the background color of the chip.
        '''

        self.md_bg_color = (
            self.theme_cls.primary_color
            if active_value
            else (
                (1,1,1,1)
                if self.theme_cls.theme_style == "Light"
                else (
                    self.theme_cls.bg_light
                    if not self.disabled
                    else self.theme_cls.disabled_hint_text_color
                )
            )
        )


class Motive(MDScreen):
    pass
