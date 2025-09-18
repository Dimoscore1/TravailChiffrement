from back.Controller.ApiUser import ApiUser
from back.Class.CConfig import Config, db

config = Config()
app = config.app

app.register_blueprint(ApiUser)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
