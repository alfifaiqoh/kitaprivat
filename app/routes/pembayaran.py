from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required
from app import db
from app.models.pembayaran import Pembayaran
from app.models.penugasan import Penugasan

pembayaran_bp = Blueprint('pembayaran', __name__, url_prefix='/pembayaran')


@pembayaran_bp.route('/')
@login_required
def index():
    data = Pembayaran.query.all()
    return render_template('pages/pembayaran/index.html', pembayaran_list=data)


@pembayaran_bp.route('/tambah', methods=['GET', 'POST'])
@login_required
def tambah():
    if request.method == 'POST':
        tgl = request.form.get('tanggal_bayar')
        p = Pembayaran(
            penugasan_id=request.form['penugasan_id'],
            jumlah=request.form['jumlah'],
            bulan=request.form['bulan'],
            status=request.form.get('status', 'belum_dibayar'),
            metode=request.form.get('metode'),
            tanggal_bayar=datetime.strptime(tgl, '%Y-%m-%d') if tgl else None,
            keterangan=request.form.get('keterangan'),
        )
        db.session.add(p)
        db.session.commit()
        return redirect(url_for('pembayaran.index'))
    penugasan_list = Penugasan.query.filter_by(status='aktif').all()
    return render_template('pages/pembayaran/form.html', pembayaran=None, penugasan_list=penugasan_list)


@pembayaran_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    p = Pembayaran.query.get_or_404(id)
    if request.method == 'POST':
        tgl = request.form.get('tanggal_bayar')
        p.penugasan_id = request.form['penugasan_id']
        p.jumlah = request.form['jumlah']
        p.bulan = request.form['bulan']
        p.status = request.form.get('status', 'belum_dibayar')
        p.metode = request.form.get('metode')
        p.tanggal_bayar = datetime.strptime(tgl, '%Y-%m-%d') if tgl else None
        p.keterangan = request.form.get('keterangan')
        db.session.commit()
        return redirect(url_for('pembayaran.index'))
    penugasan_list = Penugasan.query.filter_by(status='aktif').all()
    return render_template('pages/pembayaran/form.html', pembayaran=p, penugasan_list=penugasan_list)


@pembayaran_bp.route('/hapus/<int:id>')
@login_required
def hapus(id):
    p = Pembayaran.query.get_or_404(id)
    db.session.delete(p)
    db.session.commit()
    return redirect(url_for('pembayaran.index'))
