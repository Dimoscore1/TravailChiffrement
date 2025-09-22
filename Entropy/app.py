import os
from flask import Flask
from Class.CConfig import Config, db
from Controller.ApiUser import ApiUser
from Model import EntropyModel  # pour que SQLAlchemy connaisse les modèles

# Force le chemin absolu des templates et static
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_FOLDER = os.path.join(BASE_DIR, 'Entropy', 'templates')
STATIC_FOLDER = os.path.join(BASE_DIR, 'Entropy', 'static')

# Crée l'app Flask
app = Flask(__name__, template_folder=TEMPLATE_FOLDER, static_folder=STATIC_FOLDER)

# Charge la configuration
config = Config()
app.config.update(config.get_config())  # si tu as une méthode get_config() pour tes variables

# Initialise SQLAlchemy
db.init_app(app)

# Crée les tables si elles n'existent pas
with app.app_context():
    db.create_all()

# Enregistre le blueprint
app.register_blueprint(ApiUser)

# Routes de test / health
@app.route("/health")
def health():
    return "OK"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)
