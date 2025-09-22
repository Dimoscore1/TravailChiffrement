import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initialise SQLAlchemy sans app pour le moment
db = SQLAlchemy()


class Config:
    def __init__(self):
        # Crée l'application Flask
        self.app = Flask(
            __name__,
            template_folder=os.path.join(os.getcwd(), 'Entropy', 'templates'),
            static_folder=os.path.join(os.getcwd(), 'Entropy', 'static')
        )

        # Configuration Flask
        self.app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'ma_cle_secrete_par_defaut')

        # Récupération de l'URL complète de la base PostgreSQL
        database_url = os.environ.get('POSTGRES_SERVER')

        if not database_url:
            raise ValueError("La variable d'environnement POSTGRES_SERVER n'est pas définie !")

        # Configuration SQLAlchemy
        self.app.config['SQLALCHEMY_DATABASE_URI'] = database_url
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        # Initialise SQLAlchemy avec l'app
        db.init_app(self.app)

        # Crée les tables si elles n'existent pas
        with self.app.app_context():
            db.create_all()
