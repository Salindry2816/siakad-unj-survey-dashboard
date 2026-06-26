"""
=============================================================================
LANGKAH 7: PEMBUATAN GRAFIK (VISUALISASI DATA)
=============================================================================
Proyek PDLR 3 & 4 — Survei Pengalaman Mahasiswa dalam Menggunakan SIAKAD UNJ

Script ini membuat visualisasi data menggunakan Matplotlib dan Seaborn:
1. Pie Chart — Distribusi profil responden
2. Bar Chart — Rata-rata skor Likert per kategori
3. Scatter Plot — Korelasi performa vs kepuasan
4. Bar Chart — Perbandingan skor berdasarkan jenis kelamin
=============================================================================
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import seaborn as sns
import sqlite3
import os
import numpy as np

# ==================== KONFIGURASI ====================
DB_FILE = "siakad_survey.db"
GRAFIK_DIR = "grafik"

# Mapping label kuesioner
LABEL_KUESIONER = {
    'loading_lama': 'Loading Lama',
    'sering_error': 'Sering Error',
    'gangguan_jam_sibuk': 'Gangguan Jam Sibuk',
    'mengulang_akses': 'Mengulang Akses',
    'fitur_tidak_berfungsi': 'Fitur Tidak Berfungsi',
    'tampilan_membingungkan': 'Tampilan Membingungkan',
    'kesulitan_alur': 'Kesulitan Alur',
    'menu_tidak_terstruktur': 'Menu Tidak Terstruktur',
    'kesulitan_menemukan_info': 'Kesulitan Menemukan Info',
    'proses_rumit': 'Proses Rumit',
    'kesal_error': 'Kesal Error',
    'frustrasi_lambat': 'Frustrasi Lambat',
    'tidak_nyaman': 'Tidak Nyaman',
    'jengkel_mengulang': 'Jengkel Mengulang',
    'enggan_akses': 'Enggan Akses',
    'mengeluh': 'Mengeluh',
    'kewajiban_bukan_kenyamanan': 'Kewajiban',
    'terpaksa_menggunakan': 'Terpaksa',
    'kurang_percaya': 'Kurang Percaya',
    'kurang_puas': 'Kurang Puas',
}

# Kategori kuesioner
KATEGORI = {
    'Performa Sistem': ['loading_lama', 'sering_error', 'gangguan_jam_sibuk', 'mengulang_akses', 'fitur_tidak_berfungsi'],
    'UI/UX (Antarmuka)': ['tampilan_membingungkan', 'kesulitan_alur', 'menu_tidak_terstruktur', 'kesulitan_menemukan_info', 'proses_rumit'],
    'Dampak Emosional': ['kesal_error', 'frustrasi_lambat', 'tidak_nyaman', 'jengkel_mengulang', 'enggan_akses'],
    'Dampak Perilaku': ['mengeluh', 'kewajiban_bukan_kenyamanan', 'terpaksa_menggunakan', 'kurang_percaya', 'kurang_puas'],
}

# Warna tema
COLORS_PIE = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', '#98D8C8']
COLORS_BAR = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFEAA7']
COLOR_MALE = '#45B7D1'
COLOR_FEMALE = '#FF6B9E'

# Style global
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")


def load_data_from_db():
    """Load data dari database SQLite3 menggunakan JOIN."""
    conn = sqlite3.connect(DB_FILE)
    
    query = """
        SELECT r.*, j.*
        FROM responden r
        JOIN jawaban_kuesioner j ON r.id = j.responden_id
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    # Hapus kolom duplikat id
    if 'id' in df.columns:
        df = df.loc[:, ~df.columns.duplicated()]
    
    print(f"✅ Data berhasil dimuat dari database: {len(df)} responden")
    return df


def pie_chart_jenis_kelamin(df):
    """Pie Chart: Distribusi Jenis Kelamin Responden."""
    fig, ax = plt.subplots(figsize=(8, 6))
    
    counts = df['jenis_kelamin'].value_counts()
    
    wedges, texts, autotexts = ax.pie(
        counts.values,
        labels=counts.index,
        autopct='%1.1f%%',
        colors=COLORS_PIE[:len(counts)],
        startangle=90,
        explode=[0.05] * len(counts),
        shadow=True,
        textprops={'fontsize': 12, 'fontweight': 'bold'}
    )
    
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(13)
        autotext.set_fontweight('bold')
    
    ax.set_title('Distribusi Jenis Kelamin Responden', fontsize=16, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.savefig(os.path.join(GRAFIK_DIR, 'pie_jenis_kelamin.png'), dpi=150, bbox_inches='tight')
    plt.close()
    print("   ✅ Pie Chart: Jenis Kelamin — disimpan")


def pie_chart_frekuensi(df):
    """Pie Chart: Distribusi Frekuensi Penggunaan SIAKAD."""
    fig, ax = plt.subplots(figsize=(8, 6))
    
    counts = df['frekuensi_penggunaan'].value_counts()
    
    wedges, texts, autotexts = ax.pie(
        counts.values,
        labels=counts.index,
        autopct='%1.1f%%',
        colors=COLORS_PIE[:len(counts)],
        startangle=90,
        explode=[0.03] * len(counts),
        shadow=True,
        textprops={'fontsize': 11, 'fontweight': 'bold'}
    )
    
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(12)
        autotext.set_fontweight('bold')
    
    ax.set_title('Frekuensi Penggunaan SIAKAD UNJ', fontsize=16, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.savefig(os.path.join(GRAFIK_DIR, 'pie_frekuensi_penggunaan.png'), dpi=150, bbox_inches='tight')
    plt.close()
    print("   ✅ Pie Chart: Frekuensi Penggunaan — disimpan")


def pie_chart_kendala(df):
    """Pie Chart: Pengalaman Kendala Responden."""
    fig, ax = plt.subplots(figsize=(8, 6))
    
    counts = df['pernah_kendala'].value_counts()
    
    explode_vals = [0.05] + [0.02] * (len(counts) - 1)
    wedges, texts, autotexts = ax.pie(
        counts.values,
        labels=counts.index,
        autopct='%1.1f%%',
        colors=['#FF6B6B', '#4ECDC4', '#FFEAA7'][:len(counts)],
        startangle=90,
        explode=explode_vals,
        shadow=True,
        textprops={'fontsize': 13, 'fontweight': 'bold'}
    )
    
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(14)
        autotext.set_fontweight('bold')
    
    ax.set_title('Pernah Mengalami Kendala SIAKAD?', fontsize=16, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.savefig(os.path.join(GRAFIK_DIR, 'pie_pengalaman_kendala.png'), dpi=150, bbox_inches='tight')
    plt.close()
    print("   ✅ Pie Chart: Pengalaman Kendala — disimpan")


def bar_chart_rata_rata_kategori(df):
    """Bar Chart: Rata-rata Skor Likert per Kategori."""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    kategori_means = {}
    for kat, cols in KATEGORI.items():
        existing_cols = [c for c in cols if c in df.columns]
        if existing_cols:
            kategori_means[kat] = df[existing_cols].mean().mean()
    
    categories = list(kategori_means.keys())
    values = list(kategori_means.values())
    
    bars = ax.bar(categories, values, color=COLORS_BAR, edgecolor='white', linewidth=2, width=0.6)
    
    # Tambah label nilai di atas bar
    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.05,
                f'{val:.2f}', ha='center', va='bottom', fontsize=13, fontweight='bold')
    
    ax.set_ylabel('Rata-rata Skor (1-5)', fontsize=12, fontweight='bold')
    ax.set_title('Rata-rata Skor Likert per Kategori', fontsize=16, fontweight='bold', pad=15)
    ax.set_ylim(0, 5.5)
    ax.axhline(y=3, color='gray', linestyle='--', alpha=0.5, label='Skor Netral (3)')
    ax.legend(fontsize=10)
    
    plt.xticks(fontsize=11, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(GRAFIK_DIR, 'bar_rata_rata_kategori.png'), dpi=150, bbox_inches='tight')
    plt.close()
    print("   ✅ Bar Chart: Rata-rata per Kategori — disimpan")


def bar_chart_detail_pertanyaan(df):
    """Bar Chart: Rata-rata Skor per Pertanyaan (semua 20 pertanyaan)."""
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # Hitung rata-rata per pertanyaan
    means = {}
    for col, label in LABEL_KUESIONER.items():
        if col in df.columns:
            means[label] = df[col].mean()
    
    labels = list(means.keys())
    values = list(means.values())
    
    # Warnai berdasarkan kategori
    colors = []
    for col in LABEL_KUESIONER.keys():
        if col in KATEGORI.get('Performa Sistem', []):
            colors.append(COLORS_BAR[0])
        elif col in KATEGORI.get('UI/UX (Antarmuka)', []):
            colors.append(COLORS_BAR[1])
        elif col in KATEGORI.get('Dampak Emosional', []):
            colors.append(COLORS_BAR[2])
        else:
            colors.append(COLORS_BAR[3])
    
    bars = ax.barh(labels, values, color=colors, edgecolor='white', linewidth=1)
    
    # Label nilai
    for bar, val in zip(bars, values):
        ax.text(val + 0.05, bar.get_y() + bar.get_height() / 2,
                f'{val:.2f}', ha='left', va='center', fontsize=10, fontweight='bold')
    
    ax.set_xlabel('Rata-rata Skor (1-5)', fontsize=12, fontweight='bold')
    ax.set_title('Rata-rata Skor per Pertanyaan Kuesioner', fontsize=16, fontweight='bold', pad=15)
    ax.set_xlim(0, 5.5)
    ax.axvline(x=3, color='gray', linestyle='--', alpha=0.5)
    
    # Legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor=COLORS_BAR[0], label='Performa Sistem'),
        Patch(facecolor=COLORS_BAR[1], label='UI/UX (Antarmuka)'),
        Patch(facecolor=COLORS_BAR[2], label='Dampak Emosional'),
        Patch(facecolor=COLORS_BAR[3], label='Dampak Perilaku'),
    ]
    ax.legend(handles=legend_elements, loc='lower right', fontsize=10)
    
    plt.tight_layout()
    plt.savefig(os.path.join(GRAFIK_DIR, 'bar_detail_pertanyaan.png'), dpi=150, bbox_inches='tight')
    plt.close()
    print("   ✅ Bar Chart: Detail Pertanyaan — disimpan")


def scatter_plot_performa_vs_kepuasan(df):
    """Scatter Plot: Korelasi Performa Sistem vs Dampak Emosional."""
    fig, ax = plt.subplots(figsize=(10, 7))
    
    # Hitung rata-rata per responden
    performa_cols = [c for c in KATEGORI['Performa Sistem'] if c in df.columns]
    emosi_cols = [c for c in KATEGORI['Dampak Emosional'] if c in df.columns]
    
    df_plot = df.copy()
    df_plot['avg_performa'] = df_plot[performa_cols].mean(axis=1)
    df_plot['avg_emosi'] = df_plot[emosi_cols].mean(axis=1)
    
    # Warna berdasarkan jenis kelamin
    colors_map = {'Laki-laki': COLOR_MALE, 'Perempuan': COLOR_FEMALE}
    
    for jk, color in colors_map.items():
        mask = df_plot['jenis_kelamin'] == jk
        ax.scatter(
            df_plot.loc[mask, 'avg_performa'],
            df_plot.loc[mask, 'avg_emosi'],
            c=color, label=jk, alpha=0.7, s=80, edgecolors='white', linewidth=1
        )
    
    # Trend line
    z = np.polyfit(df_plot['avg_performa'], df_plot['avg_emosi'], 1)
    p = np.poly1d(z)
    x_line = np.linspace(df_plot['avg_performa'].min(), df_plot['avg_performa'].max(), 100)
    ax.plot(x_line, p(x_line), '--', color='gray', alpha=0.8, linewidth=2, label='Trend Line')
    
    # Korelasi
    corr = df_plot['avg_performa'].corr(df_plot['avg_emosi'])
    ax.text(0.05, 0.95, f'Korelasi (r): {corr:.3f}', transform=ax.transAxes,
            fontsize=12, fontweight='bold', verticalalignment='top',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='lightyellow', alpha=0.8))
    
    ax.set_xlabel('Rata-rata Skor Performa Sistem', fontsize=12, fontweight='bold')
    ax.set_ylabel('Rata-rata Skor Dampak Emosional', fontsize=12, fontweight='bold')
    ax.set_title('Korelasi Performa Sistem vs Dampak Emosional', fontsize=16, fontweight='bold', pad=15)
    ax.legend(fontsize=11)
    ax.set_xlim(0.5, 5.5)
    ax.set_ylim(0.5, 5.5)
    
    plt.tight_layout()
    plt.savefig(os.path.join(GRAFIK_DIR, 'scatter_performa_vs_emosi.png'), dpi=150, bbox_inches='tight')
    plt.close()
    print("   ✅ Scatter Plot: Performa vs Emosi — disimpan")


def bar_chart_gender_comparison(df):
    """Bar Chart: Perbandingan Skor per Kategori berdasarkan Jenis Kelamin."""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    gender_data = {}
    for jk in df['jenis_kelamin'].unique():
        df_jk = df[df['jenis_kelamin'] == jk]
        gender_data[jk] = {}
        for kat, cols in KATEGORI.items():
            existing = [c for c in cols if c in df.columns]
            if existing:
                gender_data[jk][kat] = df_jk[existing].mean().mean()
    
    x = np.arange(len(KATEGORI))
    width = 0.35
    
    genders = list(gender_data.keys())
    colors_gender = [COLOR_MALE if 'Laki' in g else COLOR_FEMALE for g in genders]
    
    for i, (gender, color) in enumerate(zip(genders, colors_gender)):
        values = [gender_data[gender].get(k, 0) for k in KATEGORI.keys()]
        offset = width * (i - (len(genders) - 1) / 2)
        bars = ax.bar(x + offset, values, width, label=gender, color=color, edgecolor='white', linewidth=1.5)
        
        for bar, val in zip(bars, values):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.05,
                    f'{val:.2f}', ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    ax.set_xticks(x)
    ax.set_xticklabels(KATEGORI.keys(), fontsize=11, fontweight='bold')
    ax.set_ylabel('Rata-rata Skor (1-5)', fontsize=12, fontweight='bold')
    ax.set_title('Perbandingan Skor per Kategori berdasarkan Jenis Kelamin', fontsize=15, fontweight='bold', pad=15)
    ax.set_ylim(0, 5.5)
    ax.axhline(y=3, color='gray', linestyle='--', alpha=0.5)
    ax.legend(fontsize=11)
    
    plt.tight_layout()
    plt.savefig(os.path.join(GRAFIK_DIR, 'bar_gender_comparison.png'), dpi=150, bbox_inches='tight')
    plt.close()
    print("   ✅ Bar Chart: Perbandingan Gender — disimpan")


def heatmap_korelasi(df):
    """Heatmap: Korelasi antar pertanyaan kuesioner."""
    fig, ax = plt.subplots(figsize=(14, 10))
    
    likert_cols = [c for c in LABEL_KUESIONER.keys() if c in df.columns]
    labels = [LABEL_KUESIONER[c] for c in likert_cols]
    
    corr_matrix = df[likert_cols].corr()
    corr_matrix.index = labels
    corr_matrix.columns = labels
    
    sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='RdYlBu_r',
                center=0, vmin=-1, vmax=1, ax=ax,
                square=True, linewidths=0.5,
                annot_kws={'fontsize': 7})
    
    ax.set_title('Matriks Korelasi Antar Pertanyaan Kuesioner', fontsize=16, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.savefig(os.path.join(GRAFIK_DIR, 'heatmap_korelasi.png'), dpi=150, bbox_inches='tight')
    plt.close()
    print("   ✅ Heatmap: Korelasi — disimpan")


# ==================== MAIN ====================
if __name__ == "__main__":
    print("=" * 60)
    print("LANGKAH 7: PEMBUATAN GRAFIK (VISUALISASI DATA)")
    print("=" * 60)
    
    # Buat folder grafik
    os.makedirs(GRAFIK_DIR, exist_ok=True)
    
    # Load data
    df = load_data_from_db()
    
    # Buat semua grafik
    print("\n📊 Membuat visualisasi grafik...\n")
    
    pie_chart_jenis_kelamin(df)
    pie_chart_frekuensi(df)
    pie_chart_kendala(df)
    bar_chart_rata_rata_kategori(df)
    bar_chart_detail_pertanyaan(df)
    scatter_plot_performa_vs_kepuasan(df)
    bar_chart_gender_comparison(df)
    heatmap_korelasi(df)
    
    print(f"\n📁 Semua grafik tersimpan di folder: {GRAFIK_DIR}/")
    print("\n" + "=" * 60)
    print("🎉 LANGKAH 7 SELESAI — Semua grafik berhasil dibuat!")
    print("=" * 60)
