from app import db


class Penugasan(db.Model):
    __tablename__ = 'penugasan'

    id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.Integer, db.ForeignKey('request_les.id'))
    siswa_id = db.Column(db.Integer, db.ForeignKey('siswa.id'), nullable=False)
    tutor_id = db.Column(db.Integer, db.ForeignKey('tutor.id'), nullable=False)
    mata_pelajaran = db.Column(db.String(100), nullable=False)
    tarif = db.Column(db.Float)
    status = db.Column(db.String(20), default='aktif')
    assigned_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    assigned_at = db.Column(db.DateTime, server_default=db.func.now())
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    siswa = db.relationship('Siswa', backref='penugasan_list', lazy=True)
    tutor = db.relationship('Tutor', backref='penugasan_list', lazy=True)
    admin = db.relationship('User', backref='penugasan_admin', lazy=True)
