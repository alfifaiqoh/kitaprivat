from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from app import db
from app.models.penugasan import Penugasan
from app.models.siswa import Siswa
from app.models.tutor import Tutor

penugasan_bp = Blueprint('penugasan', __name__, url_prefix='/penugasan')


@penugasan_bp.route('/')
@login_required
def index():
    if current_user.role == 'tutor':
        tutor = Tutor.query.filter_by(user_id=current_user.id).first()
        data = Penugasan.query.filter_by(tutor_id=tutor.id).all() if tutor else []
    elif current_user.role == 'orang_tua':
        siswa_ids = [s.id for s in Siswa.query.filter_by(orang_tua_id=current_user.id).all()]
        data = Penugasan.query.filter(Penugasan.siswa_id.in_(siswa_ids)).all() if siswa_ids else []
    else:
        data = Penugasan.query.all()
    return render_template('pages/penugasan/index.html', penugasan_list=data)


@penugasan_bp.route('/tambah', methods=['GET', 'POST'])
@login_required
def tambah():
    if request.method == 'POST':
        p = Penugasan(
            siswa_id=request.form['siswa_id'],
            tutor_id=request.form['tutor_id'],
            mata_pelajaran=request.form['mata_pelajaran'],
            tarif=request.form.get('tarif', type=float),
            status=request.form.get('status', 'aktif'),
        )
        db.session.add(p)
        db.session.commit()
        return redirect(url_for('penugasan.index'))
    siswa_list = Siswa.query.filter_by(aktif=True).all()
    tutor_list = Tutor.query.all()
    return render_template('pages/penugasan/form.html', penugasan=None, siswa_list=siswa_list, tutor_list=tutor_list)


@penugasan_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    p = Penugasan.query.get_or_404(id)
    if request.method == 'POST':
        p.siswa_id = request.form['siswa_id']
        p.tutor_id = request.form['tutor_id']
        p.mata_pelajaran = request.form['mata_pelajaran']
        p.tarif = request.form.get('tarif', type=float)
        p.status = request.form.get('status', 'aktif')
        db.session.commit()
        return redirect(url_for('penugasan.index'))
    siswa_list = Siswa.query.filter_by(aktif=True).all()
    tutor_list = Tutor.query.all()
    return render_template('pages/penugasan/form.html', penugasan=p, siswa_list=siswa_list, tutor_list=tutor_list)


@penugasan_bp.route('/hapus/<int:id>')
@login_required
def hapus(id):
    p = Penugasan.query.get_or_404(id)
    db.session.delete(p)
    db.session.commit()
    return redirect(url_for('penugasan.index'))
