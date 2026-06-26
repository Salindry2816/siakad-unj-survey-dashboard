# 📊 Dashboard Survei SIAKAD UNJ

Dashboard interaktif untuk menganalisis **Pengalaman Mahasiswa dalam Menggunakan SIAKAD UNJ** (Sistem Informasi Akademik Universitas Negeri Jakarta).

## 📋 Tentang Proyek

Proyek ini merupakan tugas **PDLR (Pengelolaan Data Literasi dan Riset)** yang menganalisis data survei dari 72 responden mahasiswa UNJ mengenai pengalaman mereka menggunakan SIAKAD, meliputi:

- **Performa Sistem** — Loading, error, gangguan jam sibuk
- **UI/UX (Antarmuka)** — Kemudahan navigasi, struktur menu
- **Dampak Emosional** — Frustasi, kekesalan, ketidaknyamanan
- **Dampak Perilaku** — Keengganan, keluhan, kepercayaan

## 🛠️ Teknologi

| Teknologi | Kegunaan |
|-----------|----------|
| Python 3 | Bahasa pemrograman utama |
| SQLite3 | Database relasional |
| Pandas | Pengolahan data |
| Matplotlib & Seaborn | Visualisasi grafik statis |
| Plotly | Visualisasi grafik interaktif |
| Streamlit | Framework dashboard web |

## 📁 Struktur File

```
├── app.py                    # Dashboard Streamlit (Langkah 8)
├── data_to_sqlite.py         # Integrasi SQLite3 (Langkah 6)
├── visualisasi.py            # Pembuatan Grafik (Langkah 7)
├── requirements.txt          # Dependensi Python
├── siakad_survey.db          # Database SQLite3
├── data_bersih.csv           # Data hasil cleaning
├── grafik/                   # Folder grafik statis
│   ├── pie_jenis_kelamin.png
│   ├── pie_frekuensi_penggunaan.png
│   ├── pie_pengalaman_kendala.png
│   ├── bar_rata_rata_kategori.png
│   ├── bar_detail_pertanyaan.png
│   ├── scatter_performa_vs_emosi.png
│   ├── bar_gender_comparison.png
│   └── heatmap_korelasi.png
├── .streamlit/
│   └── config.toml           # Konfigurasi tema Streamlit
└── SURVEY PENGALAMAN...xlsx  # Data survei mentah
```

## 🚀 Cara Menjalankan

### 1. Install Dependensi
```bash
pip install -r requirements.txt
```

### 2. Jalankan Script Database (Langkah 6)
```bash
python data_to_sqlite.py
```

### 3. Buat Grafik Statis (Langkah 7)
```bash
python visualisasi.py
```

### 4. Jalankan Dashboard (Langkah 8)
```bash
streamlit run app.py
```

Dashboard akan terbuka di browser pada `http://localhost:8501`

## 📊 Fitur Dashboard

- **Overview** — KPI cards, distribusi responden (pie chart)
- **Visualisasi** — Grafik interaktif (bar, scatter, heatmap)
- **Data Explorer** — Tabel data yang bisa difilter, sort, dan download
- **Kesimpulan** — Data storytelling dan rekomendasi

### Filter Interaktif
- Jenis Kelamin
- Program Studi
- Kelompok Umur
- Frekuensi Penggunaan
- Pengalaman Kendala

## 👥 Tim

Proyek PDLR 3 & 4 — Universitas Negeri Jakarta
