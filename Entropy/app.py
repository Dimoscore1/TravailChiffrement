from flask import Flask
from Class.CConfig import db, Config
from Controller.ApiUser import ApiUser, init_api

# Instanciation de l'application Flask avec chemins absolus pour templates et static
config = Config()
app = config.app  # Contient template_folder et static_folder configurés

# Enregistrer le Blueprint site web (login, register, accueil)
app.register_blueprint(ApiUser, url_prefix='')  # accessible sur /

# Initialiser Swagger API sur /Api
api = init_api(app, prefix='/Api')

# Initialiser SQLAlchemy (déjà fait dans Config)
db.init_app(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
