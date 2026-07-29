from app import db

class Wilayah(db.Model):
    __tablename__ = 'wilayah'

    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
