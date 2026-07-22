from app import db


class Absensi(db.Model):
    __tablename__ = 'absensi'

    id = db.Column(db.Integer, primary_key=True)
    penugasan_id = db.Column(db.Integer, db.ForeignKey('penugasan.id'), nullable=False)
    tutor_id = db.Column(db.Integer, db.ForeignKey('tutor.id'), nullable=False)
    tanggal = db.Column(db.Date, nullable=False)
    jam_masuk = db.Column(db.String(5))
    jam_keluar = db.Column(db.String(5))
    status = db.Column(db.String(10), default='hadir')  # hadir, izin, sakit, alpha
    gps_lat = db.Column(db.Float)
    gps_lng = db.Column(db.Float)
    selfie = db.Column(db.String(255))
    keterangan = db.Column(db.Text)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    penugasan = db.relationship('Penugasan', backref='absensi_list', lazy=True)
    tutor = db.relationship('Tutor', backref='absensi_list', lazy=True)
