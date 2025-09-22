import os
import tempfile
import pytest
import yaml
from flask import Flask

from Entropy.Class.CConfig import Config


@pytest.fixture
def temp_config_file():
    # Crée un fichier YAML temporaire
    content = {
        "secret_key": "supersecret",
        "databases": {
            "Postgres": {
                "server": "localhost",
                "username": "user",
                "password": "pass",
                "database": "testdb",
                "port": 5432
            }
        }
    }
    fd, path = tempfile.mkstemp(suffix=".yaml")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        yaml.dump(content, f)
    yield path
    os.remove(path)

def test_config_initialization(temp_config_file):
    cfg = Config(config_file=temp_config_file)

    # Vérifie que c'est bien un objet Flask
    assert isinstance(cfg.app, Flask)

    # Vérifie que la clé secrète est correcte
    assert cfg.app.secret_key == "supersecret"

    # Vérifie la configuration SQLAlchemy
    expected_uri = "postgresql://user:pass@localhost:5432/testdb"
    assert cfg.app.config['SQLALCHEMY_DATABASE_URI'] == expected_uri
    assert cfg.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] is False

def test_missing_config_file():
    with pytest.raises(FileNotFoundError):
        Config(config_file="non_existant.yaml")

def test_missing_secret_key(temp_config_file):
    # Modifie le fichier temporaire pour supprimer secret_key
    with open(temp_config_file, "w", encoding="utf-8") as f:
        yaml.dump({"databases": {"Postgres": {"server": "a", "username": "b", "password": "c", "database": "d", "port": 1}}}, f)
    with pytest.raises(RuntimeError):
        Config(config_file=temp_config_file)

def test_missing_postgres_section(temp_config_file):
    # Modifie le fichier pour supprimer la section Postgres
    with open(temp_config_file, "w", encoding="utf-8") as f:
        yaml.dump({"secret_key": "key"}, f)
    with pytest.raises(ValueError):
        Config(config_file=temp_config_file)
