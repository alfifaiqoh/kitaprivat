from flask import Blueprint, render_template
from flask_login import login_required
from app import db
from app.models.pembayaran import Pembayaran
from app.models.honor import HonorTutor
from app.models.pencairan import PengajuanPencairan
from app.models.dompet import Dompet
from app.utils.decorators import role_required

keuangan_bp = Blueprint('keuangan', __name__, url_prefix='/admin/keuangan')


@keuangan_bp.route('/')
@login_required
@role_required('admin')
def index():
    total_pendapatan = db.session.query(db.func.sum(Pembayaran.jumlah)).filter_by(status='lunas').scalar() or 0
    total_honor = db.session.query(db.func.sum(HonorTutor.total_honor)).scalar() or 0
    total_pencairan = db.session.query(db.func.sum(PengajuanPencairan.jumlah)).filter_by(status='dicairkan').scalar() or 0
    total_komisi = total_pendapatan - total_honor
    return render_template('keuangan/index.html',
                           total_pendapatan=total_pendapatan,
                           total_honor=total_honor,
                           total_pencairan=total_pencairan,
                           total_komisi=total_komisi)
