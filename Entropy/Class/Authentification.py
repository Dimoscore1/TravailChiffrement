from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session

from Model import Entropy, db


class Authentification:

    @staticmethod
    def login(prenom, mdp):
        user = Entropy.query.filter_by(prenom=prenom).first()
        if user and check_password_hash(user.mdpHache, mdp):
            session['user_id'] = user.id
            return True, "Connexion réussie"
        else:
            return False, "Identifiants invalides"

    @staticmethod
    def logout():
        session.pop('user_id', None)
        return "Déconnecté avec succès"

    @staticmethod
    def register(prenom, nom, mdp, calculer_entropy):
        if not prenom or not nom or not mdp:
            return False, "Tous les champs doivent être remplis"

        existing_user = Entropy.query.filter_by(prenom=prenom).first()
        if existing_user:
            return False, "Ce prénom est déjà utilisé"

        hashed_mdp = generate_password_hash(mdp, method='scrypt')
        ent_calc, _ = calculer_entropy(mdp)
        new_user = Entropy(prenom=prenom, nom=nom, mdpHache=hashed_mdp, entropy=ent_calc)
        db.session.add(new_user)
        db.session.commit()
        return True, "Inscription réussie !"
