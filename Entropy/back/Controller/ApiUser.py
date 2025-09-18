import math
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from back.Class.Authentification import Authentification

ApiUser = Blueprint("ApiUser", __name__)

def calculer_entropy(mdp):
    if not mdp:
        return None, None
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

@ApiUser.route('/')
def index():
    return render_template('index.html')

@ApiUser.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        prenom = request.form.get('prenom', '')
        mdp = request.form.get('mdp', '')
        success, message = Authentification.login(prenom, mdp)
        if success:
            return redirect(url_for('ApiUser.accueil'))
        flash(message, 'danger')
    return render_template('login.html')

@ApiUser.route('/register', methods=['GET', 'POST'])
def register():
    prenom_val = ""
    nom_val = ""
    mdp_val = ""
    ent_value = ""
    niveau = ""
    if request.method == 'POST':
        prenom_val = request.form.get('prenom', '')
        nom_val = request.form.get('nom', '')
        mdp_val = request.form.get('mdp', '')
        success, message = Authentification.register(prenom_val, nom_val, mdp_val, calculer_entropy)
        if success:
            flash(message, 'success')
            return redirect(url_for('ApiUser.login'))
        else:
            flash(message, 'warning')
        if mdp_val:
            ent_value, niveau = calculer_entropy(mdp_val)
    return render_template('register.html',
                           prenom_val=prenom_val,
                           nom_val=nom_val,
                           mdp_val=mdp_val,
                           ent_value=ent_value,
                           niveau=niveau)

@ApiUser.route('/accueil')
def accueil():
    if 'user_id' not in session:
        flash("Vous devez être connecté pour accéder à cette page.", "warning")
        return redirect(url_for('ApiUser.login'))
    return render_template('accueil.html')

@ApiUser.route('/logout')
def logout():
    Authentification.logout()
    flash('Déconnecté avec succès.', 'info')
    return redirect(url_for('ApiUser.index'))
