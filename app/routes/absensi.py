from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from flask_login import login_required, current_user
from app import db
from app.models.absensi import Absensi
from app.models.penugasan import Penugasan
from app.models.tutor import Tutor
from app.utils.helpers import save_base64_image

absensi_bp = Blueprint('absensi', __name__, url_prefix='/absensi')


@absensi_bp.route('/')
@login_required
def index():
    if current_user.role == 'tutor':
        tutor = Tutor.query.filter_by(user_id=current_user.id).first()
        data = Absensi.query.filter_by(tutor_id=tutor.id).order_by(Absensi.tanggal.desc()).all() if tutor else []
    else:
        data = Absensi.query.order_by(Absensi.tanggal.desc()).all()
    return render_template('pages/absensi/index.html', absensi_list=data)


@absensi_bp.route('/checkin', methods=['GET', 'POST'])
@login_required
def checkin():
    tutor = Tutor.query.filter_by(user_id=current_user.id).first_or_404()
    today = datetime.today().date()

    existing = Absensi.query.filter(
        Absensi.tutor_id == tutor.id,
        Absensi.tanggal == today,
        Absensi.jam_keluar.is_(None),
    ).first()

    if request.method == 'POST':
        penugasan_id = request.form.get('penugasan_id', type=int)
        selfie_data = request.form.get('selfie_data')
        gps_lat = request.form.get('gps_lat', type=float)
        gps_lng = request.form.get('gps_lng', type=float)
        now = datetime.now()

        if existing:
            a = existing
        else:
            a = Absensi(
                penugasan_id=penugasan_id,
                tutor_id=tutor.id,
                tanggal=today,
                status='masuk',
            )
            db.session.add(a)

        a.jam_masuk = now.strftime('%H:%M')
        a.gps_lat = gps_lat or a.gps_lat
        a.gps_lng = gps_lng or a.gps_lng
        if selfie_data:
            a.selfie = save_base64_image(selfie_data, 'selfie') or a.selfie
        a.status = 'masuk'
        db.session.commit()

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'ok': True, 'id': a.id, 'jam': a.jam_masuk})
        return redirect(url_for('absensi.status', id=a.id))

    penugasan_list = Penugasan.query.filter_by(tutor_id=tutor.id, status='aktif').all()
    return render_template('pages/absensi/checkin.html',
                           absensi=existing,
                           penugasan_list=penugasan_list,
                           today=today)


@absensi_bp.route('/checkout/<int:id>', methods=['POST'])
@login_required
def checkout(id):
    a = Absensi.query.get_or_404(id)
    a.jam_keluar = datetime.now().strftime('%H:%M')
    a.status = 'selesai'
    db.session.commit()
    return redirect(url_for('laporan.tambah', absensi_id=a.id, penugasan_id=a.penugasan_id))


@absensi_bp.route('/status/<int:id>')
@login_required
def status(id):
    a = Absensi.query.get_or_404(id)
    return render_template('pages/absensi/status.html', absensi=a)


@absensi_bp.route('/tambah', methods=['GET', 'POST'])
@login_required
def tambah():
    if request.method == 'POST':
        tgl = request.form.get('tanggal')
        selfie_file = save_base64_image(request.form.get('selfie_data', ''), 'selfie')
        a = Absensi(
            penugasan_id=request.form['penugasan_id'],
            tutor_id=request.form['tutor_id'],
            tanggal=datetime.strptime(tgl, '%Y-%m-%d') if tgl else datetime.today(),
            jam_masuk=request.form.get('jam_masuk'),
            jam_keluar=request.form.get('jam_keluar'),
            status=request.form.get('status', 'hadir'),
            gps_lat=request.form.get('gps_lat', type=float),
            gps_lng=request.form.get('gps_lng', type=float),
            selfie=selfie_file,
            keterangan=request.form.get('keterangan'),
        )
        db.session.add(a)
        db.session.commit()
        return redirect(url_for('absensi.index'))
    penugasan_list = Penugasan.query.filter_by(status='aktif').all()
    tutor_list = Tutor.query.all()
    return render_template('pages/absensi/form.html', absensi=None, penugasan_list=penugasan_list, tutor_list=tutor_list)


@absensi_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    a = Absensi.query.get_or_404(id)
    if request.method == 'POST':
        tgl = request.form.get('tanggal')
        selfie_file = save_base64_image(request.form.get('selfie_data', ''), 'selfie') or a.selfie
        a.penugasan_id = request.form['penugasan_id']
        a.tutor_id = request.form['tutor_id']
        a.tanggal = datetime.strptime(tgl, '%Y-%m-%d') if tgl else a.tanggal
        a.jam_masuk = request.form.get('jam_masuk')
        a.jam_keluar = request.form.get('jam_keluar')
        a.status = request.form.get('status', 'hadir')
        a.gps_lat = request.form.get('gps_lat', type=float)
        a.gps_lng = request.form.get('gps_lng', type=float)
        a.selfie = selfie_file
        a.keterangan = request.form.get('keterangan')
        db.session.commit()
        return redirect(url_for('absensi.index'))
    penugasan_list = Penugasan.query.filter_by(status='aktif').all()
    tutor_list = Tutor.query.all()
    return render_template('pages/absensi/form.html', absensi=a, penugasan_list=penugasan_list, tutor_list=tutor_list)


@absensi_bp.route('/hapus/<int:id>')
@login_required
def hapus(id):
    a = Absensi.query.get_or_404(id)
    db.session.delete(a)
    db.session.commit()
    return redirect(url_for('absensi.index'))
