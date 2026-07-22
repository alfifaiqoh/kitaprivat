from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required
from app import db
from app.models.jadwal import Jadwal
from app.models.penugasan import Penugasan

jadwal_bp = Blueprint('jadwal', __name__, url_prefix='/jadwal')


@jadwal_bp.route('/')
@login_required
def index():
    data = Jadwal.query.all()
    return render_template('pages/jadwal/index.html', jadwal_list=data)


@jadwal_bp.route('/tambah', methods=['GET', 'POST'])
@login_required
def tambah():
    if request.method == 'POST':
        j = Jadwal(
            penugasan_id=request.form['penugasan_id'],
            hari=request.form['hari'],
            jam_mulai=request.form['jam_mulai'],
            jam_selesai=request.form['jam_selesai'],
        )
        db.session.add(j)
        db.session.commit()
        return redirect(url_for('jadwal.index'))
    penugasan_list = Penugasan.query.filter_by(status='aktif').all()
    return render_template('pages/jadwal/form.html', jadwal=None, penugasan_list=penugasan_list)


@jadwal_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    j = Jadwal.query.get_or_404(id)
    if request.method == 'POST':
        j.penugasan_id = request.form['penugasan_id']
        j.hari = request.form['hari']
        j.jam_mulai = request.form['jam_mulai']
        j.jam_selesai = request.form['jam_selesai']
        db.session.commit()
        return redirect(url_for('jadwal.index'))
    penugasan_list = Penugasan.query.filter_by(status='aktif').all()
    return render_template('pages/jadwal/form.html', jadwal=j, penugasan_list=penugasan_list)


@jadwal_bp.route('/hapus/<int:id>')
@login_required
def hapus(id):
    j = Jadwal.query.get_or_404(id)
    db.session.delete(j)
    db.session.commit()
    return redirect(url_for('jadwal.index'))
