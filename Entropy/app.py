import os
from flask import Flask
from Controller.ApiUser import ApiUser  # ton blueprint

# ---------------- Création de l'application Flask ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, 'templates'),  # Entropy/templates
    static_folder=os.path.join(BASE_DIR, 'static')        # Entropy/static
)

# Clé secrète pour les sessions Flask
app.secret_key = os.environ.get('SECRET_KEY', 'dev_secret_key')

# ---------------- Enregistrement du blueprint ----------------
app.register_blueprint(ApiUser)

# ---------------- Route par défaut / test ----------------
@app.route('/health')
def health():
    return "OK"

# ---------------- Main ----------------
if __name__ == "__main__":
    # Affiche toutes les routes pour debug
    print(app.url_map)

    # Lancer l'app en local
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=True)
