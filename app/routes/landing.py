from flask import Blueprint, render_template

landing_bp = Blueprint('landing', __name__)


@landing_bp.route('/')
def index():
    return render_template('landing/index.html')


@landing_bp.route('/tentang')
def tentang():
    return render_template('landing/tentang.html')


@landing_bp.route('/program')
def program():
    return render_template('landing/program.html')


@landing_bp.route('/jenjang')
def jenjang():
    return render_template('landing/jenjang.html')


@landing_bp.route('/cara-daftar')
def cara_daftar():
    return render_template('landing/cara_daftar.html')


@landing_bp.route('/rekrutmen')
def rekrutmen():
    return render_template('landing/rekrutmen.html')


@landing_bp.route('/faq')
def faq():
    return render_template('landing/faq.html')


@landing_bp.route('/kontak')
def kontak():
    return render_template('landing/kontak.html')
