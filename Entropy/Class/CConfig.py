import os
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Config:
    """
    Configuration Flask et SQLAlchemy
    """
    # Lecture des variables d'environnement Render
    POSTGRES_USER = os.environ.get("POSTGRES_USER", "user")
    POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "password")
    POSTGRES_DB = os.environ.get("POSTGRES_DB", "db")
    POSTGRES_SERVER = os.environ.get("POSTGRES_SERVER", "localhost")
    POSTGRES_PORT = os.environ.get("POSTGRES_PORT", "5432")

    SECRET_KEY = os.environ.get("SECRET_KEY", "ma_cle_secrete_par_defaut")

    # Construction de l'URI SQLAlchemy correctement
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
        f"@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
