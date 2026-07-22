from app import db


class Penugasan(db.Model):
    __tablename__ = 'penugasan'

    id = db.Column(db.Integer, primary_key=True)
    siswa_id = db.Column(db.Integer, db.ForeignKey('siswa.id'), nullable=False)
    tutor_id = db.Column(db.Integer, db.ForeignKey('tutor.id'), nullable=False)
    mata_pelajaran = db.Column(db.String(100), nullable=False)
    tarif = db.Column(db.Float)
    status = db.Column(db.String(20), default='aktif')  # aktif, selesai, dibatalkan
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    siswa = db.relationship('Siswa', backref='penugasan_list', lazy=True)
    tutor = db.relationship('Tutor', backref='penugasan_list', lazy=True)
