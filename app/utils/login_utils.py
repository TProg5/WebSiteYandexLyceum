from flask import Flask

from flask_login import LoginManager

def initilaze_login_manager(app: Flask) -> LoginManager:
    login_manager: LoginManager = LoginManager()

    login_manager.init_app(app=app)

    return login_manager

