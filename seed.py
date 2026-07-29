import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app, db
from app.models.user import User
from app.models.tutor import Tutor
from app.models.siswa import Siswa
from app.models.penugasan import Penugasan
from app.models.jadwal import Jadwal
from app.models.absensi import Absensi
from app.models.pembayaran import Pembayaran
from app.models.honor import HonorTutor
from app.models.pencairan import PengajuanPencairan
from app.models.penilaian import PenilaianPerforma
from app.models.laporan import Laporan
from app.models.pengumuman import Pengumuman
from app.models.jenjang import Jenjang
from app.models.program import Program
from app.models.paket import Paket
from app.models.mapel import MataPelajaran
from app.models.wilayah import Wilayah
from datetime import date, datetime, timedelta
import random

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    # ── Admin ──
    admin = User(username='admin', nama='Administrator', role='admin')
    admin.set_password('admin123')
    db.session.add(admin)

    # ── Jenjang ──
    jenjang_data = ['SD', 'SMP', 'SMA', 'Mahasiswa', 'Umum']
    jenjang_objs = {}
    for j in jenjang_data:
        obj = Jenjang(nama=j)
        db.session.add(obj)
        jenjang_objs[j] = obj
    db.session.flush()

    # ── Program ──
    programs = [
        ('Reguler SD', 'SD'), ('Privat SD', 'SD'),
        ('Reguler SMP', 'SMP'), ('Privat SMP', 'SMP'),
        ('Reguler SMA', 'SMA'), ('Privat SMA', 'SMA'),
        ('Bahasa Asing', 'Umum'), ('Olimpiade', 'SMA'),
    ]
    program_objs = {}
    for nama, jnama in programs:
        obj = Program(nama=nama, deskripsi=f'Program {nama}', jenjang_id=jenjang_objs[jnama].id)
        db.session.add(obj)
        program_objs[nama] = obj
    db.session.flush()

    # ── Paket ──
    pakets = [
        ('Reguler SD', '6x Pertemuan', 6, 600000),
        ('Reguler SD', '12x Pertemuan', 12, 1000000),
        ('Privat SD', '8x Pertemuan', 8, 1200000),
        ('Reguler SMP', '6x Pertemuan', 6, 750000),
        ('Reguler SMP', '12x Pertemuan', 12, 1300000),
        ('Privat SMP', '8x Pertemuan', 8, 1500000),
        ('Reguler SMA', '6x Pertemuan', 6, 900000),
        ('Reguler SMA', '12x Pertemuan', 12, 1600000),
        ('Privat SMA', '8x Pertemuan', 8, 1800000),
    ]
    for pnama, paket_nama, jml, harga in pakets:
        obj = Paket(program_id=program_objs[pnama].id, nama=paket_nama, jumlah_pertemuan=jml, harga=harga)
        db.session.add(obj)
    db.session.flush()

    # ── Mata Pelajaran ──
    mapels = [
        ('Matematika', 'Akademik'),
        ('IPA', 'Akademik'),
        ('Bahasa Inggris', 'Bahasa'),
        ('Bahasa Indonesia', 'Bahasa'),
        ('Fisika', 'Akademik'),
        ('Kimia', 'Akademik'),
        ('Biologi', 'Akademik'),
        ('Ekonomi', 'Akademik'),
        ('Sejarah', 'Akademik'),
        ('Geografi', 'Akademik'),
        ('Bahasa Jepang', 'Bahasa'),
        ('Bahasa Arab', 'Bahasa'),
        ('Komputer', 'Keterampilan'),
        ('Mengaji', 'Agama'),
    ]
    for nama, kategori in mapels:
        db.session.add(MataPelajaran(nama=nama, kategori=kategori))
    db.session.flush()

    # ── Wilayah ──
    wil = ['Jakarta Pusat', 'Jakarta Selatan', 'Jakarta Barat', 'Jakarta Timur', 'Jakarta Utara', 'Bogor', 'Depok', 'Tangerang', 'Bekasi']
    for w in wil:
        db.session.add(Wilayah(nama=w))
    db.session.flush()

    # ── Tutor ──
    tutor_data = [
        ('tutor1', 'Ahmad Fauzi', 'Matematika', 'S1 Pendidikan Matematika - UNJ', 50000, 'BCA', '1234567890'),
        ('tutor2', 'Siti Nurhaliza', 'IPA', 'S1 Pendidikan IPA - UPI', 60000, 'Mandiri', '9876543210'),
        ('tutor3', 'Budi Santoso', 'Bahasa Inggris', 'S1 Sastra Inggris - UI', 55000, 'BNI', '5556667770'),
        ('tutor4', 'Dewi Lestari', 'Fisika', 'S1 Fisika - ITB', 65000, 'BRI', '1112223330'),
        ('tutor5', 'Rudi Hermawan', 'Matematika & IPA', 'S1 Matematika - UGM', 55000, 'BCA', '4445556660'),
    ]
    tutor_objs = []
    for uname, nama, bidang, pendidikan, tarif, bank, norek in tutor_data:
        u = User(username=uname, nama=nama, role='tutor', email=f'{uname}@kitaprivat.id', telepon=f'0812{random.randint(1000000,9999999)}')
        u.set_password('tutor123')
        db.session.add(u)
        db.session.flush()
        t = Tutor(user_id=u.id, bidang=bidang, pendidikan=pendidikan, tarif_per_sesi=tarif, bank_nama=bank, bank_akun=norek, status='aktif', rating=round(random.uniform(3.5,5.0),1))
        db.session.add(t)
        tutor_objs.append(t)
    db.session.flush()

    # ── Orang Tua ──
    ortu = User(username='ortu1', nama='Bambang Supomo', role='orang_tua', email='bambang@email.com', telepon='081311112222')
    ortu.set_password('ortu123')
    db.session.add(ortu)
    db.session.flush()

    # ── Siswa ──
    siswa_data = [
        ('Andi Pratama', 'SMA', 'SMA Negeri 1 Jakarta', 'L', '2007-05-12', 'Matematika, Fisika'),
        ('Rina Wijaya', 'SMA', 'SMA Negeri 2 Jakarta', 'P', '2008-08-22', 'Bahasa Inggris, Biologi'),
        ('Doni Saputra', 'SMP', 'SMP Negeri 5 Jakarta', 'L', '2010-02-14', 'Matematika, IPA'),
        ('Sari Indah', 'SMP', 'SMP Harapan Bangsa', 'P', '2011-11-30', 'Matematika, Bahasa Inggris'),
        ('Bagas Putra', 'SD', 'SD Negeri 3 Jakarta', 'L', '2013-07-08', 'Matematika, IPA'),
        ('Maya Anggraini', 'SD', 'SD Cendekia', 'P', '2014-04-18', 'Bahasa Inggris, Membaca'),
        ('Fajar Hidayat', 'SMA', 'SMA Negeri 5 Jakarta', 'L', '2007-12-01', 'Fisika, Matematika'),
        ('Nina Amelia', 'SMP', 'SMP Negeri 8 Jakarta', 'P', '2011-06-15', 'Bahasa Inggris, IPA'),
    ]
    siswa_objs = []
    for i, (nama, kelas, sekolah, jk, tgl, mapel_str) in enumerate(siswa_data):
        tgl_lahir = date(*[int(x) for x in tgl.split('-')])
        is_baru = i >= 6  # last 2 are new registrations
        s = Siswa(
            orang_tua_id=None if is_baru else ortu.id,
            nama=nama, kelas=kelas, sekolah=sekolah,
            jenis_kelamin=jk, tanggal_lahir=tgl_lahir,
            alamat=f'Jl. Contoh No.{random.randint(1,100)}, Jakarta',
            telepon=f'0812{random.randint(1000000,9999999)}',
            email=f'{nama.lower().replace(" ","")}@email.com',
            mata_pelajaran=mapel_str,
            status='baru' if is_baru else 'aktif',
            aktif=True
        )
        db.session.add(s)
        siswa_objs.append(s)
    db.session.flush()

    # ── Penugasan (active assignments) ──
    penugasan_data = [
        (siswa_objs[0], tutor_objs[0], 'Matematika', 50000),
        (siswa_objs[0], tutor_objs[3], 'Fisika', 65000),
        (siswa_objs[1], tutor_objs[2], 'Bahasa Inggris', 55000),
        (siswa_objs[2], tutor_objs[4], 'Matematika', 55000),
        (siswa_objs[3], tutor_objs[2], 'Bahasa Inggris', 55000),
        (siswa_objs[4], tutor_objs[4], 'Matematika', 55000),
        (siswa_objs[5], tutor_objs[1], 'IPA', 60000),
    ]
    penugasan_objs = []
    for siswa, tutor, mapel, tarif in penugasan_data:
        p = Penugasan(
            siswa_id=siswa.id, tutor_id=tutor.id,
            mata_pelajaran=mapel, tarif=tarif,
            status='aktif', assigned_by=admin.id
        )
        db.session.add(p)
        penugasan_objs.append(p)
    db.session.flush()

    # ── Jadwal ──
    hari_list = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu']
    jadwal_data = [
        (penugasan_objs[0], 'Senin', '14:00', '16:00'),
        (penugasan_objs[0], 'Rabu', '14:00', '16:00'),
        (penugasan_objs[1], 'Selasa', '15:00', '17:00'),
        (penugasan_objs[2], 'Senin', '13:00', '15:00'),
        (penugasan_objs[2], 'Kamis', '13:00', '15:00'),
        (penugasan_objs[3], 'Selasa', '14:00', '16:00'),
        (penugasan_objs[3], 'Jumat', '14:00', '16:00'),
        (penugasan_objs[4], 'Rabu', '15:00', '17:00'),
        (penugasan_objs[5], 'Sabtu', '09:00', '11:00'),
        (penugasan_objs[6], 'Sabtu', '10:00', '12:00'),
    ]
    for penugasan, hari, mulai, selesai in jadwal_data:
        db.session.add(Jadwal(penugasan_id=penugasan.id, hari=hari, jam_mulai=mulai, jam_selesai=selesai))
    db.session.flush()

    # ── Absensi ──
    today = date.today()
    for i in range(30):
        d = today - timedelta(days=i)
        if d.weekday() < 6:
            for p in penugasan_objs:
                if random.random() < 0.15:
                    status = random.choices(['hadir', 'hadir', 'hadir', 'izin', 'sakit'], weights=[60,20,10,5,5])[0]
                    jam_m = f'{random.randint(13,15):02d}:{random.randint(0,59):02d}'
                    jam_k = f'{random.randint(15,17):02d}:{random.randint(0,59):02d}'
                    db.session.add(Absensi(
                        penugasan_id=p.id, tutor_id=p.tutor_id,
                        tanggal=d, jam_masuk=jam_m, jam_keluar=jam_k,
                        status=status, keterangan='' if status == 'hadir' else f'{status.title()}'
                    ))
    db.session.flush()

    # ── Pembayaran ──
    bulan_list = ['2026-01', '2026-02', '2026-03', '2026-04', '2026-05', '2026-06', '2026-07']
    for p in penugasan_objs:
        for bln in bulan_list[:random.randint(3,6)]:
            status = random.choices(['lunas', 'lunas', 'lunas', 'belum_dibayar'], weights=[60,20,10,10])[0]
            tgl_bayar = today - timedelta(days=random.randint(1,60)) if status == 'lunas' else None
            db.session.add(Pembayaran(
                penugasan_id=p.id, jumlah=p.tarif * 4,
                bulan=bln, status=status,
                metode='Transfer' if status == 'lunas' else None,
                tanggal_bayar=tgl_bayar
            ))
    db.session.flush()

    # ── Honor ──
    for t in tutor_objs:
        for bln in ['2026-05', '2026-06', '2026-07']:
            sesi = random.randint(4,12)
            honor = HonorTutor(
                tutor_id=t.id, bulan=bln,
                total_sesi=sesi, tarif_per_sesi=t.tarif_per_sesi,
                total_honor=sesi * t.tarif_per_sesi * 0.75,
                status=random.choices(['belum_diajukan', 'diajukan', 'dicairkan'], weights=[30,30,40])[0]
            )
            db.session.add(honor)
    db.session.flush()

    # ── Pencairan ──
    for t in tutor_objs[:3]:
        nominal = random.randint(300000, 1500000)
        db.session.add(PengajuanPencairan(
            tutor_id=t.id, jumlah=nominal,
            status=random.choices(['diajukan', 'disetujui', 'dicairkan'], weights=[40,30,30])[0],
            tanggal_diajukan=today - timedelta(days=random.randint(5,30)),
            tanggal_disetujui=today - timedelta(days=random.randint(1,20)),
        ))
    db.session.flush()

    # ── Penilaian ──
    for t in tutor_objs:
        for _ in range(random.randint(1,3)):
            disiplin = random.randint(3,5)
            materi = random.randint(3,5)
            komunikasi = random.randint(3,5)
            hadir = random.randint(3,5)
            total = (disiplin + materi + komunikasi + hadir) / 4
            db.session.add(PenilaianPerforma(
                tutor_id=t.id, penilai_id=admin.id,
                tanggal=today - timedelta(days=random.randint(5,60)),
                kedisiplinan=disiplin, penguasaan_materi=materi,
                komunikasi=komunikasi, kehadiran=hadir,
                total_skor=total, catatan='Pertahankan!'
            ))
    db.session.flush()

    # ── Laporan ──
    for p in penugasan_objs:
        for _ in range(random.randint(2,6)):
            d = today - timedelta(days=random.randint(1,45))
            db.session.add(Laporan(
                penugasan_id=p.id, tutor_id=p.tutor_id,
                tanggal=d, materi=f'Materi pertemuan ke-{random.randint(1,12)}',
                catatan='Siswa aktif bertanya', pr='Kerjakan soal latihan',
                hadir=True
            ))
    db.session.flush()

    # ── Pengumuman ──
    pengumuman = [
        ('Libur Nasional', 'Sehubungan dengan libur nasional, seluruh kegiatan les diliburkan.', 'semua'),
        ('Rapat Tutor Bulanan', 'Rapat tutor akan diadakan pada hari Sabtu, 10 Agustus 2026.', 'tutor'),
        ('Informasi Pembayaran', 'Pembayaran bulan Juli sudah dapat dilakukan melalui transfer.', 'semua'),
    ]
    for judul, isi, target in pengumuman:
        db.session.add(Pengumuman(judul=judul, isi=isi, target=target, aktif=True, dibuat_oleh=admin.id))
    db.session.flush()

    db.session.commit()
    print('=== SEED BERHASIL ===')
    print(f'Admin: admin / admin123')
    print(f'Tutor: tutor1-5 / tutor123')
    print(f'Orang Tua: ortu1 / ortu123')
    print(f'Siswa: {len(siswa_objs)} siswa')
    print(f'Penugasan: {len(penugasan_objs)}')
