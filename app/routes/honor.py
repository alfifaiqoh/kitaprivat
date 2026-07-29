from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from app import db
from app.models.honor import HonorTutor
from app.models.absensi import Absensi
from app.models.tutor import Tutor
from app.utils.decorators import role_required

honor_bp = Blueprint('honor', __name__, url_prefix='/honor')


@honor_bp.route('/')
@login_required
def index():
    if current_user.role == 'tutor':
        tutor = Tutor.query.filter_by(user_id=current_user.id).first()
        data = HonorTutor.query.filter_by(tutor_id=tutor.id).all() if tutor else []
    else:
        data = HonorTutor.query.all()
    return render_template('pages/honor/index.html', honor_list=data)


@honor_bp.route('/generate', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def generate():
    if request.method == 'POST':
        bulan = request.form['bulan']
        tutor_id = request.form.get('tutor_id', type=int)
        tutor = Tutor.query.get(tutor_id)
        if not tutor:
            return redirect(url_for('honor.index'))

        sesi = Absensi.query.filter(
            Absensi.tutor_id == tutor_id,
            db.func.strftime('%Y-%m', Absensi.tanggal) == bulan,
            Absensi.status == 'hadir',
        ).count()

        existing = HonorTutor.query.filter_by(tutor_id=tutor_id, bulan=bulan).first()
        if existing:
            existing.total_sesi = sesi
            existing.tarif_per_sesi = tutor.tarif_per_sesi
            existing.total_honor = sesi * (tutor.tarif_per_sesi or 0)
        else:
            h = HonorTutor(
                tutor_id=tutor_id,
                bulan=bulan,
                total_sesi=sesi,
                tarif_per_sesi=tutor.tarif_per_sesi,
                total_honor=sesi * (tutor.tarif_per_sesi or 0),
            )
            db.session.add(h)
        db.session.commit()
        return redirect(url_for('honor.index'))

    tutor_list = Tutor.query.all()
    return render_template('pages/honor/generate.html', tutor_list=tutor_list)


@honor_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def edit(id):
    h = HonorTutor.query.get_or_404(id)
    if request.method == 'POST':
        h.status = request.form.get('status', h.status)
        h.catatan = request.form.get('catatan')
        db.session.commit()
        return redirect(url_for('honor.index'))
    return render_template('pages/honor/form.html', honor=h)


@honor_bp.route('/hapus/<int:id>')
@login_required
@role_required('admin')
def hapus(id):
    h = HonorTutor.query.get_or_404(id)
    db.session.delete(h)
    db.session.commit()
    return redirect(url_for('honor.index'))
