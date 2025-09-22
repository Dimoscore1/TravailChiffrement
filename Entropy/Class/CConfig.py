import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Instance SQLAlchemy globale (à importer partout)
db = SQLAlchemy()

class Config:
    def __init__(self):
        # Récupération des variables d'environnement
        self.secret_key = os.environ.get("SECRET_KEY", "dev_secret_key")
        self.postgres_server = os.environ.get("POSTGRES_SERVER", "localhost")
        self.postgres_user = os.environ.get("POSTGRES_USER", "postgres")
        self.postgres_password = os.environ.get("POSTGRES_PASSWORD", "password")
        self.postgres_db = os.environ.get("POSTGRES_DB", "entropydb")
        self.postgres_port = os.environ.get("POSTGRES_PORT", "5432")

        # Vérifications
        if not all([self.secret_key, self.postgres_server, self.postgres_user,
                    self.postgres_password, self.postgres_db]):
            raise RuntimeError("Certaines variables d'environnement ne sont pas définies !")

        # Création de l'app Flask
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        template_dir = os.path.join(project_root, 'templates')
        static_dir = os.path.join(project_root, 'static')

        print("Dossier templates :", template_dir)
        print("Dossier static :", static_dir)

        self.app = Flask(
            __name__,
            template_folder=template_dir,
            static_folder=static_dir
        )
        self.app.secret_key = self.secret_key

        # Config SQLAlchemy
        self.app.config['SQLALCHEMY_DATABASE_URI'] = (
            f"postgresql://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_server}:{self.postgres_port}/{self.postgres_db}"
        )
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        # Init db avec l'app
        db.init_app(self.app)

    def get_app(self):
        return self.app
