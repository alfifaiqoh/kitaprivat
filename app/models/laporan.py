from app import db


class Laporan(db.Model):
    __tablename__ = 'laporan'

    id = db.Column(db.Integer, primary_key=True)
    penugasan_id = db.Column(db.Integer, db.ForeignKey('penugasan.id'), nullable=False)
    tutor_id = db.Column(db.Integer, db.ForeignKey('tutor.id'), nullable=False)
    tanggal = db.Column(db.Date, nullable=False)
    materi = db.Column(db.Text, nullable=False)
    catatan = db.Column(db.Text)
    pr = db.Column(db.Text)
    hadir = db.Column(db.Boolean, default=True)
    absensi_id = db.Column(db.Integer, db.ForeignKey('absensi.id'))
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    penugasan = db.relationship('Penugasan', backref='laporan_list', lazy=True)
    tutor = db.relationship('Tutor', backref='laporan_list', lazy=True)
