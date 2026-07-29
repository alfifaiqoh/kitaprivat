from app import db

class Paket(db.Model):
    __tablename__ = 'paket'

    id = db.Column(db.Integer, primary_key=True)
    program_id = db.Column(db.Integer, db.ForeignKey('program.id'), nullable=False)
    nama = db.Column(db.String(100), nullable=False)
    jumlah_pertemuan = db.Column(db.Integer, default=0)
    harga = db.Column(db.Float, default=0)
    durasi_per_sesi = db.Column(db.Integer, default=60)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
