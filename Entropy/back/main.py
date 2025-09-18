from flask import Flask
from flasgger import Swagger
from os import path
from secrets import token_hex
import logging
from Class.CConfig import Config

from db import userDb

if(__name__ == "__main__"):
    app:Flask = Flask(import_name="app")
    app.logger.setLevel(logging.INFO)
    app.config["SECRET_KEY"] = token_hex(16)
    swagger = Swagger(app)

    # registering controllers
    from Controller.ApiUser import UserBP
    app.register_blueprint(UserBP)

    # Importing config
    config = Config(app)

    # Database Parameters
    param_bdd = f"postgresql+pg8000://{config.PostgresUsername}:{config.PostgresPassword}@{config.PostgresServer}/userDb"
    app.config['SQLALCHEMY_DATABASE_URI'] = param_bdd
    # Creating database instance
    userDb.init_app(app)

    from Model.User import User
    with app.app_context():
        from base import Base
        Base.metadata.create_all(userDb.engine)

    @app.get("/")
    def root():
        return "ok"

    app.run(host='0.0.0.0', port=5000)