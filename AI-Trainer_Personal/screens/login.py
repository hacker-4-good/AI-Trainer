from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.screenmanager import ScreenManagerException
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.snackbar import Snackbar

import database

class Login(MDScreen):

    user_name: str
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.c_username = None
        self.c_password = None
        self.app = MDApp.get_running_app()

    def userAuthLogin(self, username, password):
        self.c_username = username
        self.c_password = password

        try:
            if not ((len(self.c_username) is not 0) and not self.c_username.isspace()):
                self.ids.login_username.error = True

            if not ((len(self.c_password) is not 0) and not self.c_password.isspace()):
                self.ids.login_password.error = True

        except Exception:
            pass

        try:
            if not (self.ids.login_username.error or self.ids.login_password.error):
                if database.check_user(self.c_username) and database.check_pass(self.c_password):
                    Login.user_name = self.c_username
                    print(Login.user_name)
                    self.manager.current = "screen_1"

                elif not database.check_user(self.c_username):
                    Snackbar(
                        text="[color=#000000]No user found![/color]",
                        snackbar_x="10dp",
                        snackbar_y="10dp",
                        bg_color=(1,1,1,1),
                        elevation=0,
                        size_hint_x=(Window.width - (dp(10) * 2)) / Window.width).open()

                else:
                    Snackbar(
                        text="[color=#000000]Wrong password.Check Again![/color]",
                        snackbar_x="10dp",
                        snackbar_y="10dp",
                        bg_color=(1, 1, 1, 1),
                        elevation=0,
                        size_hint_x=(Window.width - (dp(10) * 2)) / Window.width).open()

        except ScreenManagerException:
            pass