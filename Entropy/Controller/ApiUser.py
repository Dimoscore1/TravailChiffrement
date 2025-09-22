import math
import hashlib
import requests

from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from flask_restx import Api, Resource, fields
from werkzeug.security import generate_password_hash, check_password_hash
from Class.CConfig import db  # ton instance SQLAlchemy

# ---------------- Blueprint Web ----------------
ApiUser = Blueprint("ApiUser", __name__, template_folder="../templates", static_folder="../static")

# ---------------- SQLAlchemy Model ----------------
class Entropy(db.Model):
    __tablename__ = "Entropy"
    id = db.Column(db.Integer, primary_key=True)
    prenom = db.Column(db.String(50), nullable=False)
    nom = db.Column(db.String(50), nullable=False)
    mdpHache = db.Column(db.String(200), nullable=False)
    entropy = db.Column(db.Integer, nullable=False)

# ---------------- Helpers ----------------
def calculer_entropy(mdp):
    if not mdp:
        return 0, "N/A"
    pool = 0
    if any(c.islower() for c in mdp): pool += 26
    if any(c.isupper() for c in mdp): pool += 26
    if any(c.isdigit() for c in mdp): pool += 10
    if any(not c.isalnum() for c in mdp): pool += 32
    ent = round(len(mdp) * math.log2(pool), 2) if pool > 0 else 0
    if ent < 28: niveau = "Faible"
    elif ent < 36: niveau = "Moyenne"
    else: niveau = "Bonne"
    return ent, niveau

def calculer_redundance(mdp):
    if not mdp: return 0
    from collections import Counter
    freqs = Counter(mdp)
    n = len(mdp)
    Hmax = math.log2(len(set(mdp)))
    H = -sum((count/n)*math.log2(count/n) for count in freqs.values())
    red = round(100*(1 - H/Hmax),2) if Hmax > 0 else 0
    return red

def password_pwned(mdp):
    sha1 = hashlib.sha1(mdp.encode('utf-8')).hexdigest().upper()
    prefix, suffix = sha1[:5], sha1[5:]
    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    res = requests.get(url)
    if res.status_code != 200: return False
    hashes = (line.split(':') for line in res.text.splitlines())
    return any(h == suffix for h,_ in hashes)

# ---------------- Routes Web ----------------
@ApiUser.route('/')
def index():
    return render_template('index.html')

@ApiUser.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        prenom = request.form.get('prenom', '')
        mdp = request.form.get('mdp', '')
        user = Entropy.query.filter_by(prenom=prenom).first()
        if user and check_password_hash(user.mdpHache, mdp):
            session['user_id'] = user.id
            session['prenom'] = user.prenom
            return redirect(url_for('ApiUser.accueil'))
        flash("Identifiants invalides.", "danger")
    return render_template('login.html')

@ApiUser.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        prenom = request.form.get('prenom', '')
        nom = request.form.get('nom', '')
        mdp = request.form.get('mdp', '')
        if Entropy.query.filter_by(prenom=prenom).first():
            flash("Ce prénom est déjà utilisé.", "warning")
            return redirect(url_for('ApiUser.register'))
        hashed_mdp = generate_password_hash(mdp, method='scrypt')
        ent_val, _ = calculer_entropy(mdp)
        new_user = Entropy(prenom=prenom, nom=nom, mdpHache=hashed_mdp, entropy=ent_val)
        db.session.add(new_user)
        db.session.commit()
        flash("Inscription réussie.", "success")
        return redirect(url_for('ApiUser.login'))
    return render_template('register.html')

@ApiUser.route('/accueil')
def accueil():
    if 'user_id' not in session:
        flash("Vous devez être connecté.", "warning")
        return redirect(url_for('ApiUser.login'))
    return render_template('accueil.html')

@ApiUser.route('/logout')
def logout():
    session.clear()
    flash("Déconnecté.", "info")
    return redirect(url_for('ApiUser.index'))

# ---------------- Vérification mot de passe pwned ----------------
@ApiUser.route('/check_pwned', methods=['POST'])
def check_pwned_route():
    data = request.get_json()
    mdp = data.get("mdp", "")
    return jsonify({"pwned": password_pwned(mdp)})

# ---------------- API REST / Swagger ----------------
def init_api(app, prefix='/Api'):
    api = Api(app, version="1.0", title="API Entropy",
              description="API de gestion des mots de passe et entropie",
              doc=f"{prefix}/")  # Swagger UI accessible sur /Api

    ns = api.namespace('entropy', description='Gestion utilisateurs et entropie')

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

    @ns.route('/calculate_entropy')
    class EntropyCalc(Resource):
        @ns.expect(password_model)
        def post(self):
            mdp = request.get_json().get('mdp', '')
            ent, niveau = calculer_entropy(mdp)
            return {'entropy': ent, 'niveau': niveau}

    @ns.route('/calculate_redundancy')
    class RedundancyCalc(Resource):
        @ns.expect(password_model)
        def post(self):
            mdp = request.get_json().get('mdp', '')
            return {'redondance': calculer_redundance(mdp)}

    @ns.route('/check_pwned')
    class PwnedCheck(Resource):
        @ns.expect(password_model)
        def post(self):
            mdp = request.get_json().get('mdp', '')
            return {'pwned': password_pwned(mdp)}

    @ns.route('/register')
    class RegisterApi(Resource):
        @ns.expect(register_model)
        def post(self):
            data = request.get_json()
            prenom, nom, mdp = data['prenom'], data['nom'], data['mdp']
            if Entropy.query.filter_by(prenom=prenom).first():
                return {'message': 'Prénom déjà utilisé.'}, 400
            hashed_mdp = generate_password_hash(mdp, method='scrypt')
            ent_val, _ = calculer_entropy(mdp)
            new_user = Entropy(prenom=prenom, nom=nom, mdpHache=hashed_mdp, entropy=ent_val)
            db.session.add(new_user)
            db.session.commit()
            return {'message': 'Inscription réussie.', 'entropy': ent_val}

    @ns.route('/login')
    class LoginApi(Resource):
        @ns.expect(login_model)
        def post(self):
            data = request.get_json()
            prenom, mdp = data['prenom'], data['mdp']
            user = Entropy.query.filter_by(prenom=prenom).first()
            if user and check_password_hash(user.mdpHache, mdp):
                return {'message': 'Connexion réussie.', 'prenom': user.prenom, 'nom': user.nom}
            return {'message': 'Identifiants invalides.'}, 401

    return api
