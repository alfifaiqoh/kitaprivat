from app import db


class PengajuanPencairan(db.Model):
    __tablename__ = 'pengajuan_pencairan'

    id = db.Column(db.Integer, primary_key=True)
    tutor_id = db.Column(db.Integer, db.ForeignKey('tutor.id'), nullable=False)
    honor_tutor_id = db.Column(db.Integer, db.ForeignKey('honor_tutor.id'))
    jumlah = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='diajukan')
    # diajukan, disetujui, ditolak, dicairkan
    tanggal_diajukan = db.Column(db.DateTime, server_default=db.func.now())
    tanggal_disetujui = db.Column(db.DateTime)
    tanggal_ditolak = db.Column(db.DateTime)
    tanggal_dicairkan = db.Column(db.DateTime)
    catatan_admin = db.Column(db.Text)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    tutor = db.relationship('Tutor', backref='pencairan_list', lazy=True)
    honor_tutor = db.relationship('HonorTutor', backref='pencairan_list', lazy=True)
