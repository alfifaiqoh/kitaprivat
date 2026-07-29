from app import db

class Invoice(db.Model):
    __tablename__ = 'invoice'

    id = db.Column(db.Integer, primary_key=True)
    nomor_invoice = db.Column(db.String(20), unique=True, nullable=False)
    siswa_id = db.Column(db.Integer, db.ForeignKey('siswa.id'), nullable=False)
    tipe = db.Column(db.String(30), nullable=False)
    jumlah = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='draft')
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    jatuh_tempo = db.Column(db.Date)
    keterangan = db.Column(db.Text)

    siswa = db.relationship('Siswa', backref='invoice_list', lazy=True)

    @staticmethod
    def generate_nomor():
        last = Invoice.query.order_by(Invoice.id.desc()).first()
        num = (last.id + 1) if last else 1
        return f'INV-{num:04d}'
