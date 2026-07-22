from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app import db
from app.models.penugasan import Penugasan
from app.models.siswa import Siswa
from app.models.tutor import Tutor
from app.models.pembayaran import Pembayaran

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@dashboard_bp.route('/')
@login_required
def index():
    role = current_user.role
    context = {'role': role}

    if role == 'admin':
        context['total_siswa'] = Siswa.query.count()
        context['total_tutor'] = Tutor.query.count()
        context['total_penugasan'] = Penugasan.query.count()
        total = db.session.query(db.func.sum(Pembayaran.jumlah)).filter_by(status='lunas').scalar()
        context['total_pendapatan'] = total or 0

    elif role == 'tutor':
        tutor = Tutor.query.filter_by(user_id=current_user.id).first()
        if tutor:
            context['penugasan_list'] = Penugasan.query.filter_by(tutor_id=tutor.id).all()

    elif role == 'orang_tua':
        context['siswa_list'] = Siswa.query.filter_by(orang_tua_id=current_user.id).all()

    return render_template('dashboard/index.html', **context)
