import pytest
import sys
import os
from flask import Flask, session
from werkzeug.security import generate_password_hash

from Entropy import db
from Entropy.Class import Authentification
from Entropy.Model import EntropyModel

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))



@pytest.fixture
def app():
    """Crée une app Flask de test avec SQLite en mémoire."""
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "test_secret"

    db.init_app(app)

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


def test_register_success(app):
    def fake_entropy(pwd):
        return (3.5, "ok")

    with app.app_context():
        ok, msg = Authentification.register("Vico", "Gascon", "mdp123", fake_entropy)

        assert ok is True
        assert msg == "Inscription réussie !"
        user = Entropy.query.filter_by(prenom="Alice").first()
        assert user is not None
        assert user.nom == "Gascon"
        assert user.entropy == 3.5


def test_register_existing_user(app):
    def fake_entropy(pwd):
        return (4.2, "ok")

    with app.app_context():
        # Premier enregistrement
        Authentification.register("Bob", "Martin", "1234", fake_entropy)

        # Deuxième enregistrement avec le même prénom
        ok, msg = Authentification.register("Bob", "Autre", "5678", fake_entropy)
        assert ok is False
        assert msg == "Ce prénom est déjà utilisé"


def test_login_success(app):
    def fake_entropy(pwd):
        return (3.0, "ok")

    with app.app_context():
        # On crée un utilisateur
        hashed = generate_password_hash("mypassword", method="scrypt")
        user = Entropy(prenom="Eve", nom="Test", mdpHache=hashed, entropy=3.0)
        db.session.add(user)
        db.session.commit()

        with app.test_request_context():
            ok, msg = Authentification.login("Eve", "mypassword")
            assert ok is True
            assert msg == "Connexion réussie"
            assert session["user_id"] == user.id


def test_login_invalid(app):
    with app.test_request_context():
        ok, msg = Authentification.login("Inconnu", "wrongpass")
        assert ok is False
        assert msg == "Identifiants invalides"


def test_logout(app):
    with app.test_request_context():
        session["user_id"] = 42
        msg = Authentification.logout()
        assert msg == "Déconnecté avec succès"
        assert "user_id" not in session
