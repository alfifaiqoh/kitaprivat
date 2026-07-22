from app import db


class RekrutmenTutor(db.Model):
    __tablename__ = 'rekrutmen_tutor'

    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    telepon = db.Column(db.String(20))
    alamat = db.Column(db.Text)
    bidang = db.Column(db.String(100))
    pendidikan = db.Column(db.String(100))
    pengalaman = db.Column(db.Text)

    ktp = db.Column(db.String(255))
    cv = db.Column(db.String(255))
    ijazah = db.Column(db.String(255))
    transkrip = db.Column(db.String(255))
    sertifikat = db.Column(db.String(255))

    status = db.Column(db.String(20), default='menunggu')
    catatan_admin = db.Column(db.Text)
    tanggal_interview = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
