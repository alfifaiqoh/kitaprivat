from app import db


class Pembayaran(db.Model):
    __tablename__ = 'pembayaran'

    id = db.Column(db.Integer, primary_key=True)
    penugasan_id = db.Column(db.Integer, db.ForeignKey('penugasan.id'), nullable=False)
    jumlah = db.Column(db.Float, nullable=False)
    bulan = db.Column(db.String(7), nullable=False)
    status = db.Column(db.String(20), default='belum_dibayar')  # belum_dibayar, lunas, tertunda
    metode = db.Column(db.String(50))
    tanggal_bayar = db.Column(db.Date)
    keterangan = db.Column(db.Text)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    penugasan = db.relationship('Penugasan', backref='pembayaran_list', lazy=True)
