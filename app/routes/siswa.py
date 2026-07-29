from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from app import db
from app.models.siswa import Siswa
from app.utils.decorators import role_required

siswa_bp = Blueprint('siswa', __name__, url_prefix='/siswa')


@siswa_bp.route('/')
@login_required
def index():
    tab = request.args.get('tab', 'aktif')
    if current_user.role == 'orang_tua':
        base = Siswa.query.filter_by(orang_tua_id=current_user.id)
    else:
        base = Siswa.query

    if tab == 'baru':
        data = base.filter_by(status='baru').order_by(Siswa.created_at.desc()).all()
    elif tab == 'nonaktif':
        data = base.filter_by(status='nonaktif').order_by(Siswa.nama).all()
    else:
        data = base.filter_by(status='aktif').order_by(Siswa.nama).all()

    return render_template('pages/siswa/index.html', siswa_list=data, tab=tab)


@siswa_bp.route('/tambah', methods=['GET', 'POST'])
@login_required
def tambah():
    if request.method == 'POST':
        tgl = request.form.get('tanggal_lahir')
        s = Siswa(
            nama=request.form['nama'],
            jenis_kelamin=request.form.get('jenis_kelamin'),
            tanggal_lahir=datetime.strptime(tgl, '%Y-%m-%d') if tgl else None,
            kelas=request.form.get('kelas'),
            sekolah=request.form.get('sekolah'),
            alamat=request.form.get('alamat'),
            telepon=request.form.get('telepon'),
            email=request.form.get('email'),
            mata_pelajaran=request.form.get('mata_pelajaran'),
            jadwal_diinginkan=request.form.get('jadwal_diinginkan'),
            orang_tua_id=current_user.id if current_user.role == 'orang_tua' else request.form.get('orang_tua_id'),
            keterangan=request.form.get('keterangan'),
            status='aktif',
        )
        db.session.add(s)
        db.session.commit()
        return redirect(url_for('siswa.index'))
    return render_template('pages/siswa/form.html', siswa=None)


@siswa_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    s = Siswa.query.get_or_404(id)
    if request.method == 'POST':
        tgl = request.form.get('tanggal_lahir')
        s.nama = request.form['nama']
        s.jenis_kelamin = request.form.get('jenis_kelamin')
        s.tanggal_lahir = datetime.strptime(tgl, '%Y-%m-%d') if tgl else None
        s.kelas = request.form.get('kelas')
        s.sekolah = request.form.get('sekolah')
        s.alamat = request.form.get('alamat')
        s.telepon = request.form.get('telepon')
        s.email = request.form.get('email')
        s.mata_pelajaran = request.form.get('mata_pelajaran')
        s.jadwal_diinginkan = request.form.get('jadwal_diinginkan')
        s.keterangan = request.form.get('keterangan')
        db.session.commit()
        return redirect(url_for('siswa.index'))
    return render_template('pages/siswa/form.html', siswa=s)


@siswa_bp.route('/terima/<int:id>')
@login_required
@role_required('admin')
def terima(id):
    s = Siswa.query.get_or_404(id)
    s.status = 'aktif'
    db.session.commit()
    return redirect(url_for('siswa.index', tab='baru'))


@siswa_bp.route('/detail/<int:id>')
@login_required
def detail(id):
    s = Siswa.query.get_or_404(id)
    return render_template('pages/siswa/detail.html', s=s)


@siswa_bp.route('/hapus/<int:id>')
@login_required
@role_required('admin')
def hapus(id):
    s = Siswa.query.get_or_404(id)
    db.session.delete(s)
    db.session.commit()
    return redirect(url_for('siswa.index'))


@siswa_bp.route('/daftar', methods=['GET', 'POST'])
def daftar():
    if request.method == 'POST':
        tgl = request.form.get('tanggal_lahir')
        s = Siswa(
            nama=request.form['nama'],
            jenis_kelamin=request.form.get('jenis_kelamin'),
            tanggal_lahir=datetime.strptime(tgl, '%Y-%m-%d') if tgl else None,
            kelas=request.form.get('kelas'),
            sekolah=request.form.get('sekolah'),
            alamat=request.form.get('alamat'),
            telepon=request.form.get('telepon'),
            email=request.form.get('email'),
            mata_pelajaran=request.form.get('mata_pelajaran'),
            jadwal_diinginkan=request.form.get('jadwal_diinginkan'),
            keterangan=request.form.get('keterangan'),
            status='baru',
        )
        db.session.add(s)
        db.session.commit()
        return redirect(url_for('siswa.sukses'))
    return render_template('pages/siswa/daftar.html')


@siswa_bp.route('/daftar/sukses')
def sukses():
    return render_template('pages/siswa/sukses.html')
