from app import db


class Pengumuman(db.Model):
    __tablename__ = 'pengumuman'

    id = db.Column(db.Integer, primary_key=True)
    judul = db.Column(db.String(200), nullable=False)
    isi = db.Column(db.Text, nullable=False)
    target = db.Column(db.String(20), default='semua')
    aktif = db.Column(db.Boolean, default=True)
    dibuat_oleh = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    pembuat = db.relationship('User', backref='pengumuman_list', lazy=True)
