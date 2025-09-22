import sys
import os
import pytest

from Entropy.Class.CConfig import Config, db
from Entropy.Model import EntropyModel

# Ajoute le dossier parent au PYTHONPATH pour que Python trouve "back"
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from werkzeug.security import generate_password_hash


@pytest.fixture
def app():
    """ On crée une app Flask de test avec SQLite en mémoire."""
    config = Config()
    app = config.app
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["TESTING"] = True

    app.register_blueprint(ApiUser)

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


def test_index(client):
    response = client.get('/')
    assert response.status_code == 200


def test_register_and_login(client, app):
    with app.app_context():
        # Test register
        response = client.post('/register', data={
            'prenom': 'Vico',
            'nom': 'Gascon',
            'mdp': 'mdp123'
        }, follow_redirects=True)

        # Vérifie que l'utilisateur a été créé
        user = Entropy.query.filter_by(prenom='Vico').first()
        assert user is not None

        # Test login
        response = client.post('/login', data={
            'prenom': 'Vico',
            'mdp': 'mdp123'
        }, follow_redirects=True)

        # Vérifie que user_id est bien dans la session
        with client.session_transaction() as sess:
            assert sess.get('user_id') == user.id


def test_login_invalid(client):
    response = client.post('/login', data={
        'prenom': 'Mathieu',
        'mdp': 'Minecraft85'
    }, follow_redirects=True)

    data_str = response.data.decode('utf-8')
    assert "Identifiants invalides" in data_str


def test_accueil_requires_login(client):
    response = client.get('/accueil', follow_redirects=True)
    data_str = response.data.decode('utf-8')
    assert "Vous devez être connecté" in data_str


def test_logout(client):
    # Définit user_id dans la session du client
    with client.session_transaction() as sess:
        sess['user_id'] = 42

    response = client.get('/logout', follow_redirects=True)

    # Vérifie que user_id a été supprimé
    with client.session_transaction() as sess:
        assert 'user_id' not in sess

    # Vérifie que le message flash est présent
    data_str = response.data.decode('utf-8')
    assert "Déconnecté avec succès" in data_str
