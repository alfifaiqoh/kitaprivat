from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from app import db
from app.models.penilaian import PenilaianPerforma
from app.models.penugasan import Penugasan
from app.models.tutor import Tutor
from app.utils.decorators import role_required

penilaian_bp = Blueprint('penilaian', __name__, url_prefix='/penilaian')


@penilaian_bp.route('/')
@login_required
def index():
    if current_user.role == 'tutor':
        tutor = Tutor.query.filter_by(user_id=current_user.id).first()
        data = PenilaianPerforma.query.filter_by(tutor_id=tutor.id).all() if tutor else []
    else:
        data = PenilaianPerforma.query.all()
    return render_template('pages/penilaian/index.html', penilaian_list=data)


@penilaian_bp.route('/tambah', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def tambah():
    if request.method == 'POST':
        tgl = request.form.get('tanggal')
        ked = int(request.form['kedisiplinan'])
        png = int(request.form['penguasaan_materi'])
        kom = int(request.form['komunikasi'])
        kdr = int(request.form['kehadiran'])
        total = (ked + png + kom + kdr) / 4.0

        p = PenilaianPerforma(
            tutor_id=request.form['tutor_id'],
            penugasan_id=request.form.get('penugasan_id', type=int),
            penilai_id=current_user.id,
            tanggal=datetime.strptime(tgl, '%Y-%m-%d') if tgl else datetime.today(),
            kedisiplinan=ked,
            penguasaan_materi=png,
            komunikasi=kom,
            kehadiran=kdr,
            total_skor=total,
            catatan=request.form.get('catatan'),
        )
        db.session.add(p)
        db.session.commit()
        return redirect(url_for('penilaian.index'))

    tutor_list = Tutor.query.all()
    penugasan_list = Penugasan.query.filter_by(status='aktif').all()
    return render_template('pages/penilaian/form.html', penilaian=None, tutor_list=tutor_list, penugasan_list=penugasan_list)


@penilaian_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def edit(id):
    p = PenilaianPerforma.query.get_or_404(id)
    if request.method == 'POST':
        tgl = request.form.get('tanggal')
        p.tutor_id = request.form['tutor_id']
        p.penugasan_id = request.form.get('penugasan_id', type=int)
        p.tanggal = datetime.strptime(tgl, '%Y-%m-%d') if tgl else p.tanggal
        p.kedisiplinan = int(request.form['kedisiplinan'])
        p.penguasaan_materi = int(request.form['penguasaan_materi'])
        p.komunikasi = int(request.form['komunikasi'])
        p.kehadiran = int(request.form['kehadiran'])
        p.total_skor = (p.kedisiplinan + p.penguasaan_materi + p.komunikasi + p.kehadiran) / 4.0
        p.catatan = request.form.get('catatan')
        db.session.commit()
        return redirect(url_for('penilaian.index'))

    tutor_list = Tutor.query.all()
    penugasan_list = Penugasan.query.filter_by(status='aktif').all()
    return render_template('pages/penilaian/form.html', penilaian=p, tutor_list=tutor_list, penugasan_list=penugasan_list)


@penilaian_bp.route('/hapus/<int:id>')
@login_required
@role_required('admin')
def hapus(id):
    p = PenilaianPerforma.query.get_or_404(id)
    db.session.delete(p)
    db.session.commit()
    return redirect(url_for('penilaian.index'))
