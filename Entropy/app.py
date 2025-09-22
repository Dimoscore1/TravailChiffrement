import os

from Class.CConfig import Config
from Controller.ApiUser import ApiUser
from Api import init_api  # ton API Swagger
from flask import Flask, render_template
from threading import Thread

# Initialisation de la config et de l'app
conf = Config()
app = conf.app

# Enregistrement du blueprint web
app.register_blueprint(ApiUser)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

def create_app():
    app = Flask(
        __name__,
        template_folder=os.path.join(BASE_DIR, "templates"),
        static_folder=os.path.join(BASE_DIR, "static")
    )
# Initialisation de l'API Swagger sur le même app mais sous /Api
api = init_api(app, prefix='/Api')  # on passe le préfixe pour Swagger

# Si tu veux lancer l'API sur un port séparé, tu peux utiliser un Thread (optionnel)
# Ici on garde tout sur le même port 5000, site web sur / et Swagger sur /Api

if __name__ == "__main__":
    app.run(debug=True, port=5000)
