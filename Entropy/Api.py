from flask_restx import Api, Resource, fields
from flask import request
import math
import hashlib
import requests
from werkzeug.security import generate_password_hash, check_password_hash
from back.Class.CConfig import db

# SQLAlchemy Model
class Entropy(db.Model):
    __tablename__ = "Entropy"
    id = db.Column(db.Integer, primary_key=True)
    prenom = db.Column(db.String(50), nullable=False)
    nom = db.Column(db.String(50), nullable=False)
    mdpHache = db.Column(db.String(200), nullable=False)
    entropy = db.Column(db.Integer, nullable=False)

def init_api(app, prefix='/Api'):
    api = Api(app, version="1.0", title="API Entropy",
              description="API de gestion des mots de passe et entropie",
              doc=f"{prefix}/")  # Swagger UI accessible sur /Api

    ns = api.namespace('entropy', description='Gestion utilisateurs et entropie')

    # Models Swagger
    password_model = api.model('Password', {'mdp': fields.String(required=True)})
    register_model = api.model('Register', {
        'prenom': fields.String(required=True),
        'nom': fields.String(required=True),
        'mdp': fields.String(required=True)
    })
    login_model = api.model('Login', {
        'prenom': fields.String(required=True),
        'mdp': fields.String(required=True)
    })

    # ------------------- Helpers -------------------
    def calculer_entropy(mdp):
        if not mdp:
            return 0
        pool = 0
        if any(c.islower() for c in mdp): pool += 26
        if any(c.isupper() for c in mdp): pool += 26
        if any(c.isdigit() for c in mdp): pool += 10
        if any(not c.isalnum() for c in mdp): pool += 32
        return round(len(mdp) * math.log2(pool), 2) if pool > 0 else 0

    def niveau_entropy(ent):
        if ent < 28: return "Faible"
        elif ent < 36: return "Moyenne"
        else: return "Bonne"

    def calculer_redundance(mdp):
        if not mdp:
            return 0.0
        import collections
        freqs = collections.Counter(mdp)
        n = len(mdp)
        Hmax = math.log2(len(set(mdp)))
        H = -sum((count/n) * math.log2(count/n) for count in freqs.values())
        red = round(100*(1 - H/Hmax), 2) if Hmax > 0 else 0
        return red

    def password_pwned(mdp):
        sha1 = hashlib.sha1(f"{mdp}".encode('utf-8')).hexdigest().upper()
        prefix = sha1[:5]
        suffix = sha1[5:]
        url = f"https://api.pwnedpasswords.com/range/{prefix}"
        res = requests.get(url)
        if res.status_code != 200:
            return False
        hashes = (line.split(':') for line in res.text.splitlines())
        return any(h == suffix for h, count in hashes)

    # ------------------- Routes API -------------------
    @ns.route('/calculate_entropy')
    class EntropyCalc(Resource):
        @ns.expect(password_model)
        def post(self):
            data = request.get_json()
            mdp = data.get('mdp', '')
            ent = calculer_entropy(mdp)
            return {'entropy': ent, 'niveau': niveau_entropy(ent)}

    @ns.route('/calculate_redundancy')
    class RedundancyCalc(Resource):
        @ns.expect(password_model)
        def post(self):
            data = request.get_json()
            mdp = data.get('mdp', '')
            red = calculer_redundance(mdp)
            return {'redondance': red}

    @ns.route('/check_pwned')
    class PwnedCheck(Resource):
        @ns.expect(password_model)
        def post(self):
            data = request.get_json()
            mdp = data.get('mdp', '')
            pwned = password_pwned(mdp)
            return {'pwned': pwned}

    @ns.route('/register')
    class Register(Resource):
        @ns.expect(register_model)
        def post(self):
            data = request.get_json()
            prenom, nom, mdp = data['prenom'], data['nom'], data['mdp']
            if Entropy.query.filter_by(prenom=prenom).first():
                return {'message': 'Ce prénom est déjà utilisé.'}, 400
            hashed_mdp = generate_password_hash(mdp, method='scrypt')
            ent_val = calculer_entropy(mdp)
            new_user = Entropy(prenom=prenom, nom=nom,
                               mdpHache=hashed_mdp, entropy=ent_val)
            db.session.add(new_user)
            db.session.commit()
            return {'message': 'Inscription réussie.', 'entropy': ent_val, 'niveau': niveau_entropy(ent_val)}

    @ns.route('/login')
    class Login(Resource):
        @ns.expect(login_model)
        def post(self):
            data = request.get_json()
            prenom, mdp = data['prenom'], data['mdp']
            user = Entropy.query.filter_by(prenom=prenom).first()
            if user and check_password_hash(user.mdpHache, mdp):
                return {'message': 'Connexion réussie.', 'prenom': user.prenom, 'nom': user.nom}
            return {'message': 'Identifiants invalides.'}, 401

    return api
