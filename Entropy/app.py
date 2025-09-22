import os
from Class.CConfig import Config, db
from Controller.ApiUser import ApiUser
from Model import EntropyModel  # obligatoire pour que SQLAlchemy connaisse les modèles

# Création de l’app Flask via Config
config = Config()
app = config.app

# Création des tables au démarrage
with app.app_context():
    db.create_all()

# Enregistrement du blueprint
app.register_blueprint(ApiUser)

@app.route("/health")
def health():
    return "OK"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)
