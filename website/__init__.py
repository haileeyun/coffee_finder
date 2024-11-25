from flask import Flask
import pandas as pd
import googlemaps
import time
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from os import path

from .utils import create_coffee_shop_list


def create_app():
    app = Flask(__name__)

    from .views import views

    app.register_blueprint(views, url_prefix='/')

    # can manually enter coordinates here
    location = (40.7484, 73.9857) # dummy coordinates: empire state building
    df = create_coffee_shop_list(location)

    return app


def create_database(app):
    with app.app_context():
        db.create_all()
