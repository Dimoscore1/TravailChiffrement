import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from Controller.ApiUser import init_api  # ton code API

db = SQLAlchemy()

class Config:
    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        template_dir = os.path.join(base_dir, 'templates')
        static_dir = os.path.join(base_dir, 'static')

        self.app = Flask(
            __name__,
            template_folder=template_dir,
            static_folder=static_dir
        )

        self.app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'ma_cle_secrete')
        self.app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('POSTGRES_SERVER')
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        db.init_app(self.app)

# Initialisation
config = Config()
app = config.app

# API Swagger sur /Api/
api = init_api(app, prefix='/Api')

# ---------------- Routes Web ----------------
@app.route('/')
def index():
    return render_template('index.html')

# ---------------- Run ----------------
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
