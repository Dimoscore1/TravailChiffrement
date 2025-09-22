from Class.CConfig import db

class EntropyModel(db.Model):
    __tablename__ = 'entropy'
    id = db.Column(db.Integer, primary_key=True)
    prenom = db.Column(db.String(50), unique=True, nullable=False)
    nom = db.Column(db.String(50), nullable=False)
    mdpHache = db.Column(db.String(255), nullable=False)
    entropy = db.Column(db.Integer, nullable=True)
