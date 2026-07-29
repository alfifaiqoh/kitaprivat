from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models.siswa import Siswa
from app.models.penugasan import Penugasan
from app.models.invoice import Invoice
from app.models.pembayaran import Pembayaran
from app.models.laporan import Laporan

parent_bp = Blueprint('parent', __name__, url_prefix='/orang-tua')


@parent_bp.route('/dashboard')
@login_required
def dashboard():
    siswa_list = Siswa.query.filter_by(orang_tua_id=current_user.id).all()
    siswa_ids = [s.id for s in siswa_list]
    penugasan_list = Penugasan.query.filter(Penugasan.siswa_id.in_(siswa_ids)).all() if siswa_ids else []
    invoice_list = Invoice.query.filter(Invoice.siswa_id.in_(siswa_ids)).all() if siswa_ids else []
    return render_template('parent/dashboard.html',
                           siswa_list=siswa_list,
                           penugasan_list=penugasan_list,
                           invoice_list=invoice_list)


@parent_bp.route('/progress')
@login_required
def progress():
    siswa_list = Siswa.query.filter_by(orang_tua_id=current_user.id).all()
    siswa_ids = [s.id for s in siswa_list]
    penugasan_list = Penugasan.query.filter(Penugasan.siswa_id.in_(siswa_ids)).all() if siswa_ids else []
    penugasan_ids = [p.id for p in penugasan_list]
    laporan_list = Laporan.query.filter(Laporan.penugasan_id.in_(penugasan_ids)).order_by(Laporan.tanggal.desc()).all() if penugasan_ids else []
    return render_template('parent/progress.html',
                           siswa_list=siswa_list,
                           laporan_list=laporan_list)


@parent_bp.route('/tagihan')
@login_required
def tagihan():
    siswa_list = Siswa.query.filter_by(orang_tua_id=current_user.id).all()
    siswa_ids = [s.id for s in siswa_list]
    invoice_list = Invoice.query.filter(Invoice.siswa_id.in_(siswa_ids)).order_by(Invoice.created_at.desc()).all() if siswa_ids else []
    return render_template('parent/tagihan.html', invoice_list=invoice_list, siswa_list=siswa_list)


@parent_bp.route('/pengumuman')
@login_required
def pengumuman():
    return render_template('parent/pengumuman.html')
