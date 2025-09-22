import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Config:
    def __init__(self):
        # Variables d'environnement
        self.secret_key = os.environ.get("SECRET_KEY", "changeme")  # valeur par défaut si pas définie
        self.postgres_server = os.environ.get("POSTGRES_SERVER")
        self.postgres_user = os.environ.get("POSTGRES_USER")
        self.postgres_password = os.environ.get("POSTGRES_PASSWORD")
        self.postgres_db = os.environ.get("POSTGRES_DB")
        self.postgres_port = os.environ.get("POSTGRES_PORT", "5432")  # chaîne par défaut

        # Vérifier qu'aucune variable critique n'est vide
        for var_name in ["POSTGRES_SERVER", "POSTGRES_USER", "POSTGRES_PASSWORD", "POSTGRES_DB"]:
            if not os.environ.get(var_name):
                raise RuntimeError(f"La variable {var_name} n'est pas définie !")

        # Convertir le port en entier pour sécurité
        try:
            port_int = int(self.postgres_port)
        except ValueError:
            raise RuntimeError(f"POSTGRES_PORT invalide : {self.postgres_port}")

        # Création de l'app Flask
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        template_dir = os.path.join(project_root, 'Templates')
        static_dir = os.path.join(project_root, 'static')

        self.app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
        self.app.secret_key = self.secret_key

        # Construire l'URI correctement
        self.app.config['SQLALCHEMY_DATABASE_URI'] = (
            f"postgresql://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_server}:{port_int}/{self.postgres_db}"
        )
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        # Initialiser SQLAlchemy avec l'app
        db.init_app(self.app)
