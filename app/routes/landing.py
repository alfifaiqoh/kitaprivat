from flask import Blueprint, render_template, abort

landing_bp = Blueprint('landing', __name__)

PROGRAMS = {
    'tk': {
        'name': 'TK',
        'emoji': '🎒',
        'price': 'Rp 50K',
        'marker': '✨',
        'desc': 'Bimbingan belajar untuk anak TK dengan metode bermain sambil belajar. Menumbuhkan rasa percaya diri dan kesiapan anak memasuki jenjang SD.',
        'features': ['Siap masuk SD.', 'Worksheet eksklusif.', 'Aktivitas interaktif.', 'Progress report.', 'Jadwal fleksibel.', 'Home visit.', 'Guru berpengalaman.', '60 menit efektif.'],
        'gallery': [
            {'emoji': '🧸', 'caption': 'Belajar sambil bermain'},
            {'emoji': '✏️', 'caption': 'Calistung dasar'},
            {'emoji': '🎨', 'caption': 'Kegiatan kreatif'},
            {'emoji': '📖', 'caption': 'Membaca & bercerita'},
            {'emoji': '🧩', 'caption': 'Aktivitas interaktif'},
            {'emoji': '🏠', 'caption': 'Suasana home visit'},
        ],
    },
    'sd': {
        'name': 'SD',
        'emoji': '📚',
        'price': 'Rp 65K',
        'marker': '⭐',
        'desc': 'Bimbingan belajar untuk siswa SD. Fokus penguatan semua mapel, latihan soal terarah, dan persiapan TKA dengan suasana belajar yang menyenangkan.',
        'features': ['Semua mapel.', 'Guru berpengalaman.', 'Rangkuman eksklusif.', 'Latihan soal terarah.', 'Siap TKA.', 'Home visit.', 'Jadwal fleksibel.', '90 menit efektif.'],
        'gallery': [
            {'emoji': '📐', 'caption': 'Matematika seru'},
            {'emoji': '🔬', 'caption': 'Eksperimen IPA'},
            {'emoji': '✏️', 'caption': 'Latihan menulis'},
            {'emoji': '📚', 'caption': 'Membaca bersama'},
            {'emoji': '🎨', 'caption': 'Kelas kreatif'},
            {'emoji': '🏠', 'caption': 'Suasana home visit'},
        ],
    },
    'smp': {
        'name': 'SMP',
        'emoji': '📖',
        'price': 'Rp 70K',
        'marker': '⭐',
        'desc': 'Bimbingan intensif semua mapel untuk siswa SMP. Soal latihan sesuai kisi-kisi, siap menghadapi ujian sekolah dan TKA.',
        'features': ['Semua mapel.', 'Guru berpengalaman.', 'Rangkuman eksklusif.', 'Soal sesuai kisi-kisi.', 'Siap ujian & TKA.', 'Home visit.', 'Jadwal fleksibel.', '90 menit efektif.'],
        'gallery': [
            {'emoji': '📐', 'caption': 'Matematika & aljabar'},
            {'emoji': '🔬', 'caption': 'IPA terpadu'},
            {'emoji': '🌍', 'caption': 'IPS & sejarah'},
            {'emoji': '✏️', 'caption': 'Latihan soal terarah'},
            {'emoji': '💻', 'caption': 'Belajar digital'},
            {'emoji': '🏠', 'caption': 'Suasana home visit'},
        ],
    },
    'sma': {
        'name': 'SMA',
        'emoji': '🎯',
        'price': 'Rp 80K',
        'marker': '⭐',
        'desc': 'Pendampingan semua mapel untuk siswa SMA/SMK. Materi mendalam sesuai kisi-kisi, siap menghadapi UTBK, TKA, dan ujian sekolah.',
        'features': ['Semua mapel.', 'Guru berpengalaman.', 'Rangkuman eksklusif.', 'Soal sesuai kisi-kisi.', 'Siap UTBK, TKA, & ujian.', 'Home visit.', 'Jadwal fleksibel.', '90 menit efektif.'],
        'gallery': [
            {'emoji': '🧮', 'caption': 'Matematika lanjut'},
            {'emoji': '⚛️', 'caption': 'Fisika & kimia'},
            {'emoji': '🧬', 'caption': 'Biologi'},
            {'emoji': '✍️', 'caption': 'Latihan UTBK'},
            {'emoji': '💻', 'caption': 'Belajar digital'},
            {'emoji': '🏠', 'caption': 'Suasana home visit'},
        ],
    },
}


@landing_bp.route('/')
def index():
    return render_template('landing/index.html')


@landing_bp.route('/tentang')
def tentang():
    return render_template('landing/tentang.html')


@landing_bp.route('/program')
def program():
    return render_template('landing/program.html')


@landing_bp.route('/program/<slug>')
def program_detail(slug):
    prog = PROGRAMS.get(slug)
    if prog is None:
        abort(404)
    return render_template('landing/program_detail.html', prog=prog, slug=slug)


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
