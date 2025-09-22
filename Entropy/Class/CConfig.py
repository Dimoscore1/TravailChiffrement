import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Config:
    def __init__(self):
        # Dossiers absolus pour templates et static
        base_dir = os.path.dirname(os.path.abspath(__file__))
        template_dir = os.path.join(base_dir, '..', 'templates')
        static_dir = os.path.join(base_dir, '..', 'static')

        # Crée l'app Flask avec templates et static
        self.app = Flask(
            __name__,
            template_folder=template_dir,
            static_folder=static_dir
        )

        # Configuration Flask
        self.app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'ma_cle_secrete')
        self.app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('POSTGRES_SERVER')
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

