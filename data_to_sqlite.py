"""
=============================================================================
LANGKAH 6: INTEGRASI SQLite3
=============================================================================
Proyek PDLR 3 & 4 — Survei Pengalaman Mahasiswa dalam Menggunakan SIAKAD UNJ

Script ini melakukan:
1. Load data dari file Excel (.xlsx)
2. Data Cleaning (handle NaN, duplikat, normalisasi)
3. Export data bersih ke CSV
4. Membuat database SQLite3 dengan 2 tabel relasional
5. Demonstrasi query SQL: SELECT, WHERE, JOIN
=============================================================================
"""

import pandas as pd
import sqlite3
import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# ==================== KONFIGURASI ====================
EXCEL_FILE = "SURVEY PENGALAMAN MAHASISWA DALAM MENGGUNAKAN SIAKAD UNJ (Jawaban).xlsx"
DB_FILE = "siakad_survey.db"
CSV_CLEAN = "data_bersih.csv"

# Kolom profil responden
PROFIL_COLS = [
    'Timestamp', 'Nama Lengkap', 'Status Mahasiswa UNJ', 
    'Prodi (Khusus Rumpun Manajemen) ', 'Umur', 'Jenis Kelamin',
    'Seberapa sering menggunakan siakad?', 'Keperluan Menggunakan Siakad',
    'Pernah mengalami kendala saat menggunakan SIAKAD?'
]

# Label singkat untuk kolom kuesioner Likert
LABEL_KUESIONER = {
    'SIAKAD UNJ sering mengalami loading lama saat diakses': 'loading_lama',
    'SIAKAD UNJ sering error ketika digunakan (misalnya tidak bisa dibuka atau gagal memuat halaman)': 'sering_error',
    'SIAKAD UNJ sering mengalami gangguan saat jam sibuk (misalnya saat mengisi KRS atau pembayaran UKT)': 'gangguan_jam_sibuk',
    'Saya sering harus mengulang akses karena SIAKAD tiba-tiba tidak merespon ': 'mengulang_akses',
    'Fitur dalam SIAKAD UNJ sering tidak berfungsi dengan baik': 'fitur_tidak_berfungsi',
    'Tampilan menu pada SIAKAD UNJ membingungkan bagi pengguna ': 'tampilan_membingungkan',
    'Saya kesulitan memahami alur penggunaan SIAKAD UNJ ': 'kesulitan_alur',
    'Menu dalam SIAKAD UNJ terasa tidak terstruktur dengan baik ': 'menu_tidak_terstruktur',
    'Saya sering kesulitan menemukan informasi atau fitur yang dibutuhkan ': 'kesulitan_menemukan_info',
    'Beberapa proses akademik (seperti mengisi KRS, pembayaran, atau cek nilai) terasa rumit dan membingungkan': 'proses_rumit',
    'Saya merasa kesal saat SIAKAD UNJ mengalami error ': 'kesal_error',
    'Saya merasa frustrasi ketika SIAKAD lambat saat digunakan, terutama pada saat ramai pengguna ': 'frustrasi_lambat',
    'Masalah teknis pada SIAKAD membuat saya tidak nyaman menggunakannya ': 'tidak_nyaman',
    'Saya merasa jengkel ketika harus mengulang proses akibat gangguan sistem ': 'jengkel_mengulang',
    'Pengalaman buruk saat menggunakan SIAKAD membuat saya enggan mengaksesnya kembali': 'enggan_akses',
    'Saya sering mengeluhkan masalah SIAKAD kepada teman atau pihak kampus ': 'mengeluh',
    'Saya menggunakan SIAKAD hanya karena kewajiban, bukan karena kenyamanan ': 'kewajiban_bukan_kenyamanan',
    'Saya merasa terpaksa tetap menggunakan SIAKAD meskipun sering mengalami masalah ': 'terpaksa_menggunakan',
    'Masalah pada SIAKAD membuat saya kurang percaya terhadap sistem akademik kampus ': 'kurang_percaya',
    'Saya merasa pengalaman buruk menggunakan SIAKAD mengurangi kepuasan saya sebagai mahasiswa.': 'kurang_puas',
}

# Kategori kuesioner
KATEGORI = {
    'Performa Sistem': ['loading_lama', 'sering_error', 'gangguan_jam_sibuk', 'mengulang_akses', 'fitur_tidak_berfungsi'],
    'UI/UX (Antarmuka)': ['tampilan_membingungkan', 'kesulitan_alur', 'menu_tidak_terstruktur', 'kesulitan_menemukan_info', 'proses_rumit'],
    'Dampak Emosional': ['kesal_error', 'frustrasi_lambat', 'tidak_nyaman', 'jengkel_mengulang', 'enggan_akses'],
    'Dampak Perilaku': ['mengeluh', 'kewajiban_bukan_kenyamanan', 'terpaksa_menggunakan', 'kurang_percaya', 'kurang_puas'],
}


def load_and_clean_data():
    """Load data dari Excel dan lakukan pembersihan."""
    print("=" * 60)
    print("LANGKAH 6: INTEGRASI SQLite3 — DATA LOADING & CLEANING")
    print("=" * 60)
    
    # Load data
    df = pd.read_excel(EXCEL_FILE)
    print(f"\n✅ Data berhasil dimuat dari Excel")
    print(f"   Jumlah baris awal: {len(df)}")
    print(f"   Jumlah kolom: {len(df.columns)}")
    
    # --- DATA CLEANING ---
    print("\n📋 Proses Data Cleaning:")
    
    # 1. Cek dan hapus duplikat
    duplicates = df.duplicated().sum()
    if duplicates > 0:
        df = df.drop_duplicates()
        print(f"   ❌ Ditemukan {duplicates} data duplikat → dihapus")
    else:
        print(f"   ✅ Tidak ada data duplikat")
    
    # 2. Cek dan handle missing values (NaN)
    nan_count = df.isnull().sum().sum()
    if nan_count > 0:
        print(f"   ⚠️ Ditemukan {nan_count} nilai kosong (NaN)")
        # Untuk kolom numerik, isi dengan median
        numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
        for col in numeric_cols:
            if df[col].isnull().any():
                median_val = df[col].median()
                df[col] = df[col].fillna(median_val)
                print(f"      → Kolom '{col}': NaN diisi dengan median ({median_val})")
        # Untuk kolom string, isi dengan 'Tidak diketahui'
        str_cols = df.select_dtypes(include=['object']).columns
        for col in str_cols:
            if df[col].isnull().any():
                df[col] = df[col].fillna('Tidak diketahui')
                print(f"      → Kolom '{col}': NaN diisi dengan 'Tidak diketahui'")
    else:
        print(f"   ✅ Tidak ada nilai kosong (NaN)")
    
    # 3. Normalisasi kolom Umur (beberapa data berupa angka, beberapa berupa range)
    def normalize_umur(val):
        if pd.isna(val):
            return 'Tidak diketahui'
        if isinstance(val, (int, float)):
            age = int(val)
            if age <= 20:
                return '18-20 tahun'
            elif age <= 23:
                return '21-23 tahun'
            elif age <= 26:
                return '24-26 tahun'
            else:
                return '>27 tahun'
        return str(val)
    
    df['Umur'] = df['Umur'].apply(normalize_umur)
    print("   ✅ Kolom 'Umur' dinormalisasi ke format range")
    
    # 4. Pastikan skor Likert dalam rentang 1-5
    likert_cols = list(LABEL_KUESIONER.keys())
    for col in likert_cols:
        if col in df.columns:
            df[col] = df[col].clip(1, 5).astype(int)
    print("   ✅ Skor Likert divalidasi (rentang 1-5)")
    
    # 5. Hapus kolom Email Address untuk privasi
    if 'Email Address' in df.columns:
        df = df.drop(columns=['Email Address'])
        print("   ✅ Kolom 'Email Address' dihapus untuk privasi data")
    
    print(f"\n📊 Data setelah cleaning: {len(df)} baris, {len(df.columns)} kolom")
    
    return df


def export_to_csv(df):
    """Export data bersih ke CSV."""
    df.to_csv(CSV_CLEAN, index=False, encoding='utf-8-sig')
    print(f"\n💾 Data bersih berhasil disimpan ke: {CSV_CLEAN}")


def create_database(df):
    """Buat database SQLite3 dengan 2 tabel relasional."""
    print("\n" + "=" * 60)
    print("MEMBUAT DATABASE SQLite3")
    print("=" * 60)
    
    # Hapus database lama jika ada
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # --- TABEL 1: RESPONDEN ---
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS responden (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT,
            status_mahasiswa TEXT,
            prodi TEXT,
            umur TEXT,
            jenis_kelamin TEXT,
            frekuensi_penggunaan TEXT,
            keperluan TEXT,
            pernah_kendala TEXT
        )
    ''')
    print("\n✅ Tabel 'responden' berhasil dibuat")
    
    # --- TABEL 2: JAWABAN KUESIONER ---
    cols_kuesioner = ', '.join([f'{label} INTEGER' for label in LABEL_KUESIONER.values()])
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS jawaban_kuesioner (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            responden_id INTEGER,
            {cols_kuesioner},
            FOREIGN KEY (responden_id) REFERENCES responden(id)
        )
    ''')
    print("✅ Tabel 'jawaban_kuesioner' berhasil dibuat (dengan FOREIGN KEY)")
    
    # --- INSERT DATA ---
    print("\n📥 Memasukkan data ke database...")
    
    for idx, row in df.iterrows():
        # Insert ke tabel responden
        cursor.execute('''
            INSERT INTO responden (nama, status_mahasiswa, prodi, umur, jenis_kelamin, 
                                   frekuensi_penggunaan, keperluan, pernah_kendala)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            row.get('Nama Lengkap', ''),
            row.get('Status Mahasiswa UNJ', ''),
            row.get('Prodi (Khusus Rumpun Manajemen) ', ''),
            row.get('Umur', ''),
            row.get('Jenis Kelamin', ''),
            row.get('Seberapa sering menggunakan siakad?', ''),
            row.get('Keperluan Menggunakan Siakad', ''),
            row.get('Pernah mengalami kendala saat menggunakan SIAKAD?', '')
        ))
        
        responden_id = cursor.lastrowid
        
        # Insert ke tabel jawaban_kuesioner
        values = [responden_id]
        for orig_col, label in LABEL_KUESIONER.items():
            values.append(int(row.get(orig_col, 3)))
        
        placeholders = ', '.join(['?'] * len(values))
        col_names = 'responden_id, ' + ', '.join(LABEL_KUESIONER.values())
        cursor.execute(f'INSERT INTO jawaban_kuesioner ({col_names}) VALUES ({placeholders})', values)
    
    conn.commit()
    
    # Verifikasi
    cursor.execute("SELECT COUNT(*) FROM responden")
    count_resp = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM jawaban_kuesioner")
    count_jawab = cursor.fetchone()[0]
    
    print(f"   ✅ Tabel 'responden': {count_resp} baris")
    print(f"   ✅ Tabel 'jawaban_kuesioner': {count_jawab} baris")
    
    conn.close()
    print(f"\n💾 Database berhasil disimpan ke: {DB_FILE}")


def demo_queries():
    """Demonstrasi query SQL: SELECT, WHERE, JOIN."""
    print("\n" + "=" * 60)
    print("DEMONSTRASI QUERY SQL")
    print("=" * 60)
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # --- QUERY 1: SELECT ---
    print("\n📌 QUERY 1: SELECT — Menampilkan 5 responden pertama")
    print("-" * 50)
    cursor.execute("SELECT id, nama, prodi, jenis_kelamin, umur FROM responden LIMIT 5")
    rows = cursor.fetchall()
    print(f"{'ID':<5} {'Nama':<25} {'Prodi':<25} {'JK':<12} {'Umur':<15}")
    print("-" * 82)
    for row in rows:
        print(f"{row[0]:<5} {str(row[1])[:24]:<25} {str(row[2])[:24]:<25} {str(row[3]):<12} {str(row[4]):<15}")
    
    # --- QUERY 2: WHERE ---
    print("\n📌 QUERY 2: WHERE — Responden perempuan yang sering menggunakan SIAKAD")
    print("-" * 50)
    cursor.execute("""
        SELECT id, nama, frekuensi_penggunaan 
        FROM responden 
        WHERE jenis_kelamin = 'Perempuan' 
          AND frekuensi_penggunaan IN ('Sering', 'Sangat sering')
        LIMIT 5
    """)
    rows = cursor.fetchall()
    print(f"{'ID':<5} {'Nama':<30} {'Frekuensi':<20}")
    print("-" * 55)
    for row in rows:
        print(f"{row[0]:<5} {str(row[1])[:29]:<30} {str(row[2]):<20}")
    
    # --- QUERY 3: JOIN ---
    print("\n📌 QUERY 3: JOIN — Gabungkan profil responden dengan jawaban kuesioner")
    print("-" * 50)
    cursor.execute("""
        SELECT r.nama, r.jenis_kelamin, r.umur,
               j.loading_lama, j.sering_error, j.kesal_error, j.frustrasi_lambat
        FROM responden r
        JOIN jawaban_kuesioner j ON r.id = j.responden_id
        WHERE j.kesal_error >= 4
        LIMIT 5
    """)
    rows = cursor.fetchall()
    print(f"{'Nama':<25} {'JK':<12} {'Umur':<15} {'Loading':<8} {'Error':<8} {'Kesal':<8} {'Frustasi':<8}")
    print("-" * 84)
    for row in rows:
        print(f"{str(row[0])[:24]:<25} {str(row[1]):<12} {str(row[2]):<15} {row[3]:<8} {row[4]:<8} {row[5]:<8} {row[6]:<8}")
    
    # --- QUERY 4: Aggregasi ---
    print("\n📌 QUERY 4: Rata-rata skor per jenis kelamin (JOIN + GROUP BY)")
    print("-" * 50)
    cursor.execute("""
        SELECT r.jenis_kelamin,
               ROUND(AVG(j.loading_lama), 2) as avg_loading,
               ROUND(AVG(j.sering_error), 2) as avg_error,
               ROUND(AVG(j.kesal_error), 2) as avg_kesal,
               COUNT(*) as jumlah
        FROM responden r
        JOIN jawaban_kuesioner j ON r.id = j.responden_id
        GROUP BY r.jenis_kelamin
    """)
    rows = cursor.fetchall()
    print(f"{'Jenis Kelamin':<15} {'Avg Loading':<12} {'Avg Error':<12} {'Avg Kesal':<12} {'Jumlah':<8}")
    print("-" * 59)
    for row in rows:
        print(f"{str(row[0]):<15} {row[1]:<12} {row[2]:<12} {row[3]:<12} {row[4]:<8}")
    
    conn.close()
    print("\n✅ Demonstrasi query SQL selesai!")


# ==================== MAIN ====================
if __name__ == "__main__":
    # 1. Load & Clean Data
    df = load_and_clean_data()
    
    # 2. Export ke CSV
    export_to_csv(df)
    
    # 3. Buat Database SQLite3
    create_database(df)
    
    # 4. Demo Queries
    demo_queries()
    
    print("\n" + "=" * 60)
    print("🎉 LANGKAH 6 SELESAI — Database SQLite3 berhasil dibuat!")
    print("=" * 60)
