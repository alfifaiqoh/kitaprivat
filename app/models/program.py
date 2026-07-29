from app import db

class Program(db.Model):
    __tablename__ = 'program'

    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)
    deskripsi = db.Column(db.Text)
    jenjang_id = db.Column(db.Integer, db.ForeignKey('jenjang.id'))
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    paket_list = db.relationship('Paket', backref='program', lazy=True)
