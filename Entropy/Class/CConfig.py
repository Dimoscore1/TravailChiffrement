import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Création de l'objet SQLAlchemy
db = SQLAlchemy()

class Config:
    def __init__(self):
        # Définition des chemins des dossiers templates et static
        self.app = Flask(
            __name__,
            template_folder=os.path.join(os.path.dirname(__file__), '../templates'),
            static_folder=os.path.join(os.path.dirname(__file__), '../static')
        )

        # Configuration de la base de données via variables d'environnement
        self.app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('POSTGRES_SERVER')
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'ma_cle_secrete_super_longue')

        # Initialisation de SQLAlchemy avec l'app
        db.init_app(self.app)
