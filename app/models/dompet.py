from app import db

class Dompet(db.Model):
    __tablename__ = 'dompet'

    id = db.Column(db.Integer, primary_key=True)
    tutor_id = db.Column(db.Integer, db.ForeignKey('tutor.id'), unique=True)
    saldo = db.Column(db.Float, default=0)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    tutor = db.relationship('Tutor', backref='dompet', uselist=False, lazy=True)
