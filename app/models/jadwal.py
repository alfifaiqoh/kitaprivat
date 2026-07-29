from app import db


class Jadwal(db.Model):
    __tablename__ = 'jadwal'

    id = db.Column(db.Integer, primary_key=True)
    penugasan_id = db.Column(db.Integer, db.ForeignKey('penugasan.id'), nullable=False)
    hari = db.Column(db.String(20), nullable=False)
    jam_mulai = db.Column(db.String(5), nullable=False)
    jam_selesai = db.Column(db.String(5), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    penugasan = db.relationship('Penugasan', backref='jadwal_list', lazy=True)
