Kalau melihat kebutuhan yang sudah kita diskusikan, saya akan membuat sistem yang benar-benar mengikuti operasional lembaga les privat, bukan marketplace seperti Ruangguru atau Superprof.

Konsep Sistem

Nama Sistem (contoh): KITA PRIVAT

Role User

Admin
Orang Tua
Tutor

Pada versi pertama, murid tidak memiliki akun. Orang tua yang mendaftarkan dan mengelola seluruh administrasi.

1. Website Landing Page

Menu:

Home
Tentang Kami
Program Les
Jenjang Pendidikan
Cara Pendaftaran
Rekrutmen Tutor
FAQ
Kontak

Tombol utama:

Daftar Les
Daftar Menjadi Tutor
2. Portal Orang Tua
Dashboard
Dashboard

Anak Saya
Jadwal Hari Ini
Tagihan
Pengumuman
Progress Belajar
Data Anak
Tambah Anak

Nama

Sekolah

Kelas

Jenis Kelamin

Tanggal Lahir

Alamat

Mata Pelajaran

Jadwal yang Diinginkan

Catatan

Satu akun orang tua bisa memiliki banyak anak.

Pendaftaran Les

Flow:

Orang Tua

↓

Isi Data Anak

↓

Pilih Program

↓

Pilih Paket

↓

Submit

↓

Menunggu Admin

Admin yang menentukan tutor.

Pembayaran

Jenis pembayaran:

Biaya Pendaftaran
Biaya Paket
Tagihan Bulanan
Biaya Tambahan

Status:

Belum Bayar

Menunggu Verifikasi

Lunas

Expired

Invoice:

INV-0001

Biaya Pendaftaran

Rp100.000
Jadwal Les
Senin

16.00

Matematika

Tutor:
Pak Budi
Progress Belajar
Mata Pelajaran

Pertemuan

Nilai

Catatan Tutor

Progress
Riwayat Pembayaran
Invoice

Tanggal

Nominal

Status
3. Portal Tutor

Dashboard

Hari Ini

Jadwal

Honor

Penugasan Baru
Penugasan
Nama Murid

Kelas

Alamat

Mapel

Hari

Jam

[Terima]
[Tolak]
Jadwal Mengajar

Kalender

08.00

09.30

Matematika

Rumah Murid
Absensi

Masuk

GPS
Selfie (opsional)
Jam otomatis

Keluar

GPS
Jam otomatis

Status

Hadir

Terlambat

Tidak Hadir
Laporan Mengajar
Materi

Kehadiran

PR

Catatan

Upload Foto (Opsional)
Honor Tutor
Total Honor

Honor Bulan Ini

Menunggu Pencairan

Sudah Dibayar
Withdrawal
Saldo

↓

Ajukan

↓

Admin Transfer

↓

Selesai
4. Portal Admin
Dashboard
Total Murid

Total Tutor

Les Hari Ini

Pendapatan

Tagihan

Grafik
Master Data
Tutor

Orang Tua

Murid

Jenjang

Program

Paket

Mata Pelajaran

Wilayah
Rekrutmen Tutor

Flow

Calon Tutor

↓

Isi Form

↓

Upload Dokumen

↓

Review

↓

Interview

↓

Lulus

↓

Aktif

Menu

Lamaran Baru

Interview

Lulus

Ditolak

Tutor Aktif
Request Les

Flow

Orang Tua Daftar

↓

Request Baru

↓

Admin Review

↓

Cari Tutor

↓

Assign Tutor

↓

Tutor Terima

↓

Invoice

↓

Pembayaran

↓

Jadwal Aktif
Penjadwalan

Kalender

Tutor

Hari

Jam

Lokasi

Admin dapat mengubah jadwal jika diperlukan.

Pembayaran
Invoice

Biaya Pendaftaran

Biaya Paket

Tagihan Bulanan

Status

Draft

Pending

Paid

Expired

Cancel
Keuangan
Pendapatan

Honor Tutor

Withdrawal

Komisi

Kas
Absensi Tutor
Masuk

Pulang

Lokasi

Jam

Status
Pengumuman
Semua Tutor

Semua Orang Tua

Per Tutor

Per Murid
Laporan
Pendapatan

Tutor Terbaik

Jumlah Les

Mapel Terlaris

Pembayaran

Absensi Tutor
Database
Users
id
role
name
email
password
phone
status
Parents
id
user_id
address
Students
id
parent_id
name
school
grade
birth_date
gender
notes
Tutors
id
user_id
education
experience
status
rating
bank_name
account_number
Subjects
id
name
category
Programs
id
name
description
Packages
id
program_id
name
meeting
price
duration
Requests
id
student_id
subject_id
schedule
status
Assignments
id
request_id
tutor_id
status
assigned_by
assigned_at
Schedules
id
assignment_id
date
start_time
end_time
location
status
Attendance
id
schedule_id
check_in
check_out
latitude
longitude
photo
status
Reports
id
schedule_id
material
homework
notes
Invoices
id
student_id
type
amount
status
Payments
id
invoice_id
method
transaction_id
status
paid_at
Wallet
id
tutor_id
balance
Withdrawals
id
tutor_id
amount
status
Status Sistem
Request
Baru
Diproses
Menunggu Tutor
Tutor Ditugaskan
Menunggu Pembayaran
Aktif
Selesai
Dibatalkan
Tutor
Calon Tutor
Verifikasi
Interview
Aktif
Cuti
Nonaktif
Resign
Invoice
Draft
Pending
Paid
Expired
Cancelled
Jadwal
Terjadwal
Berlangsung
Selesai
Dibatalkan
Pengembangan Selanjutnya (Versi 2)
WhatsApp Gateway (pengingat jadwal dan tagihan)
QR Code absensi tutor
Tanda tangan digital orang tua setelah sesi selesai
Penilaian tutor oleh orang tua
Penilaian murid oleh tutor
Pengajuan pengganti jadwal (reschedule)
Modul try out dan bank soal
Aplikasi mobile untuk tutor
Dashboard analitik perkembangan belajar
Integrasi payment gateway (Midtrans/Xendit)
Rekomendasi tambahan

Agar operasional lebih rapi, saya menyarankan menambahkan modul CRM (Customer Relationship Management) untuk admin. Modul ini mencatat seluruh perjalanan calon pelanggan hingga menjadi murid aktif.

Contohnya:

Lead Baru – Orang tua mengisi formulir atau menghubungi admin.
Konsultasi – Admin menggali kebutuhan belajar anak.
Pendaftaran – Orang tua mengisi data dan membayar biaya pendaftaran.
Penugasan Tutor – Admin memilih tutor yang sesuai.
Murid Aktif – Les berjalan rutin.
Perpanjangan Paket – Pengingat ketika paket hampir habis.
Alumni – Murid sudah selesai mengikuti program.

Dengan tambahan modul CRM ini, sistem tidak hanya mengelola proses belajar, tetapi juga membantu admin mengelola calon pelanggan, murid aktif, dan retensi pelanggan dalam satu platform.