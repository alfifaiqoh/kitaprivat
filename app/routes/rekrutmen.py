import os
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app import db
from app.models.rekrutmen import RekrutmenTutor
from app.models.tutor import Tutor
from app.models.user import User
from app.utils.decorators import role_required
from app.utils.helpers import wa_chat_url

rekrutmen_bp = Blueprint('rekrutmen', __name__, url_prefix='/rekrutmen')

ALLOWED_EXT = {'pdf', 'png', 'jpg', 'jpeg', 'doc', 'docx'}
FIELD_FILE_MAP = {
    'ktp': 'ktp',
    'cv': 'cv',
    'ijazah': 'ijazah',
    'transkrip': 'transkrip',
    'sertifikat': 'sertifikat',
}


def simpan_berkas(file, jenis, nama):
    if not file or not file.filename:
        return None
    ext = file.filename.rsplit('.', 1)[-1].lower()
    if ext not in ALLOWED_EXT:
        return None
    nama_file = f"{jenis}_{nama}.{ext}"
    folder = os.path.join(current_app.root_path, '..', 'uploads', 'rekrutmen')
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, nama_file)
    file.save(path)
    return nama_file


@rekrutmen_bp.route('/', methods=['GET', 'POST'])
def daftar():
    if request.method == 'POST':
        nama = request.form['nama'].strip()
        slug = nama.lower().replace(' ', '_')

        r = RekrutmenTutor(
            nama=nama,
            email=request.form['email'],
            telepon=request.form.get('telepon'),
            alamat=request.form.get('alamat'),
            bidang=request.form.get('bidang'),
            pendidikan=request.form.get('pendidikan'),
            pengalaman=request.form.get('pengalaman'),
            ktp=simpan_berkas(request.files.get('ktp'), 'ktp', slug),
            cv=simpan_berkas(request.files.get('cv'), 'cv', slug),
            ijazah=simpan_berkas(request.files.get('ijazah'), 'ijazah', slug),
            transkrip=simpan_berkas(request.files.get('transkrip'), 'transkrip', slug),
            sertifikat=simpan_berkas(request.files.get('sertifikat'), 'sertifikat', slug),
        )
        db.session.add(r)
        db.session.commit()

        pesan = f"""Halo Admin KITA PRIVAT, saya baru mendaftar sebagai tentor:

Nama: {r.nama}
Email: {r.email}
Telepon: {r.telepon or '-'}
Alamat: {r.alamat or '-'}
Bidang: {r.bidang or '-'}
Pendidikan: {r.pendidikan or '-'}
Pengalaman: {r.pengalaman or '-'}

Mohon info langkah selanjutnya. Terima kasih."""
        return redirect(wa_chat_url(pesan))

    return render_template('pages/rekrutmen/daftar.html')


@rekrutmen_bp.route('/sukses')
def sukses():
    return render_template('pages/rekrutmen/sukses.html')


@rekrutmen_bp.route('/list')
@login_required
@role_required('admin')
def index():
    tab = request.args.get('tab', 'menunggu')
    if tab == 'tutor_aktif':
        data = Tutor.query.all()
        return render_template('pages/rekrutmen/index.html', tab=tab, tutor_list=data)
    if tab == 'all':
        data = RekrutmenTutor.query.order_by(RekrutmenTutor.created_at.desc()).all()
    else:
        data = RekrutmenTutor.query.filter_by(status=tab).order_by(RekrutmenTutor.created_at.desc()).all()
    return render_template('pages/rekrutmen/index.html', tab=tab, rekrutmen_list=data)


@rekrutmen_bp.route('/review/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def review(id):
    r = RekrutmenTutor.query.get_or_404(id)
    if request.method == 'POST':
        r.status = request.form['status']
        r.catatan_admin = request.form.get('catatan_admin')
        tgl = request.form.get('tanggal_interview')
        if tgl:
            r.tanggal_interview = datetime.strptime(tgl, '%Y-%m-%dT%H:%M')
        db.session.commit()
        return redirect(url_for('rekrutmen.index'))
    return render_template('pages/rekrutmen/review.html', r=r)


@rekrutmen_bp.route('/terima/<int:id>')
@login_required
@role_required('admin')
def terima(id):
    r = RekrutmenTutor.query.get_or_404(id)
    if r.status != 'diterima':
        r.status = 'diterima'
        db.session.commit()

    if not User.query.filter_by(username=r.email).first():
        user = User(
            username=r.email.split('@')[0],
            nama=r.nama,
            role='tutor',
            email=r.email,
            telepon=r.telepon,
        )
        user.set_password('tutor123')
        db.session.add(user)
        db.session.flush()

        t = Tutor(
            user_id=user.id,
            bidang=r.bidang,
            pengalaman=r.pengalaman,
            pendidikan=r.pendidikan,
        )
        db.session.add(t)
        db.session.commit()

    return redirect(url_for('rekrutmen.index'))
