from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from app import db
from app.models.tutor import Tutor
from app.models.user import User
from app.utils.decorators import role_required

tutor_bp = Blueprint('tutor', __name__, url_prefix='/tutor')


@tutor_bp.route('/')
@login_required
def index():
    if current_user.role == 'tutor':
        data = Tutor.query.filter_by(user_id=current_user.id).all()
    else:
        data = Tutor.query.all()
    return render_template('pages/tutor/index.html', tutor_list=data)


@tutor_bp.route('/tambah', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def tambah():
    if request.method == 'POST':
        user = User(
            username=request.form['username'],
            nama=request.form['nama'],
            role='tutor',
            email=request.form.get('email'),
            telepon=request.form.get('telepon'),
        )
        user.set_password(request.form['password'])
        db.session.add(user)
        db.session.flush()

        t = Tutor(
            user_id=user.id,
            bidang=request.form.get('bidang'),
            pengalaman=request.form.get('pengalaman'),
            pendidikan=request.form.get('pendidikan'),
            tarif_per_sesi=request.form.get('tarif_per_sesi', type=float),
            bank_nama=request.form.get('bank_nama'),
            bank_akun=request.form.get('bank_akun'),
        )
        db.session.add(t)
        db.session.commit()
        return redirect(url_for('tutor.index'))

    return render_template('pages/tutor/form.html', tutor=None)


@tutor_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def edit(id):
    t = Tutor.query.get_or_404(id)
    if request.method == 'POST':
        t.user.nama = request.form['nama']
        t.user.email = request.form.get('email')
        t.user.telepon = request.form.get('telepon')
        t.bidang = request.form.get('bidang')
        t.pengalaman = request.form.get('pengalaman')
        t.pendidikan = request.form.get('pendidikan')
        t.tarif_per_sesi = request.form.get('tarif_per_sesi', type=float)
        t.bank_nama = request.form.get('bank_nama')
        t.bank_akun = request.form.get('bank_akun')
        if request.form.get('password'):
            t.user.set_password(request.form['password'])
        db.session.commit()
        return redirect(url_for('tutor.index'))
    return render_template('pages/tutor/form.html', tutor=t)


@tutor_bp.route('/hapus/<int:id>')
@login_required
@role_required('admin')
def hapus(id):
    t = Tutor.query.get_or_404(id)
    db.session.delete(t.user)
    db.session.delete(t)
    db.session.commit()
    return redirect(url_for('tutor.index'))


@tutor_bp.route('/daftar', methods=['GET', 'POST'])
def daftar():
    if request.method == 'POST':
        user = User(
            username=request.form['username'],
            nama=request.form['nama'],
            role='tutor',
            email=request.form.get('email'),
            telepon=request.form.get('telepon'),
        )
        user.set_password(request.form['password'])
        db.session.add(user)
        db.session.flush()

        t = Tutor(
            user_id=user.id,
            bidang=request.form.get('bidang'),
            pengalaman=request.form.get('pengalaman'),
            pendidikan=request.form.get('pendidikan'),
            tarif_per_sesi=request.form.get('tarif_per_sesi', type=float),
            bank_nama=request.form.get('bank_nama'),
            bank_akun=request.form.get('bank_akun'),
        )
        db.session.add(t)
        db.session.commit()
        return redirect(url_for('auth.login'))
    return render_template('pages/tutor/daftar.html')


@tutor_bp.route('/profil', methods=['GET', 'POST'])
@login_required
def profil():
    t = Tutor.query.filter_by(user_id=current_user.id).first_or_404()
    if request.method == 'POST':
        t.user.nama = request.form['nama']
        t.user.email = request.form.get('email')
        t.user.telepon = request.form.get('telepon')
        t.bidang = request.form.get('bidang')
        t.pengalaman = request.form.get('pengalaman')
        t.pendidikan = request.form.get('pendidikan')
        t.bank_nama = request.form.get('bank_nama')
        t.bank_akun = request.form.get('bank_akun')
        if request.form.get('password'):
            t.user.set_password(request.form['password'])
        db.session.commit()
        return redirect(url_for('tutor.profil'))
    return render_template('pages/tutor/profil.html', tutor=t)
