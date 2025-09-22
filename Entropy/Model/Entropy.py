from Entropy import db


class Entropy(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    prenom = db.Column(db.String(50), unique=True, nullable=False)
    nom = db.Column(db.String(50), nullable=False)
    mdpHache = db.Column(db.String(255), nullable=False)
    entropy = db.Column(db.Integer)