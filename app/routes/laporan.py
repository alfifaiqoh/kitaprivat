from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from app import db
from app.models.laporan import Laporan
from app.models.absensi import Absensi
from app.models.penugasan import Penugasan
from app.models.tutor import Tutor

laporan_bp = Blueprint('laporan', __name__, url_prefix='/laporan')


@laporan_bp.route('/')
@login_required
def index():
    if current_user.role == 'tutor':
        tutor = Tutor.query.filter_by(user_id=current_user.id).first()
        data = Laporan.query.filter_by(tutor_id=tutor.id).order_by(Laporan.tanggal.desc()).all() if tutor else []
    else:
        data = Laporan.query.order_by(Laporan.tanggal.desc()).all()
    return render_template('pages/laporan/index.html', laporan_list=data)


@laporan_bp.route('/tambah', methods=['GET', 'POST'])
@login_required
def tambah():
    tutor = Tutor.query.filter_by(user_id=current_user.id).first()
    absensi_id = request.args.get('absensi_id', type=int)
    preselected_penugasan = request.args.get('penugasan_id', type=int)

    if request.method == 'POST':
        tgl = request.form.get('tanggal')
        l = Laporan(
            penugasan_id=request.form['penugasan_id'],
            tutor_id=request.form['tutor_id'],
            tanggal=datetime.strptime(tgl, '%Y-%m-%d') if tgl else datetime.today(),
            materi=request.form['materi'],
            catatan=request.form.get('catatan'),
            pr=request.form.get('pr'),
            hadir=request.form.get('hadir') == 'on',
            absensi_id=request.form.get('absensi_id', type=int),
        )
        db.session.add(l)
        db.session.commit()

        if request.form.get('absensi_id'):
            absensi = Absensi.query.get(int(request.form['absensi_id']))
            if absensi:
                absensi.status = 'laporan'
                db.session.commit()

        return redirect(url_for('laporan.index'))

    penugasan_list = Penugasan.query.filter_by(status='aktif').all()
    if current_user.role == 'tutor' and tutor:
        penugasan_list = Penugasan.query.filter_by(tutor_id=tutor.id, status='aktif').all()
    tutor_list = Tutor.query.all()

    return render_template('pages/laporan/form.html',
                           laporan=None,
                           penugasan_list=penugasan_list,
                           tutor_list=tutor_list,
                           absensi_id=absensi_id,
                           preselected_penugasan=preselected_penugasan)


@laporan_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    l = Laporan.query.get_or_404(id)
    if request.method == 'POST':
        tgl = request.form.get('tanggal')
        l.penugasan_id = request.form['penugasan_id']
        l.tutor_id = request.form['tutor_id']
        l.tanggal = datetime.strptime(tgl, '%Y-%m-%d') if tgl else l.tanggal
        l.materi = request.form['materi']
        l.catatan = request.form.get('catatan')
        l.pr = request.form.get('pr')
        l.hadir = request.form.get('hadir') == 'on'
        db.session.commit()
        return redirect(url_for('laporan.index'))
    penugasan_list = Penugasan.query.filter_by(status='aktif').all()
    tutor_list = Tutor.query.all()
    return render_template('pages/laporan/form.html', laporan=l, penugasan_list=penugasan_list, tutor_list=tutor_list)


@laporan_bp.route('/hapus/<int:id>')
@login_required
def hapus(id):
    l = Laporan.query.get_or_404(id)
    db.session.delete(l)
    db.session.commit()
    return redirect(url_for('laporan.index'))
