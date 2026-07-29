from flask import request
from datetime import datetime
from flask_login import current_user
from app.models.pengumuman import Pengumuman


def inject_globals():
    return {
        'current_path': request.path,
        'now': datetime.now,
        'role': getattr(current_user, 'role', None) if not current_user.is_anonymous else None,
        'get_pengumuman': lambda: Pengumuman.query.filter_by(aktif=True).order_by(Pengumuman.created_at.desc()).all(),
    }
