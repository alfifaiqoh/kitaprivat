from app import db

class Siswa(db.Model):
    __tablename__ = 'siswa'

    id = db.Column(db.Integer, primary_key=True)
    orang_tua_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    nama = db.Column(db.String(100), nullable=False)
    sekolah = db.Column(db.String(100))
    kelas = db.Column(db.String(20))
    jenis_kelamin = db.Column(db.String(10))
    tanggal_lahir = db.Column(db.Date)
    alamat = db.Column(db.Text)
    telepon = db.Column(db.String(20))
    email = db.Column(db.String(120))
    mata_pelajaran = db.Column(db.String(200))
    jadwal_diinginkan = db.Column(db.String(200))
    keterangan = db.Column(db.Text)
    status = db.Column(db.String(20), default='aktif')  # baru, aktif, nonaktif
    aktif = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    orang_tua = db.relationship('User', backref='siswa_list', lazy=True)
