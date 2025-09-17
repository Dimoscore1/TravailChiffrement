from flask import Flask, request
from flask_restx import Api, Resource, fields
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# ----------------- Setup Flask -----------------
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://userbdd:1234@localhost:5432/Entropy'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

api = Api(app, version='1.0', title='API Entropy',
          description='API pour tester les fonctions de mot de passe et d’entropie')
ns = api.namespace('entropy', description='Gestion des utilisateurs et calcul d’entropie')

# ----------------- Modèle BDD -----------------
class Entropy(db.Model):
    __tablename__ = "Entropy"
    id = db.Column(db.Integer, primary_key=True)
    prenom = db.Column(db.String(50), nullable=False)
    nom = db.Column(db.String(50), nullable=False)
    mdpHache = db.Column(db.String(200), nullable=False)
    entropy = db.Column(db.Integer, nullable=False)
    cree = db.Column(db.DateTime, default=datetime.utcnow)

# ----------------- Modèles Swagger -----------------
password_model = api.model('Password', {
    'mdp': fields.String(required=True, description='Mot de passe à analyser')
})

register_model = api.model('Register', {
    'prenom': fields.String(required=True, description='Prénom de l’utilisateur'),
    'nom': fields.String(required=True, description='Nom de l’utilisateur'),
    'mdp': fields.String(required=True, description='Mot de passe')
})

login_model = api.model('Login', {
    'prenom': fields.String(required=True, description='Prénom de l’utilisateur'),
    'mdp': fields.String(required=True, description='Mot de passe')
})

# ----------------- Fonctions Utilitaires -----------------
def calculer_entropy(mdp):
    import math
    if not mdp:
        return 0
    pool = 0
    if any(c.islower() for c in mdp): pool += 26
    if any(c.isupper() for c in mdp): pool += 26
    if any(c.isdigit() for c in mdp): pool += 10
    if any(not c.isalnum() for c in mdp): pool += 32
    return round(len(mdp) * math.log2(pool), 2) if pool > 0 else 0

def niveau_entropy(ent):
    if ent < 28:
        return "Faible"
    elif ent < 36:
        return "Moyenne"
    else:
        return "Bonne"

# ----------------- Endpoints API -----------------
@ns.route('/calculate')
class EntropyCalc(Resource):
    @ns.expect(password_model)
    def post(self):
        data = request.get_json()
        mdp = data.get('mdp', '')
        ent = calculer_entropy(mdp)
        niveau = niveau_entropy(ent)
        return {'entropy': ent, 'niveau': niveau}

@ns.route('/register')
class Register(Resource):
    @ns.expect(register_model)
    def post(self):
        data = request.get_json()
        prenom = data.get('prenom', '')
        nom = data.get('nom', '')
        mdp = data.get('mdp', '')

        if not prenom or not nom or not mdp:
            return {'message': 'Tous les champs sont requis.'}, 400

        existing_user = Entropy.query.filter_by(prenom=prenom).first()
        if existing_user:
            return {'message': 'Ce prénom est déjà utilisé.'}, 400

        hashed_mdp = generate_password_hash(mdp, method='scrypt')
        ent_val = calculer_entropy(mdp)
        new_user = Entropy(prenom=prenom, nom=nom, mdpHache=hashed_mdp, entropy=ent_val)
        db.session.add(new_user)
        db.session.commit()
        return {'message': 'Inscription réussie.', 'entropy': ent_val, 'niveau': niveau_entropy(ent_val)}

@ns.route('/login')
class Login(Resource):
    @ns.expect(login_model)
    def post(self):
        data = request.get_json()
        prenom = data.get('prenom', '')
        mdp = data.get('mdp', '')

        if not prenom or not mdp:
            return {'message': 'Tous les champs sont requis.'}, 400

        user = Entropy.query.filter_by(prenom=prenom).first()
        if user and check_password_hash(user.mdpHache, mdp):
            return {'message': 'Connexion réussie.', 'prenom': user.prenom, 'nom': user.nom}
        else:
            return {'message': 'Identifiants invalides.'}, 401

# ----------------- Lancement -----------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5001)
