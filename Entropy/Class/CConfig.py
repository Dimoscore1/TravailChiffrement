import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Instance SQLAlchemy globale
db = SQLAlchemy()

class Config:
    def __init__(self):
        # Récupération des variables d'environnement
        self.secret_key = os.environ.get("SECRET_KEY")
        self.postgres_server = os.environ.get("POSTGRES_SERVER")
        self.postgres_user = os.environ.get("POSTGRES_USER")
        self.postgres_password = os.environ.get("POSTGRES_PASSWORD")
        self.postgres_db = os.environ.get("POSTGRES_DB")
        self.postgres_port = os.environ.get("POSTGRES_PORT", "5432")  # valeur par défaut

        # Vérification des variables
        if not all([self.secret_key, self.postgres_server, self.postgres_user,
                    self.postgres_password, self.postgres_db, self.postgres_port]):
            raise RuntimeError("Certaines variables d'environnement ne sont pas définies !")

        # Création de l'app Flask
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        template_dir = os.path.join(project_root, 'Templates')
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
        # Vérifie si POSTGRES_SERVER contient déjà l'URL complète
        if self.postgres_server.startswith("postgresql://"):
            db_uri = self.postgres_server
        else:
            db_uri = (
                f"postgresql://{self.postgres_user}:{self.postgres_password}"
                f"@{self.postgres_server}:{self.postgres_port}/{self.postgres_db}"
            )

        self.app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        # Initialisation de SQLAlchemy
        db.init_app(self.app)
