import os
from flask import Flask
from Class.CConfig import Config, db
from Controller.ApiUser import ApiUser
from Model import EntropyModel  # pour que SQLAlchemy connaisse les modèles

# Chemins absolus pour templates et static
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_FOLDER = os.path.join(BASE_DIR, 'Entropy', 'templates')
STATIC_FOLDER = os.path.join(BASE_DIR, 'Entropy', 'static')

# Création de l'app Flask
app = Flask(__name__, template_folder=TEMPLATE_FOLDER, static_folder=STATIC_FOLDER)

# Chargement de la configuration
app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
app.config['SECRET_KEY'] = Config.SECRET_KEY
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = Config.SQLALCHEMY_TRACK_MODIFICATIONS

# Initialisation de la base
db.init_app(app)

# Création des tables
with app.app_context():
    db.create_all()

# Enregistrement des blueprints
app.register_blueprint(ApiUser)

# Routes de test
@app.route("/health")
def health():
    return "OK"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)
