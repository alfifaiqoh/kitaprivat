from app import db


class PenilaianPerforma(db.Model):
    __tablename__ = 'penilaian_performa'

    id = db.Column(db.Integer, primary_key=True)
    tutor_id = db.Column(db.Integer, db.ForeignKey('tutor.id'), nullable=False)
    penugasan_id = db.Column(db.Integer, db.ForeignKey('penugasan.id'))
    penilai_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    tanggal = db.Column(db.Date, nullable=False)
    kedisiplinan = db.Column(db.Integer, nullable=False)
    penguasaan_materi = db.Column(db.Integer, nullable=False)
    komunikasi = db.Column(db.Integer, nullable=False)
    kehadiran = db.Column(db.Integer, nullable=False)
    total_skor = db.Column(db.Float)
    catatan = db.Column(db.Text)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    tutor = db.relationship('Tutor', backref='penilaian_list', lazy=True)
    penugasan = db.relationship('Penugasan', backref='penilaian_list', lazy=True)
    penilai = db.relationship('User', backref='penilaian_list', lazy=True)
