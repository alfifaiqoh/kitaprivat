from app import db

class Jenjang(db.Model):
    __tablename__ = 'jenjang'

    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    program_list = db.relationship('Program', backref='jenjang', lazy=True)
