from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required
from app import db
from app.models.jenjang import Jenjang
from app.models.program import Program
from app.models.paket import Paket
from app.models.mapel import MataPelajaran
from app.models.wilayah import Wilayah
from app.utils.decorators import role_required

master_bp = Blueprint('master', __name__, url_prefix='/admin/master')


@master_bp.route('/')
@login_required
@role_required('admin')
def index():
    return render_template('master/index.html')


@master_bp.route('/jenjang')
@login_required
@role_required('admin')
def jenjang_index():
    data = Jenjang.query.all()
    return render_template('master/jenjang.html', data=data)


@master_bp.route('/jenjang/tambah', methods=['POST'])
@login_required
@role_required('admin')
def jenjang_tambah():
    j = Jenjang(nama=request.form['nama'])
    db.session.add(j)
    db.session.commit()
    return redirect(url_for('master.jenjang_index'))


@master_bp.route('/jenjang/hapus/<int:id>')
@login_required
@role_required('admin')
def jenjang_hapus(id):
    Jenjang.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect(url_for('master.jenjang_index'))


@master_bp.route('/program')
@login_required
@role_required('admin')
def program_index():
    data = Program.query.all()
    jenjang_list = Jenjang.query.all()
    return render_template('master/program.html', data=data, jenjang_list=jenjang_list)


@master_bp.route('/program/tambah', methods=['POST'])
@login_required
@role_required('admin')
def program_tambah():
    p = Program(nama=request.form['nama'], deskripsi=request.form.get('deskripsi'), jenjang_id=request.form.get('jenjang_id', type=int))
    db.session.add(p)
    db.session.commit()
    return redirect(url_for('master.program_index'))


@master_bp.route('/program/hapus/<int:id>')
@login_required
@role_required('admin')
def program_hapus(id):
    Program.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect(url_for('master.program_index'))


@master_bp.route('/paket')
@login_required
@role_required('admin')
def paket_index():
    data = Paket.query.all()
    program_list = Program.query.all()
    return render_template('master/paket.html', data=data, program_list=program_list)


@master_bp.route('/paket/tambah', methods=['POST'])
@login_required
@role_required('admin')
def paket_tambah():
    p = Paket(
        program_id=request.form['program_id'],
        nama=request.form['nama'],
        jumlah_pertemuan=request.form.get('jumlah_pertemuan', type=int),
        harga=request.form.get('harga', type=float),
        durasi_per_sesi=request.form.get('durasi_per_sesi', type=int, default=60),
    )
    db.session.add(p)
    db.session.commit()
    return redirect(url_for('master.paket_index'))


@master_bp.route('/paket/hapus/<int:id>')
@login_required
@role_required('admin')
def paket_hapus(id):
    Paket.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect(url_for('master.paket_index'))


@master_bp.route('/mapel')
@login_required
@role_required('admin')
def mapel_index():
    data = MataPelajaran.query.all()
    return render_template('master/mapel.html', data=data)


@master_bp.route('/mapel/tambah', methods=['POST'])
@login_required
@role_required('admin')
def mapel_tambah():
    m = MataPelajaran(nama=request.form['nama'], kategori=request.form.get('kategori'))
    db.session.add(m)
    db.session.commit()
    return redirect(url_for('master.mapel_index'))


@master_bp.route('/mapel/hapus/<int:id>')
@login_required
@role_required('admin')
def mapel_hapus(id):
    MataPelajaran.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect(url_for('master.mapel_index'))


@master_bp.route('/wilayah')
@login_required
@role_required('admin')
def wilayah_index():
    data = Wilayah.query.all()
    return render_template('master/wilayah.html', data=data)


@master_bp.route('/wilayah/tambah', methods=['POST'])
@login_required
@role_required('admin')
def wilayah_tambah():
    w = Wilayah(nama=request.form['nama'])
    db.session.add(w)
    db.session.commit()
    return redirect(url_for('master.wilayah_index'))


@master_bp.route('/wilayah/hapus/<int:id>')
@login_required
@role_required('admin')
def wilayah_hapus(id):
    Wilayah.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect(url_for('master.wilayah_index'))
