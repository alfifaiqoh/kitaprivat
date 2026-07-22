from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from app import db
from app.models.siswa import Siswa
from app.utils.decorators import role_required

siswa_bp = Blueprint('siswa', __name__, url_prefix='/siswa')


@siswa_bp.route('/')
@login_required
def index():
    if current_user.role == 'orang_tua':
        data = Siswa.query.filter_by(orang_tua_id=current_user.id).all()
    else:
        data = Siswa.query.all()
    return render_template('pages/siswa/index.html', siswa_list=data)


@siswa_bp.route('/tambah', methods=['GET', 'POST'])
@login_required
def tambah():
    if request.method == 'POST':
        s = Siswa(
            nama=request.form['nama'],
            kelas=request.form.get('kelas'),
            sekolah=request.form.get('sekolah'),
            alamat=request.form.get('alamat'),
            telepon=request.form.get('telepon'),
            email=request.form.get('email'),
            orang_tua_id=current_user.id if current_user.role == 'orang_tua' else request.form.get('orang_tua_id'),
            keterangan=request.form.get('keterangan'),
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
        s.nama = request.form['nama']
        s.kelas = request.form.get('kelas')
        s.sekolah = request.form.get('sekolah')
        s.alamat = request.form.get('alamat')
        s.telepon = request.form.get('telepon')
        s.email = request.form.get('email')
        s.keterangan = request.form.get('keterangan')
        db.session.commit()
        return redirect(url_for('siswa.index'))
    return render_template('pages/siswa/form.html', siswa=s)


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
        s = Siswa(
            nama=request.form['nama'],
            kelas=request.form.get('kelas'),
            sekolah=request.form.get('sekolah'),
            alamat=request.form.get('alamat'),
            telepon=request.form.get('telepon'),
            email=request.form.get('email'),
            keterangan=request.form.get('keterangan'),
        )
        db.session.add(s)
        db.session.commit()
        return redirect(url_for('auth.login'))
    return render_template('pages/siswa/daftar.html')
