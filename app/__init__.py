from flask import Flask, render_template
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

    with app.app_context():
        from app.models import user, siswa, tutor, penugasan, jadwal
        from app.models import pembayaran, laporan, absensi, honor, pencairan, penilaian
        from app.models import rekrutmen
        db.create_all()
        user.seed_admin()

    @app.route('/')
    def landing():
        return render_template('landing.html')

    return app
