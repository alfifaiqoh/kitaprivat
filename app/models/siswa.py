from app import db


class Siswa(db.Model):
    __tablename__ = 'siswa'

    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)
    kelas = db.Column(db.String(20))
    sekolah = db.Column(db.String(100))
    alamat = db.Column(db.Text)
    telepon = db.Column(db.String(20))
    email = db.Column(db.String(120))
    orang_tua_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    keterangan = db.Column(db.Text)
    aktif = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    orang_tua = db.relationship('User', backref='siswa_list', lazy=True)
