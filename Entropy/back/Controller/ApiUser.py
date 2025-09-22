import math
import hashlib
import requests

from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from back.Class.Authentification import Authentification


ApiUser = Blueprint("ApiUser", __name__)

# ---------------- Calcul de l'entropie ----------------
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

# ---------------- Calcul de la redondance ----------------
def calculer_redondance(mdp):
    if not mdp:
        return {"pct": 0, "bits": 0, "niveau": "N/A"}
    counts = {}
    for c in mdp:
        counts[c] = counts.get(c, 0) + 1
    total_repetitions = sum(count - 1 for count in counts.values() if count > 1)
    pct = total_repetitions / len(mdp) * 100
    bits = total_repetitions * 4  # estimation bits redondants
    if pct < 10:
        niveau = "Bien"
    elif pct < 25:
        niveau = "Moyen"
    else:
        niveau = "Faible"
    return {"pct": round(pct, 2), "bits": bits, "niveau": niveau}

# ---------------- Routes Flask ----------------
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
    red = {}
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
            red = calculer_redondance(mdp_val)
    return render_template('register.html',
                           prenom_val=prenom_val,
                           nom_val=nom_val,
                           mdp_val=mdp_val,
                           ent_value=ent_value,
                           niveau=niveau,
                           red=red)

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

# ---------------- Vérification mot de passe fuité ----------------
@ApiUser.route('/check_pwned', methods=['POST'])
def check_pwned():
    data = request.get_json()
    mdp = data.get("mdp", "")
    if not mdp:
        return jsonify({"error": "Mot de passe vide"}), 400

    sha1 = hashlib.sha1(mdp.encode("utf-8")).hexdigest().upper()
    prefix, suffix = sha1[:5], sha1[5:]
    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    try:
        res = requests.get(url)
        if res.status_code != 200:
            return jsonify({"error": "Impossible de vérifier le mot de passe"}), 500
        hashes = (line.split(":") for line in res.text.splitlines())
        if any(h == suffix for h, _ in hashes):
            return jsonify({"pwned": True})
        return jsonify({"pwned": False})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
