from Class.CConfig import db

class EntropyModel(db.Model):
    __tablename__ = "entropy"

    id = db.Column(db.Integer, primary_key=True)
    prenom = db.Column(db.String(50), nullable=False)
    nom = db.Column(db.String(50), nullable=False)
    mdpHache = db.Column(db.String(255), nullable=False)
    entropy = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<EntropyModel {self.prenom} {self.nom}>"
