from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from app import db
from app.models.pengumuman import Pengumuman
from app.utils.decorators import role_required

pengumuman_bp = Blueprint('pengumuman', __name__, url_prefix='/pengumuman')


@pengumuman_bp.route('/')
def index():
    data = Pengumuman.query.filter_by(aktif=True).order_by(Pengumuman.created_at.desc()).all()
    return render_template('pengumuman/index.html', data=data)


@pengumuman_bp.route('/tambah', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def tambah():
    if request.method == 'POST':
        p = Pengumuman(
            judul=request.form['judul'],
            isi=request.form['isi'],
            target=request.form.get('target', 'semua'),
            dibuat_oleh=current_user.id,
        )
        db.session.add(p)
        db.session.commit()
        return redirect(url_for('pengumuman.index'))
    return render_template('pengumuman/form.html')


@pengumuman_bp.route('/admin')
@login_required
@role_required('admin')
def admin_index():
    data = Pengumuman.query.order_by(Pengumuman.created_at.desc()).all()
    return render_template('pengumuman/admin.html', data=data)
