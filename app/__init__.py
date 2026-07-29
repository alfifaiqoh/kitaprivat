from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Silakan login terlebih dahulu'


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    uri = app.config.get('SQLALCHEMY_DATABASE_URI', '')
    if uri.startswith('sqlite'):
        import os
        dirpath = uri.replace('sqlite:///', '').rsplit('/', 1)[0]
        os.makedirs(dirpath, exist_ok=True)

    db.init_app(app)
    login_manager.init_app(app)

    from app.utils.context_processors import inject_globals
    app.context_processor(inject_globals)

    from app.routes.auth import auth_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.siswa import siswa_bp
    from app.routes.tutor import tutor_bp
    from app.routes.penugasan import penugasan_bp
    from app.routes.jadwal import jadwal_bp
    from app.routes.pembayaran import pembayaran_bp
    from app.routes.laporan import laporan_bp
    from app.routes.absensi import absensi_bp
    from app.routes.honor import honor_bp
    from app.routes.pencairan import pencairan_bp
    from app.routes.penilaian import penilaian_bp
    from app.routes.rekrutmen import rekrutmen_bp
    from app.routes.landing import landing_bp
    from app.routes.parent import parent_bp
    from app.routes.master import master_bp
    from app.routes.keuangan import keuangan_bp
    from app.routes.pengumuman import pengumuman_bp

    app.register_blueprint(landing_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(siswa_bp)
    app.register_blueprint(tutor_bp)
    app.register_blueprint(penugasan_bp)
    app.register_blueprint(jadwal_bp)
    app.register_blueprint(pembayaran_bp)
    app.register_blueprint(laporan_bp)
    app.register_blueprint(absensi_bp)
    app.register_blueprint(honor_bp)
    app.register_blueprint(pencairan_bp)
    app.register_blueprint(penilaian_bp)
    app.register_blueprint(rekrutmen_bp)
    app.register_blueprint(parent_bp)
    app.register_blueprint(master_bp)
    app.register_blueprint(keuangan_bp)
    app.register_blueprint(pengumuman_bp)

    with app.app_context():
        from app.models import user, siswa, tutor, penugasan, jadwal
        from app.models import pembayaran, laporan, absensi, honor, pencairan, penilaian
        from app.models import rekrutmen, jenjang, program, paket, mapel, wilayah
        from app.models import invoice, dompet, request_les, pengumuman
        db.create_all()
        user.seed_admin()

    return app
