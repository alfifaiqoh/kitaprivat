from app import db


class Tutor(db.Model):
    __tablename__ = 'tutor'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)
    bidang = db.Column(db.String(100))
    pengalaman = db.Column(db.Text)
    pendidikan = db.Column(db.String(100))
    tarif_per_sesi = db.Column(db.Float)
    bank_nama = db.Column(db.String(50))
    bank_akun = db.Column(db.String(50))
    rating = db.Column(db.Float, default=0)
    status = db.Column(db.String(20), default='aktif')
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    user = db.relationship('User', backref='tutor_profile', uselist=False, lazy=True)
