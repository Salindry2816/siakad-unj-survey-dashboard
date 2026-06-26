"""
Script untuk membuat Laporan Akhir PDF — PDLR 3 & 4
Survei Pengalaman Mahasiswa dalam Menggunakan SIAKAD UNJ
"""

from fpdf import FPDF
import os
import sqlite3
import pandas as pd

GRAFIK_DIR = "grafik"
SCREENSHOT_DIR = "screenshots"
OUTPUT_PDF = "Laporan_Akhir_PDLR_3_4_Survei_SIAKAD_UNJ.pdf"


class LaporanPDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 10)
        self.set_text_color(100, 100, 100)
        self.cell(0, 8, 'Laporan Akhir PDLR 3 & 4 - Survei SIAKAD UNJ', align='C')
        self.ln(5)
        self.set_draw_color(78, 205, 196)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f'Halaman {self.page_no()}/{{nb}}', align='C')

    def chapter_title(self, title):
        self.set_font('Helvetica', 'B', 14)
        self.set_text_color(30, 30, 80)
        self.set_fill_color(240, 248, 255)
        self.cell(0, 12, title, fill=True, new_x='LMARGIN', new_y='NEXT')
        self.ln(4)

    def section_title(self, title):
        self.set_font('Helvetica', 'B', 12)
        self.set_text_color(78, 205, 196)
        self.cell(0, 10, title, new_x='LMARGIN', new_y='NEXT')
        self.ln(2)

    def body_text(self, text):
        self.set_font('Helvetica', '', 10)
        self.set_text_color(40, 40, 40)
        self.multi_cell(0, 6, text)
        self.ln(3)

    def add_image_safe(self, path, w=180):
        if os.path.exists(path):
            self.image(path, x=15, w=w)
            self.ln(5)
        else:
            self.body_text(f"[Gambar tidak ditemukan: {path}]")


def create_report():
    pdf = LaporanPDF()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)

    # ===================== COVER =====================
    pdf.add_page()
    pdf.ln(30)
    pdf.set_font('Helvetica', 'B', 24)
    pdf.set_text_color(30, 30, 80)
    pdf.cell(0, 15, 'LAPORAN AKHIR', align='C', new_x='LMARGIN', new_y='NEXT')
    
    pdf.set_font('Helvetica', 'B', 18)
    pdf.set_text_color(78, 205, 196)
    pdf.cell(0, 12, 'PDLR 3 & 4', align='C', new_x='LMARGIN', new_y='NEXT')
    
    pdf.ln(10)
    pdf.set_font('Helvetica', '', 14)
    pdf.set_text_color(60, 60, 60)
    pdf.cell(0, 10, 'Survei Pengalaman Mahasiswa dalam', align='C', new_x='LMARGIN', new_y='NEXT')
    pdf.cell(0, 10, 'Menggunakan SIAKAD UNJ', align='C', new_x='LMARGIN', new_y='NEXT')
    
    pdf.ln(15)
    pdf.set_draw_color(78, 205, 196)
    pdf.line(60, pdf.get_y(), 150, pdf.get_y())
    pdf.ln(15)
    
    pdf.set_font('Helvetica', '', 11)
    pdf.set_text_color(80, 80, 80)
    info = [
        'Mata Kuliah: Pemrograman dan Data Raya Lanjutan (3 SKS)',
        'Program Studi: Bisnis Digital',
        'Fakultas Ekonomi - Universitas Negeri Jakarta',
        'Dosen Pengampu: Sabo Hermawan, S.Kom., M.Si.',
        '',
        'Tahun Akademik 2025/2026',
    ]
    for line in info:
        pdf.cell(0, 7, line, align='C', new_x='LMARGIN', new_y='NEXT')

    # ===================== DAFTAR ISI =====================
    pdf.add_page()
    pdf.chapter_title('DAFTAR ISI')
    pdf.ln(5)
    toc_items = [
        ('1. Pendahuluan', '3'),
        ('2. Langkah 6: Integrasi SQLite3', '4'),
        ('   2.1 Data Loading & Cleaning', '4'),
        ('   2.2 Pembuatan Database', '4'),
        ('   2.3 Demonstrasi Query SQL', '5'),
        ('3. Langkah 7: Pembuatan Grafik', '6'),
        ('   3.1 Pie Chart - Profil Responden', '6'),
        ('   3.2 Bar Chart - Rata-rata Skor', '7'),
        ('   3.3 Scatter Plot - Korelasi', '8'),
        ('4. Langkah 8: Dashboard Streamlit', '9'),
        ('   4.1 Halaman Overview', '9'),
        ('   4.2 Halaman Visualisasi', '10'),
        ('   4.3 Data Explorer', '11'),
        ('   4.4 Kesimpulan & Data Storytelling', '12'),
        ('5. Langkah 9: Deployment (GitHub)', '13'),
        ('6. Kesimpulan & Rekomendasi', '14'),
    ]
    for title, page in toc_items:
        pdf.set_font('Helvetica', '', 11)
        pdf.set_text_color(40, 40, 40)
        dots = '.' * (70 - len(title))
        pdf.cell(0, 7, f'{title} {dots} {page}', new_x='LMARGIN', new_y='NEXT')

    # ===================== BAB 1: PENDAHULUAN =====================
    pdf.add_page()
    pdf.chapter_title('1. PENDAHULUAN')
    
    pdf.section_title('1.1 Latar Belakang')
    pdf.body_text(
        'Sistem Informasi Akademik (SIAKAD) merupakan platform digital yang digunakan oleh '
        'mahasiswa Universitas Negeri Jakarta (UNJ) untuk mengelola aktivitas akademik seperti '
        'pengisian KRS, pembayaran UKT, dan pengecekan nilai. Seiring meningkatnya jumlah '
        'pengguna, berbagai masalah teknis dan antarmuka mulai dikeluhkan oleh mahasiswa. '
        'Proyek ini bertujuan untuk menganalisis pengalaman mahasiswa dalam menggunakan '
        'SIAKAD UNJ melalui survei kuesioner berbasis skala Likert (1-5).'
    )
    
    pdf.section_title('1.2 Tujuan Proyek')
    pdf.body_text(
        '1. Mengumpulkan data pengalaman mahasiswa melalui Google Form (Tahap 1-2)\n'
        '2. Membersihkan dan mengolah data menggunakan Python/Pandas (Tahap 2)\n'
        '3. Menyimpan data bersih ke database SQLite3 relasional (Langkah 6)\n'
        '4. Membuat visualisasi grafik menggunakan Matplotlib/Seaborn (Langkah 7)\n'
        '5. Membangun dashboard interaktif menggunakan Streamlit (Langkah 8)\n'
        '6. Melakukan deployment ke GitHub dan Streamlit Cloud (Langkah 9)'
    )
    
    pdf.section_title('1.3 Data Survei')
    pdf.body_text(
        'Data dikumpulkan melalui Google Form dengan total 72 responden mahasiswa UNJ, '
        'khususnya dari rumpun Manajemen (Bisnis Digital, Pemasaran Digital, Manajemen). '
        'Kuesioner terdiri dari 30 kolom yang mencakup profil responden dan 20 pertanyaan '
        'Likert yang dibagi ke dalam 4 kategori:\n\n'
        '- Performa Sistem (5 pertanyaan)\n'
        '- UI/UX / Antarmuka (5 pertanyaan)\n'
        '- Dampak Emosional (5 pertanyaan)\n'
        '- Dampak Perilaku (5 pertanyaan)'
    )

    # ===================== BAB 2: LANGKAH 6 =====================
    pdf.add_page()
    pdf.chapter_title('2. LANGKAH 6: INTEGRASI SQLite3')
    
    pdf.section_title('2.1 Data Loading & Cleaning')
    pdf.body_text(
        'Data mentah dari file Excel (.xlsx) dimuat menggunakan library Pandas. '
        'Proses Data Cleaning yang dilakukan meliputi:\n\n'
        '- Pengecekan dan penghapusan data duplikat (tidak ditemukan duplikat)\n'
        '- Pengecekan nilai kosong/NaN (tidak ditemukan NaN)\n'
        '- Normalisasi kolom Umur ke format range (18-20, 21-23, 24-26, >27 tahun)\n'
        '- Validasi skor Likert dalam rentang 1-5\n'
        '- Penghapusan kolom Email Address untuk menjaga privasi data\n\n'
        'Hasil: 72 baris data bersih dengan 29 kolom disimpan ke file data_bersih.csv'
    )
    
    pdf.section_title('2.2 Pembuatan Database SQLite3')
    pdf.body_text(
        'Database relasional siakad_survey.db dibuat dengan 2 tabel yang saling berelasi '
        'melalui FOREIGN KEY:\n\n'
        '1. Tabel "responden" (9 kolom): id, nama, status_mahasiswa, prodi, umur, '
        'jenis_kelamin, frekuensi_penggunaan, keperluan, pernah_kendala\n\n'
        '2. Tabel "jawaban_kuesioner" (22 kolom): id, responden_id (FK), dan 20 kolom '
        'jawaban Likert (loading_lama, sering_error, gangguan_jam_sibuk, dll.)\n\n'
        'Kedua tabel dihubungkan melalui kolom responden_id yang mereferensi id di tabel responden.'
    )
    
    pdf.section_title('2.3 Demonstrasi Query SQL')
    pdf.body_text(
        'Berikut adalah demonstrasi query SQL yang dilakukan:\n\n'
        'QUERY 1 - SELECT: Menampilkan 5 responden pertama\n'
        '  SELECT id, nama, prodi, jenis_kelamin, umur FROM responden LIMIT 5\n\n'
        'QUERY 2 - WHERE: Filter responden perempuan yang sering menggunakan SIAKAD\n'
        '  SELECT id, nama, frekuensi_penggunaan FROM responden\n'
        '  WHERE jenis_kelamin = \'Perempuan\'\n'
        '  AND frekuensi_penggunaan IN (\'Sering\', \'Sangat sering\')\n\n'
        'QUERY 3 - JOIN: Gabungkan profil responden dengan jawaban kuesioner\n'
        '  SELECT r.nama, r.jenis_kelamin, j.loading_lama, j.kesal_error\n'
        '  FROM responden r JOIN jawaban_kuesioner j\n'
        '  ON r.id = j.responden_id WHERE j.kesal_error >= 4\n\n'
        'QUERY 4 - GROUP BY + AVG: Rata-rata skor per jenis kelamin\n'
        '  SELECT r.jenis_kelamin, AVG(j.loading_lama), AVG(j.kesal_error)\n'
        '  FROM responden r JOIN jawaban_kuesioner j ON r.id = j.responden_id\n'
        '  GROUP BY r.jenis_kelamin'
    )

    # ===================== BAB 3: LANGKAH 7 =====================
    pdf.add_page()
    pdf.chapter_title('3. LANGKAH 7: PEMBUATAN GRAFIK')
    pdf.body_text(
        'Visualisasi data dibuat menggunakan library Matplotlib dan Seaborn. '
        'Berikut adalah grafik-grafik yang dihasilkan:'
    )
    
    pdf.section_title('3.1 Pie Chart - Distribusi Profil Responden')
    pdf.body_text('Grafik berikut menunjukkan distribusi jenis kelamin responden:')
    pdf.add_image_safe(os.path.join(GRAFIK_DIR, 'pie_jenis_kelamin.png'), w=130)
    
    pdf.body_text('Distribusi frekuensi penggunaan SIAKAD:')
    pdf.add_image_safe(os.path.join(GRAFIK_DIR, 'pie_frekuensi_penggunaan.png'), w=130)
    
    pdf.add_page()
    pdf.body_text('Persentase responden yang pernah mengalami kendala:')
    pdf.add_image_safe(os.path.join(GRAFIK_DIR, 'pie_pengalaman_kendala.png'), w=130)
    
    pdf.section_title('3.2 Bar Chart - Rata-rata Skor Likert')
    pdf.body_text('Rata-rata skor per kategori kuesioner:')
    pdf.add_image_safe(os.path.join(GRAFIK_DIR, 'bar_rata_rata_kategori.png'), w=160)
    
    pdf.add_page()
    pdf.body_text('Detail rata-rata skor per pertanyaan (20 pertanyaan):')
    pdf.add_image_safe(os.path.join(GRAFIK_DIR, 'bar_detail_pertanyaan.png'), w=170)
    
    pdf.body_text('Perbandingan skor per kategori berdasarkan jenis kelamin:')
    pdf.add_image_safe(os.path.join(GRAFIK_DIR, 'bar_gender_comparison.png'), w=160)
    
    pdf.add_page()
    pdf.section_title('3.3 Scatter Plot - Korelasi Performa vs Emosi')
    pdf.body_text(
        'Scatter plot berikut menunjukkan korelasi antara rata-rata skor Performa Sistem '
        'dan Dampak Emosional per responden. Terdapat korelasi positif yang kuat, '
        'menunjukkan bahwa semakin buruk performa sistem yang dirasakan, semakin tinggi '
        'dampak emosional negatif yang dialami mahasiswa.'
    )
    pdf.add_image_safe(os.path.join(GRAFIK_DIR, 'scatter_performa_vs_emosi.png'), w=160)
    
    pdf.body_text('Matriks korelasi antar pertanyaan kuesioner (Heatmap):')
    pdf.add_image_safe(os.path.join(GRAFIK_DIR, 'heatmap_korelasi.png'), w=170)

    # ===================== BAB 4: LANGKAH 8 =====================
    pdf.add_page()
    pdf.chapter_title('4. LANGKAH 8: DASHBOARD STREAMLIT')
    pdf.body_text(
        'Dashboard interaktif dibangun menggunakan framework Streamlit dengan fitur:\n\n'
        '- Layout web responsif dengan tema gelap premium\n'
        '- Sidebar dengan filter interaktif (Jenis Kelamin, Prodi, Umur, Frekuensi, Kendala)\n'
        '- 4 halaman tab: Overview, Visualisasi, Data Explorer, Kesimpulan\n'
        '- Grafik interaktif menggunakan Plotly (hover, zoom, pan)\n'
        '- Tabel data yang bisa di-sort dan di-download (CSV)\n'
        '- Data Storytelling dengan insight dan rekomendasi otomatis'
    )
    
    pdf.section_title('4.1 Halaman Overview')
    pdf.body_text('Tampilan utama dashboard dengan KPI Cards dan distribusi responden:')
    pdf.add_image_safe(os.path.join(SCREENSHOT_DIR, 'dashboard_overview.png'), w=175)
    
    pdf.add_page()
    pdf.body_text('Distribusi responden dalam bentuk Pie Chart dan Bar Chart:')
    pdf.add_image_safe(os.path.join(SCREENSHOT_DIR, 'dashboard_pie_charts.png'), w=175)
    
    pdf.section_title('4.2 Halaman Visualisasi')
    pdf.body_text('Grafik interaktif rata-rata skor per kategori dan per pertanyaan:')
    pdf.add_image_safe(os.path.join(SCREENSHOT_DIR, 'dashboard_visualisasi_bar.png'), w=175)
    
    pdf.add_page()
    pdf.body_text('Scatter plot korelasi Performa Sistem vs Dampak Emosional (interaktif):')
    pdf.add_image_safe(os.path.join(SCREENSHOT_DIR, 'dashboard_scatter.png'), w=175)
    
    pdf.section_title('4.3 Data Explorer')
    pdf.body_text('Tabel data interaktif dengan fitur filter, sort, dan download CSV:')
    pdf.add_image_safe(os.path.join(SCREENSHOT_DIR, 'dashboard_data_explorer.png'), w=175)
    
    pdf.add_page()
    pdf.section_title('4.4 Kesimpulan & Data Storytelling')
    pdf.body_text('Halaman kesimpulan dengan insight otomatis berdasarkan data:')
    pdf.add_image_safe(os.path.join(SCREENSHOT_DIR, 'dashboard_kesimpulan.png'), w=175)

    # ===================== BAB 5: LANGKAH 9 =====================
    pdf.add_page()
    pdf.chapter_title('5. LANGKAH 9: DEPLOYMENT')
    
    pdf.section_title('5.1 GitHub Repository')
    pdf.body_text(
        'Source code Python telah diunggah ke GitHub repository:\n\n'
        'Repository: https://github.com/Salindry2816/siakad-unj-survey-dashboard\n\n'
        'File yang diunggah:\n'
        '- app.py (Dashboard Streamlit)\n'
        '- data_to_sqlite.py (Integrasi SQLite3)\n'
        '- visualisasi.py (Pembuatan Grafik)\n'
        '- requirements.txt (Dependensi Python)\n'
        '- siakad_survey.db (Database SQLite3)\n'
        '- data_bersih.csv (Data hasil cleaning)\n'
        '- grafik/ (Folder grafik statis)\n'
        '- .streamlit/config.toml (Konfigurasi tema)\n'
        '- README.md (Dokumentasi proyek)'
    )
    
    pdf.section_title('5.2 Streamlit Cloud Deployment')
    pdf.body_text(
        'Dashboard dapat di-deploy ke Streamlit Cloud melalui langkah berikut:\n\n'
        '1. Buka https://share.streamlit.io\n'
        '2. Login menggunakan akun GitHub\n'
        '3. Pilih repository: Salindry2816/siakad-unj-survey-dashboard\n'
        '4. Set Main file path: app.py\n'
        '5. Klik Deploy\n\n'
        'Dashboard akan mendapatkan URL publik yang bisa diakses oleh siapa saja.'
    )

    # ===================== BAB 6: KESIMPULAN =====================
    pdf.add_page()
    pdf.chapter_title('6. KESIMPULAN & REKOMENDASI')
    
    # Load data for dynamic stats
    conn = sqlite3.connect('siakad_survey.db')
    df = pd.read_sql_query("""
        SELECT r.*, j.* FROM responden r 
        JOIN jawaban_kuesioner j ON r.id = j.responden_id
    """, conn)
    conn.close()
    df = df.loc[:, ~df.columns.duplicated()]
    
    performa_cols = ['loading_lama', 'sering_error', 'gangguan_jam_sibuk', 'mengulang_akses', 'fitur_tidak_berfungsi']
    uiux_cols = ['tampilan_membingungkan', 'kesulitan_alur', 'menu_tidak_terstruktur', 'kesulitan_menemukan_info', 'proses_rumit']
    emosi_cols = ['kesal_error', 'frustrasi_lambat', 'tidak_nyaman', 'jengkel_mengulang', 'enggan_akses']
    perilaku_cols = ['mengeluh', 'kewajiban_bukan_kenyamanan', 'terpaksa_menggunakan', 'kurang_percaya', 'kurang_puas']
    
    avg_p = df[performa_cols].mean().mean()
    avg_u = df[uiux_cols].mean().mean()
    avg_e = df[emosi_cols].mean().mean()
    avg_b = df[perilaku_cols].mean().mean()
    pernah = len(df[df['pernah_kendala'] == 'Pernah'])
    pct = pernah / len(df) * 100
    
    pdf.section_title('6.1 Kesimpulan')
    pdf.body_text(
        f'Berdasarkan analisis data survei terhadap {len(df)} responden mahasiswa UNJ, '
        f'diperoleh temuan sebagai berikut:\n\n'
        f'1. Performa Sistem mendapat skor rata-rata {avg_p:.2f}/5, menunjukkan bahwa '
        f'masalah teknis (loading lama, error, gangguan jam sibuk) menjadi keluhan utama.\n\n'
        f'2. UI/UX (Antarmuka) mendapat skor {avg_u:.2f}/5, mengindikasikan bahwa '
        f'navigasi dan struktur menu SIAKAD masih perlu perbaikan.\n\n'
        f'3. Dampak Emosional mendapat skor {avg_e:.2f}/5, menunjukkan tingkat '
        f'frustasi dan ketidaknyamanan yang cukup tinggi di kalangan mahasiswa.\n\n'
        f'4. Dampak Perilaku mendapat skor {avg_b:.2f}/5, di mana banyak mahasiswa '
        f'menggunakan SIAKAD hanya karena kewajiban, bukan kenyamanan.\n\n'
        f'5. Sebanyak {pct:.0f}% responden menyatakan pernah mengalami kendala teknis '
        f'saat menggunakan SIAKAD.'
    )
    
    pdf.section_title('6.2 Rekomendasi')
    pdf.body_text(
        'Berdasarkan hasil analisis, berikut rekomendasi yang diberikan:\n\n'
        '1. Perbaikan Infrastruktur Server - Tingkatkan kapasitas server terutama saat '
        'jam sibuk (pengisian KRS, pembayaran UKT) untuk mengurangi loading lama.\n\n'
        '2. Redesign Antarmuka (UI/UX) - Sederhanakan navigasi menu dan perbaiki '
        'struktur informasi agar mahasiswa lebih mudah menemukan fitur yang dibutuhkan. '
        'Berdasarkan data, antarmuka aplikasi ini sulit dipahami oleh beberapa responden, '
        'sehingga perlu penyederhanaan menu.\n\n'
        '3. Optimasi Mobile - Pastikan SIAKAD dapat diakses dengan baik melalui '
        'perangkat mobile.\n\n'
        '4. Peningkatan Support - Sediakan helpdesk atau FAQ yang mudah diakses.\n\n'
        '5. Monitoring Real-time - Implementasikan sistem monitoring untuk mendeteksi '
        'dan menangani masalah teknis sebelum berdampak luas.'
    )
    
    pdf.ln(10)
    pdf.set_draw_color(78, 205, 196)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)
    pdf.set_font('Helvetica', 'I', 9)
    pdf.set_text_color(120, 120, 120)
    pdf.cell(0, 6, 'Laporan ini dibuat sebagai bagian dari tugas PDLR 3 & 4', align='C', new_x='LMARGIN', new_y='NEXT')
    pdf.cell(0, 6, 'Mata Kuliah: Pemrograman dan Data Raya Lanjutan', align='C', new_x='LMARGIN', new_y='NEXT')
    pdf.cell(0, 6, 'Program Studi Bisnis Digital - FEB UNJ', align='C', new_x='LMARGIN', new_y='NEXT')

    # Save
    pdf.output(OUTPUT_PDF)
    print(f"Laporan PDF berhasil dibuat: {OUTPUT_PDF}")
    print(f"Jumlah halaman: {pdf.pages_count}")


if __name__ == '__main__':
    create_report()
