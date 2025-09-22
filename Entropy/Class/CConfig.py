import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Config:
    def __init__(self):
        # Définir le dossier templates correctement
        template_dir = os.path.join(os.path.dirname(__file__), '..', 'templates')
        self.app = Flask(__name__, template_folder=template_dir)

        # Configuration Flask
        self.app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'ma_cle_secrete')
        self.app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('POSTGRES_SERVER')
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        # Initialisation SQLAlchemy
        db.init_app(self.app)
