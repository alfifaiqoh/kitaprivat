from app import db


class HonorTutor(db.Model):
    __tablename__ = 'honor_tutor'

    id = db.Column(db.Integer, primary_key=True)
    tutor_id = db.Column(db.Integer, db.ForeignKey('tutor.id'), nullable=False)
    bulan = db.Column(db.String(7), nullable=False)
    total_sesi = db.Column(db.Integer, default=0)
    tarif_per_sesi = db.Column(db.Float)
    total_honor = db.Column(db.Float)
    status = db.Column(db.String(20), default='belum_diajukan')
    # belum_diajukan, diajukan, dicairkan, dibatalkan
    catatan = db.Column(db.Text)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    tutor = db.relationship('Tutor', backref='honor_list', lazy=True)
