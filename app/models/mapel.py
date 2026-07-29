from app import db

class MataPelajaran(db.Model):
    __tablename__ = 'mata_pelajaran'

    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)
    kategori = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
