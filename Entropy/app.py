import os
from Class.CConfig import Config, db
from Controller.ApiUser import ApiUser
from Model import EntropyModel  # pour que SQLAlchemy connaisse les modèles

# Crée l’app Flask via Config
config = Config()  # c'est une instance
app = config.app

# Pas besoin de réaffecter SQLALCHEMY_DATABASE_URI ici, il est déjà dans config.app

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
