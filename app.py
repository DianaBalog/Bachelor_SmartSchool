from flask import Blueprint
from user import user
from institution import institution
import config

app = config.app

app.register_blueprint(user)
app.register_blueprint(institution)