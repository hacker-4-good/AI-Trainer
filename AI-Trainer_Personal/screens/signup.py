from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.screenmanager import ScreenManagerException
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
import re

from kivymd.uix.snackbar import Snackbar

import database
import random

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
id = int(random.random() * 100)


class SignUp(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.s_username = None
        self.s_email = None
        self.s_password = None
        self.app = MDApp.get_running_app()

    def userAuth(self, username, email, password):
        self.s_username = username
        self.s_email = email
        self.s_password = password

        try:
            if not ((len(self.s_username) is not 0) and not self.s_username.isspace()):
                self.ids.signup_username.error = True

            if not ((len(self.s_email) is not 0) and not self.s_email.isspace() and re.fullmatch(regex, self.s_email)):
                self.ids.signup_email.error = True

            if not ((len(self.s_password) is not 0) and not self.s_password.isspace()):
                self.ids.signup_password.error = True

        except Exception:
            pass

        try:
            if not (self.ids.signup_username.error or self.ids.signup_email.error or self.ids.signup_password.error):
                if database.check_user(username):
                    Snackbar(
                        text="[color=#FF0000]User already registered![/color]",
                        snackbar_x="10dp",
                        snackbar_y="10dp",
                        bg_color=(0, 0, 0, 1),
                        elevation = 0,
                        size_hint_x=(Window.width - (dp(10) * 2)) / Window.width).open()
                else:
                    database.create(id, self.s_username, self.s_email, self.s_password)
                    self.manager.current = "motive"

        except ScreenManagerException:
            pass
