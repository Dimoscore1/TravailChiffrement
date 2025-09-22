from flask import Flask
from Class.CConfig import db, Config
from Controller.ApiUser import ApiUser, init_api

config = Config()
app = config.app  # Flask avec templates et static configurés

# Enregistrer le Blueprint site web
app.register_blueprint(ApiUser, url_prefix='')

# Initialiser Swagger API
api = init_api(app, prefix='/Api')

# ⚠️ Initialiser db UNE seule fois
db.init_app(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
