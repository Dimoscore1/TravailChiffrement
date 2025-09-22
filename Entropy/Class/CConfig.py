import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Config:
    def __init__(self):
        # Crée l'application Flask
        self.app = Flask(__name__, template_folder="Entropy/templates", static_folder="Entropy/static")

        # Configuration Flask
        self.app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", "une_cle_par_defaut")
        self.app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("POSTGRES_SERVER")
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        # Initialisation SQLAlchemy
        db.init_app(self.app)
