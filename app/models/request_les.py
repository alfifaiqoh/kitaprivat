from app import db


class RequestLes(db.Model):
    __tablename__ = 'request_les'

    id = db.Column(db.Integer, primary_key=True)
    siswa_id = db.Column(db.Integer, db.ForeignKey('siswa.id'), nullable=False)
    program_id = db.Column(db.Integer, db.ForeignKey('program.id'))
    paket_id = db.Column(db.Integer, db.ForeignKey('paket.id'))
    mata_pelajaran = db.Column(db.String(100))
    jadwal_diinginkan = db.Column(db.String(200))
    status = db.Column(db.String(30), default='baru')
    catatan = db.Column(db.Text)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    siswa = db.relationship('Siswa', backref='request_list', lazy=True)
