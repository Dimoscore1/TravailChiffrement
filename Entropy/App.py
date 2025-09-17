from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import math

app = Flask(__name__)
app.secret_key = 'ton_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://userbdd:1234@localhost:5432/Entropy'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ----------------- Modèle BDD -----------------
class Entropy(db.Model):
    __tablename__ = "Entropy"
    id = db.Column(db.Integer, primary_key=True)
    prenom = db.Column(db.String(50), nullable=False)
    nom = db.Column(db.String(50), nullable=False)
    mdpHache = db.Column(db.String(200), nullable=False)
    entropy = db.Column(db.Integer, nullable=True)
    cree = db.Column(db.DateTime, default=datetime.utcnow)

# ----------------- Fonctions utilitaires -----------------
def calculer_entropy(mdp):
    if not mdp:
        return None, None
    # Approximation simple : log2(nombre de caractères possibles ^ longueur)
    pool = 0
    if any(c.islower() for c in mdp):
        pool += 26
    if any(c.isupper() for c in mdp):
        pool += 26
    if any(c.isdigit() for c in mdp):
        pool += 10
    if any(c in "!@#$%^&*()-_=+[]{};:,.<>/?|\\`~" for c in mdp):
        pool += 32
    if pool == 0:
        pool = 1
    ent = int(math.log2(pool ** len(mdp)))
    if ent < 28:
        niveau = "Faible"
    elif ent < 36:
        niveau = "Moyen"
    else:
        niveau = "Fort"
    return ent, niveau

# ----------------- Routes -----------------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        prenom = request.form['prenom']
        mdp = request.form['mdp']
        user = Entropy.query.filter_by(prenom=prenom).first()
        if user and check_password_hash(user.mdpHache, mdp):
            session['user_id'] = user.id
            flash('Connexion réussie !', 'success')
            return redirect(url_for('index'))
        else:
            flash('Identifiants invalides.', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    ent_value = ""
    niveau = ""
    prenom_val = ""
    nom_val = ""
    mdp_val = ""

    if request.method == 'POST':
        # récupérer les valeurs pour garder l'affichage dans les inputs
        prenom_val = request.form.get('prenom', '')
        nom_val = request.form.get('nom', '')
        mdp_val = request.form.get('mdp', '')

        if 'calculer_entropy' in request.form:
            # bouton "Calculer l'entropie" cliqué
            if mdp_val.strip() == "":
                ent_value = ""
                niveau = ""
            else:
                ent_value, niveau = calculer_entropy(mdp_val)
        else:
            # bouton "S'inscrire" cliqué
            if not prenom_val or not nom_val or not mdp_val:
                flash("Tous les champs doivent être remplis.", "warning")
            else:
                existing_user = Entropy.query.filter_by(prenom=prenom_val).first()
                if existing_user:
                    flash('Ce prénom est déjà utilisé.', 'warning')
                else:
                    hashed_mdp = generate_password_hash(mdp_val, method='scrypt')
                    ent_calc, _ = calculer_entropy(mdp_val)
                    new_user = Entropy(prenom=prenom_val, nom=nom_val, mdpHache=hashed_mdp, entropy=ent_calc)
                    db.session.add(new_user)
                    db.session.commit()
                    flash('Inscription réussie !', 'success')
                    return redirect(url_for('login'))

    return render_template('register.html',
                           prenom_val=prenom_val,
                           nom_val=nom_val,
                           mdp_val=mdp_val,
                           ent_value=ent_value,
                           niveau=niveau)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Déconnecté avec succès.', 'info')
    return redirect(url_for('index'))

# ----------------- Lancement -----------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
