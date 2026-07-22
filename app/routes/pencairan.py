from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from app import db
from app.models.pencairan import PengajuanPencairan
from app.models.honor import HonorTutor
from app.models.tutor import Tutor
from app.utils.decorators import role_required

pencairan_bp = Blueprint('pencairan', __name__, url_prefix='/pencairan')


@pencairan_bp.route('/')
@login_required
def index():
    if current_user.role == 'tutor':
        tutor = Tutor.query.filter_by(user_id=current_user.id).first()
        data = PengajuanPencairan.query.filter_by(tutor_id=tutor.id).all() if tutor else []
    else:
        data = PengajuanPencairan.query.all()
    return render_template('pages/pencairan/index.html', pencairan_list=data)


@pencairan_bp.route('/tambah', methods=['GET', 'POST'])
@login_required
def tambah():
    if request.method == 'POST':
        p = PengajuanPencairan(
            tutor_id=request.form['tutor_id'],
            honor_tutor_id=request.form.get('honor_tutor_id', type=int),
            jumlah=request.form['jumlah'],
        )
        db.session.add(p)
        db.session.commit()
        if p.honor_tutor_id:
            honor = HonorTutor.query.get(p.honor_tutor_id)
            if honor:
                honor.status = 'diajukan'
                db.session.commit()
        return redirect(url_for('pencairan.index'))

    tutor_list = Tutor.query.all()
    honor_list = HonorTutor.query.filter_by(status='belum_diajukan').all()
    return render_template('pages/pencairan/form.html', pencairan=None, tutor_list=tutor_list, honor_list=honor_list)


@pencairan_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def edit(id):
    p = PengajuanPencairan.query.get_or_404(id)
    if request.method == 'POST':
        new_status = request.form['status']
        p.status = new_status
        p.catatan_admin = request.form.get('catatan_admin')
        now = datetime.now()
        if new_status == 'disetujui':
            p.tanggal_disetujui = now
        elif new_status == 'ditolak':
            p.tanggal_ditolak = now
        elif new_status == 'dicairkan':
            p.tanggal_dicairkan = now
        db.session.commit()
        if p.honor_tutor_id:
            honor = HonorTutor.query.get(p.honor_tutor_id)
            if honor:
                status_map = {'diajukan': 'diajukan', 'disetujui': 'diajukan', 'ditolak': 'dibatalkan', 'dicairkan': 'dicairkan'}
                honor.status = status_map.get(new_status, honor.status)
                db.session.commit()
        return redirect(url_for('pencairan.index'))

    return render_template('pages/pencairan/form.html', pencairan=p)


@pencairan_bp.route('/hapus/<int:id>')
@login_required
def hapus(id):
    p = PengajuanPencairan.query.get_or_404(id)
    db.session.delete(p)
    db.session.commit()
    return redirect(url_for('pencairan.index'))
