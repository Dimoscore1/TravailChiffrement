import os
import yaml
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Instance SQLAlchemy globale
db = SQLAlchemy()

class Config:
    def __init__(self, config_file=None):
        if config_file is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            config_file = os.path.join(base_dir, 'Config', 'config.yaml')
            config_file = os.path.abspath(config_file)

        print("Chemin absolu recherché :", config_file)
        if not os.path.exists(config_file):
            raise FileNotFoundError(f"Le fichier config.yaml est introuvable : {config_file}")

        # Lecture YAML
        with open(config_file, "r", encoding="utf-8") as f:
            config = yaml.load(f, Loader=yaml.FullLoader)

        # Clé secrète
        self.secret_key = config.get("secret_key", "").strip()
        if not self.secret_key:
            raise RuntimeError("La clé secrète n'a pas été définie correctement !")

        # Config PostgreSQL
        postgres = config.get("databases", {}).get("Postgres")
        if not postgres:
            raise ValueError("Section databases.Postgres manquante dans config.yaml")

        self.PostgresServer = postgres.get("server")
        self.PostgresUsername = postgres.get("username")
        self.PostgresPassword = postgres.get("password")
        self.PostgresDatabase = postgres.get("database")
        self.PostgresPort = postgres.get("port")

        # Templates et static
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        template_dir = os.path.join(project_root, 'Templates')
        static_dir = os.path.join(project_root, 'static')
        print("Dossier templates :", template_dir)
        print("Dossier static :", static_dir)

        # Création de l'app Flask
        self.app = Flask(
            __name__,
            template_folder=template_dir,
            static_folder=static_dir
        )
        self.app.secret_key = self.secret_key

        # Config SQLAlchemy
        self.app.config['SQLALCHEMY_DATABASE_URI'] = (
            f"postgresql://{self.PostgresUsername}:{self.PostgresPassword}"
            f"@{self.PostgresServer}:{self.PostgresPort}/{self.PostgresDatabase}"
        )
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        # Init db avec l'app
        db.init_app(self.app)
