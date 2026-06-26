"""
=============================================================================
LANGKAH 8: DESAIN DASHBOARD STREAMLIT
=============================================================================
Proyek PDLR 3 & 4 — Survei Pengalaman Mahasiswa dalam Menggunakan SIAKAD UNJ

Dashboard interaktif yang menampilkan:
- Overview & KPI Cards
- Visualisasi Grafik (Pie, Bar, Scatter) menggunakan Plotly
- Data Explorer (tabel interaktif)
- Kesimpulan & Data Storytelling
=============================================================================
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sqlite3
import numpy as np
import os

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="📊 Dashboard SIAKAD UNJ — Survei Mahasiswa",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== KONFIGURASI ====================
DB_FILE = "siakad_survey.db"

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

KATEGORI = {
    'Performa Sistem': ['loading_lama', 'sering_error', 'gangguan_jam_sibuk', 'mengulang_akses', 'fitur_tidak_berfungsi'],
    'UI/UX (Antarmuka)': ['tampilan_membingungkan', 'kesulitan_alur', 'menu_tidak_terstruktur', 'kesulitan_menemukan_info', 'proses_rumit'],
    'Dampak Emosional': ['kesal_error', 'frustrasi_lambat', 'tidak_nyaman', 'jengkel_mengulang', 'enggan_akses'],
    'Dampak Perilaku': ['mengeluh', 'kewajiban_bukan_kenyamanan', 'terpaksa_menggunakan', 'kurang_percaya', 'kurang_puas'],
}

WARNA_KATEGORI = {
    'Performa Sistem': '#FF6B6B',
    'UI/UX (Antarmuka)': '#4ECDC4',
    'Dampak Emosional': '#45B7D1',
    'Dampak Perilaku': '#FFEAA7',
}


# ==================== CUSTOM CSS ====================
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
        border-right: 2px solid #4ECDC4;
    }
    
    /* Cards */
    .metric-card {
        background: linear-gradient(135deg, rgba(78, 205, 196, 0.15), rgba(69, 183, 209, 0.15));
        border: 1px solid rgba(78, 205, 196, 0.3);
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        backdrop-filter: blur(10px);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(78, 205, 196, 0.25);
    }
    .metric-value {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #4ECDC4, #45B7D1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 5px 0;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #a0a0c0;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Header */
    .main-header {
        text-align: center;
        padding: 30px 0 20px 0;
    }
    .main-header h1 {
        background: linear-gradient(135deg, #4ECDC4, #45B7D1, #FF6B9E);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem;
        font-weight: 900;
        margin-bottom: 5px;
    }
    .main-header p {
        color: #a0a0c0;
        font-size: 1.1rem;
    }
    
    /* Section headers */
    .section-header {
        color: #4ECDC4;
        font-size: 1.5rem;
        font-weight: 700;
        border-bottom: 2px solid rgba(78, 205, 196, 0.3);
        padding-bottom: 10px;
        margin-top: 30px;
    }
    
    /* Insight box */
    .insight-box {
        background: linear-gradient(135deg, rgba(255, 107, 107, 0.1), rgba(78, 205, 196, 0.1));
        border-left: 4px solid #FF6B6B;
        border-radius: 0 12px 12px 0;
        padding: 15px 20px;
        margin: 10px 0;
        color: #e0e0e0;
    }
    
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# ==================== DATA LOADING ====================
@st.cache_data
def load_data():
    """Load data dari database SQLite3."""
    conn = sqlite3.connect(DB_FILE)
    query = """
        SELECT r.id, r.nama, r.status_mahasiswa, r.prodi, r.umur, 
               r.jenis_kelamin, r.frekuensi_penggunaan, r.keperluan, r.pernah_kendala,
               j.*
        FROM responden r
        JOIN jawaban_kuesioner j ON r.id = j.responden_id
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    # Hapus kolom duplikat
    df = df.loc[:, ~df.columns.duplicated()]
    return df


# ==================== SIDEBAR ====================
def render_sidebar(df):
    """Render sidebar dengan filter interaktif."""
    st.sidebar.markdown("## 🎛️ Filter Data")
    st.sidebar.markdown("---")
    
    # Filter Jenis Kelamin
    jk_options = ['Semua'] + sorted(df['jenis_kelamin'].unique().tolist())
    selected_jk = st.sidebar.selectbox("👤 Jenis Kelamin", jk_options)
    
    # Filter Prodi
    prodi_options = ['Semua'] + sorted(df['prodi'].unique().tolist())
    selected_prodi = st.sidebar.selectbox("🎓 Program Studi", prodi_options)
    
    # Filter Umur
    umur_options = ['Semua'] + sorted(df['umur'].unique().tolist())
    selected_umur = st.sidebar.selectbox("📅 Kelompok Umur", umur_options)
    
    # Filter Frekuensi
    freq_options = ['Semua'] + sorted(df['frekuensi_penggunaan'].unique().tolist())
    selected_freq = st.sidebar.selectbox("📱 Frekuensi Penggunaan", freq_options)
    
    # Filter Kendala
    kendala_options = ['Semua'] + sorted(df['pernah_kendala'].unique().tolist())
    selected_kendala = st.sidebar.selectbox("⚠️ Pernah Kendala", kendala_options)
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📋 Info Proyek")
    st.sidebar.info(
        "**PDLR 3 & 4**\n\n"
        "Survei Pengalaman Mahasiswa dalam Menggunakan SIAKAD UNJ\n\n"
        "📊 Data: Google Form Survey\n"
        "🔧 Tools: Python, SQLite3, Streamlit"
    )
    
    # Apply filters
    df_filtered = df.copy()
    if selected_jk != 'Semua':
        df_filtered = df_filtered[df_filtered['jenis_kelamin'] == selected_jk]
    if selected_prodi != 'Semua':
        df_filtered = df_filtered[df_filtered['prodi'] == selected_prodi]
    if selected_umur != 'Semua':
        df_filtered = df_filtered[df_filtered['umur'] == selected_umur]
    if selected_freq != 'Semua':
        df_filtered = df_filtered[df_filtered['frekuensi_penggunaan'] == selected_freq]
    if selected_kendala != 'Semua':
        df_filtered = df_filtered[df_filtered['pernah_kendala'] == selected_kendala]
    
    return df_filtered


# ==================== HALAMAN: OVERVIEW ====================
def render_overview(df):
    """Render halaman overview dengan KPI cards."""
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>📊 Dashboard Survei SIAKAD UNJ</h1>
        <p>Analisis Pengalaman Mahasiswa dalam Menggunakan Sistem Informasi Akademik</p>
    </div>
    """, unsafe_allow_html=True)
    
    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total Responden</div>
            <div class="metric-value">{len(df)}</div>
            <div class="metric-label">Mahasiswa</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Rata-rata skor keseluruhan
    likert_cols = [c for c in LABEL_KUESIONER.keys() if c in df.columns]
    avg_score = df[likert_cols].mean().mean() if likert_cols else 0
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Rata-rata Skor</div>
            <div class="metric-value">{avg_score:.2f}</div>
            <div class="metric-label">Dari Skala 5</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Persentase pernah kendala
    pernah = len(df[df['pernah_kendala'] == 'Pernah']) if 'pernah_kendala' in df.columns else 0
    pct_kendala = (pernah / len(df) * 100) if len(df) > 0 else 0
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Pernah Kendala</div>
            <div class="metric-value">{pct_kendala:.0f}%</div>
            <div class="metric-label">Responden</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Skor performa (tertinggi masalah)
    performa_cols = [c for c in KATEGORI['Performa Sistem'] if c in df.columns]
    avg_performa = df[performa_cols].mean().mean() if performa_cols else 0
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Skor Performa</div>
            <div class="metric-value">{avg_performa:.2f}</div>
            <div class="metric-label">Masalah Teknis</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # --- Ringkasan Distribusi ---
    st.markdown('<div class="section-header">📋 Ringkasan Distribusi Responden</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Pie chart jenis kelamin
        jk_counts = df['jenis_kelamin'].value_counts()
        fig_jk = px.pie(
            values=jk_counts.values,
            names=jk_counts.index,
            title="Distribusi Jenis Kelamin",
            color_discrete_sequence=['#FF6B9E', '#45B7D1', '#4ECDC4'],
            hole=0.4
        )
        fig_jk.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#e0e0e0',
            title_font_size=16,
            title_font_color='#4ECDC4',
        )
        fig_jk.update_traces(textposition='inside', textinfo='percent+label',
                            textfont_size=13)
        st.plotly_chart(fig_jk, use_container_width=True)
    
    with col2:
        # Pie chart frekuensi penggunaan
        freq_counts = df['frekuensi_penggunaan'].value_counts()
        fig_freq = px.pie(
            values=freq_counts.values,
            names=freq_counts.index,
            title="Frekuensi Penggunaan SIAKAD",
            color_discrete_sequence=['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFEAA7', '#DDA0DD'],
            hole=0.4
        )
        fig_freq.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#e0e0e0',
            title_font_size=16,
            title_font_color='#4ECDC4',
        )
        fig_freq.update_traces(textposition='inside', textinfo='percent+label',
                              textfont_size=12)
        st.plotly_chart(fig_freq, use_container_width=True)
    
    # Pie chart kendala
    col1, col2 = st.columns(2)
    
    with col1:
        kendala_counts = df['pernah_kendala'].value_counts()
        fig_kendala = px.pie(
            values=kendala_counts.values,
            names=kendala_counts.index,
            title="Pernah Mengalami Kendala?",
            color_discrete_sequence=['#FF6B6B', '#4ECDC4'],
            hole=0.4
        )
        fig_kendala.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#e0e0e0',
            title_font_size=16,
            title_font_color='#4ECDC4',
        )
        fig_kendala.update_traces(textposition='inside', textinfo='percent+label',
                                 textfont_size=14)
        st.plotly_chart(fig_kendala, use_container_width=True)
    
    with col2:
        # Bar chart umur
        umur_counts = df['umur'].value_counts()
        fig_umur = px.bar(
            x=umur_counts.index,
            y=umur_counts.values,
            title="Distribusi Kelompok Umur",
            color=umur_counts.index,
            color_discrete_sequence=['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFEAA7'],
        )
        fig_umur.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#e0e0e0',
            title_font_size=16,
            title_font_color='#4ECDC4',
            xaxis_title="Kelompok Umur",
            yaxis_title="Jumlah Responden",
            showlegend=False,
        )
        st.plotly_chart(fig_umur, use_container_width=True)


# ==================== HALAMAN: VISUALISASI ====================
def render_visualisasi(df):
    """Render halaman visualisasi grafik interaktif."""
    
    st.markdown('<div class="section-header">📈 Analisis Skor Kuesioner</div>', unsafe_allow_html=True)
    
    # --- Bar Chart: Rata-rata per Kategori ---
    st.markdown("#### Rata-rata Skor per Kategori")
    
    kategori_data = []
    for kat, cols in KATEGORI.items():
        existing = [c for c in cols if c in df.columns]
        if existing:
            avg = df[existing].mean().mean()
            kategori_data.append({'Kategori': kat, 'Rata-rata': round(avg, 2), 'Warna': WARNA_KATEGORI[kat]})
    
    df_kat = pd.DataFrame(kategori_data)
    
    fig_kat = px.bar(
        df_kat, x='Kategori', y='Rata-rata',
        color='Kategori',
        color_discrete_map=WARNA_KATEGORI,
        text='Rata-rata',
        title="Rata-rata Skor Likert per Kategori"
    )
    fig_kat.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#e0e0e0',
        title_font_color='#4ECDC4',
        yaxis_range=[0, 5.5],
        showlegend=False,
        yaxis_title="Skor (1-5)",
    )
    fig_kat.update_traces(textposition='outside', textfont_size=14)
    fig_kat.add_hline(y=3, line_dash="dash", line_color="gray",
                      annotation_text="Netral (3)", annotation_position="bottom right")
    st.plotly_chart(fig_kat, use_container_width=True)
    
    # --- Bar Chart: Detail per Pertanyaan ---
    st.markdown("#### Detail Skor per Pertanyaan")
    
    detail_data = []
    for col, label in LABEL_KUESIONER.items():
        if col in df.columns:
            avg = df[col].mean()
            # Tentukan kategori
            kat_label = 'Lainnya'
            for kat, kat_cols in KATEGORI.items():
                if col in kat_cols:
                    kat_label = kat
                    break
            detail_data.append({'Pertanyaan': label, 'Rata-rata': round(avg, 2), 'Kategori': kat_label})
    
    df_detail = pd.DataFrame(detail_data)
    
    fig_detail = px.bar(
        df_detail, y='Pertanyaan', x='Rata-rata',
        color='Kategori',
        color_discrete_map=WARNA_KATEGORI,
        orientation='h',
        text='Rata-rata',
        title="Rata-rata Skor per Pertanyaan Kuesioner"
    )
    fig_detail.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#e0e0e0',
        title_font_color='#4ECDC4',
        xaxis_range=[0, 5.5],
        height=600,
        xaxis_title="Skor (1-5)",
        yaxis_title="",
    )
    fig_detail.update_traces(textposition='outside', textfont_size=11)
    fig_detail.add_vline(x=3, line_dash="dash", line_color="gray")
    st.plotly_chart(fig_detail, use_container_width=True)
    
    # --- Scatter Plot ---
    st.markdown("#### Korelasi Performa Sistem vs Dampak Emosional")
    
    performa_cols = [c for c in KATEGORI['Performa Sistem'] if c in df.columns]
    emosi_cols = [c for c in KATEGORI['Dampak Emosional'] if c in df.columns]
    
    df_scatter = df.copy()
    df_scatter['Skor Performa'] = df_scatter[performa_cols].mean(axis=1).round(2)
    df_scatter['Skor Emosional'] = df_scatter[emosi_cols].mean(axis=1).round(2)
    
    fig_scatter = px.scatter(
        df_scatter, x='Skor Performa', y='Skor Emosional',
        color='jenis_kelamin',
        color_discrete_map={'Laki-laki': '#45B7D1', 'Perempuan': '#FF6B9E'},
        title="Korelasi Performa Sistem vs Dampak Emosional",
        trendline="ols",
        hover_data=['nama', 'prodi', 'umur'],
        size_max=12,
    )
    fig_scatter.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#e0e0e0',
        title_font_color='#4ECDC4',
        xaxis_title="Rata-rata Skor Performa Sistem",
        yaxis_title="Rata-rata Skor Dampak Emosional",
    )
    fig_scatter.update_traces(marker=dict(size=10, opacity=0.7, line=dict(width=1, color='white')))
    
    # Hitung korelasi
    corr = df_scatter['Skor Performa'].corr(df_scatter['Skor Emosional'])
    fig_scatter.add_annotation(
        x=0.05, y=0.95, xref="paper", yref="paper",
        text=f"Korelasi (r): {corr:.3f}",
        showarrow=False,
        font=dict(size=14, color="#FFEAA7"),
        bgcolor="rgba(0,0,0,0.5)",
        bordercolor="#4ECDC4",
        borderwidth=1,
        borderpad=8,
    )
    st.plotly_chart(fig_scatter, use_container_width=True)
    
    # --- Perbandingan Gender ---
    st.markdown("#### Perbandingan Skor berdasarkan Jenis Kelamin")
    
    gender_data = []
    for jk in df['jenis_kelamin'].unique():
        df_jk = df[df['jenis_kelamin'] == jk]
        for kat, cols in KATEGORI.items():
            existing = [c for c in cols if c in df.columns]
            if existing:
                avg = df_jk[existing].mean().mean()
                gender_data.append({'Jenis Kelamin': jk, 'Kategori': kat, 'Rata-rata': round(avg, 2)})
    
    df_gender = pd.DataFrame(gender_data)
    
    fig_gender = px.bar(
        df_gender, x='Kategori', y='Rata-rata',
        color='Jenis Kelamin',
        barmode='group',
        color_discrete_map={'Laki-laki': '#45B7D1', 'Perempuan': '#FF6B9E'},
        text='Rata-rata',
        title="Perbandingan Skor per Kategori berdasarkan Jenis Kelamin"
    )
    fig_gender.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#e0e0e0',
        title_font_color='#4ECDC4',
        yaxis_range=[0, 5.5],
        yaxis_title="Skor (1-5)",
    )
    fig_gender.update_traces(textposition='outside', textfont_size=12)
    st.plotly_chart(fig_gender, use_container_width=True)
    
    # --- Heatmap Korelasi ---
    st.markdown("#### Matriks Korelasi Antar Pertanyaan")
    
    likert_cols = [c for c in LABEL_KUESIONER.keys() if c in df.columns]
    labels_display = [LABEL_KUESIONER[c] for c in likert_cols]
    
    corr_matrix = df[likert_cols].corr()
    
    fig_heatmap = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=labels_display,
        y=labels_display,
        colorscale='RdBu_r',
        zmid=0,
        zmin=-1, zmax=1,
        text=np.round(corr_matrix.values, 2),
        texttemplate='%{text}',
        textfont={"size": 8},
        hovertemplate='%{x} vs %{y}<br>Korelasi: %{z:.3f}<extra></extra>',
    ))
    fig_heatmap.update_layout(
        title="Matriks Korelasi Antar Pertanyaan Kuesioner",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#e0e0e0',
        title_font_color='#4ECDC4',
        height=700,
        xaxis_tickangle=45,
    )
    st.plotly_chart(fig_heatmap, use_container_width=True)


# ==================== HALAMAN: DATA EXPLORER ====================
def render_data_explorer(df):
    """Render tabel data interaktif."""
    
    st.markdown('<div class="section-header">🗄️ Data Explorer</div>', unsafe_allow_html=True)
    
    st.markdown(f"Menampilkan **{len(df)}** responden (setelah filter)")
    
    # Pilih kolom yang ditampilkan
    all_cols = df.columns.tolist()
    default_cols = ['nama', 'prodi', 'umur', 'jenis_kelamin', 'frekuensi_penggunaan', 'pernah_kendala']
    
    selected_cols = st.multiselect(
        "Pilih kolom yang ditampilkan:",
        options=all_cols,
        default=[c for c in default_cols if c in all_cols]
    )
    
    if selected_cols:
        # Sorting
        sort_col = st.selectbox("Urutkan berdasarkan:", selected_cols)
        sort_order = st.radio("Urutan:", ['Ascending', 'Descending'], horizontal=True)
        
        df_display = df[selected_cols].sort_values(
            by=sort_col,
            ascending=(sort_order == 'Ascending')
        ).reset_index(drop=True)
        
        st.dataframe(df_display, use_container_width=True, height=500)
        
        # Download button
        csv = df_display.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="📥 Download Data (CSV)",
            data=csv,
            file_name="siakad_survey_filtered.csv",
            mime="text/csv",
        )
    else:
        st.warning("Pilih minimal 1 kolom untuk ditampilkan.")
    
    # Statistik deskriptif
    st.markdown("#### 📊 Statistik Deskriptif")
    
    likert_cols = [c for c in LABEL_KUESIONER.keys() if c in df.columns]
    if likert_cols:
        stats = df[likert_cols].describe().round(2)
        stats.index = ['Jumlah', 'Rata-rata', 'Std Dev', 'Min', '25%', 'Median', '75%', 'Max']
        
        # Rename columns to readable labels
        stats.columns = [LABEL_KUESIONER.get(c, c) for c in stats.columns]
        
        st.dataframe(stats, use_container_width=True)


# ==================== HALAMAN: KESIMPULAN ====================
def render_kesimpulan(df):
    """Render halaman kesimpulan dan data storytelling."""
    
    st.markdown('<div class="section-header">📝 Kesimpulan & Data Storytelling</div>', unsafe_allow_html=True)
    
    # Hitung metrik
    likert_cols = [c for c in LABEL_KUESIONER.keys() if c in df.columns]
    avg_all = df[likert_cols].mean().mean() if likert_cols else 0
    
    performa_cols = [c for c in KATEGORI['Performa Sistem'] if c in df.columns]
    uiux_cols = [c for c in KATEGORI['UI/UX (Antarmuka)'] if c in df.columns]
    emosi_cols = [c for c in KATEGORI['Dampak Emosional'] if c in df.columns]
    perilaku_cols = [c for c in KATEGORI['Dampak Perilaku'] if c in df.columns]
    
    avg_performa = df[performa_cols].mean().mean() if performa_cols else 0
    avg_uiux = df[uiux_cols].mean().mean() if uiux_cols else 0
    avg_emosi = df[emosi_cols].mean().mean() if emosi_cols else 0
    avg_perilaku = df[perilaku_cols].mean().mean() if perilaku_cols else 0
    
    # Item tertinggi & terendah
    item_means = {LABEL_KUESIONER[c]: df[c].mean() for c in likert_cols}
    highest_item = max(item_means, key=item_means.get)
    lowest_item = min(item_means, key=item_means.get)
    
    pernah = len(df[df['pernah_kendala'] == 'Pernah']) if 'pernah_kendala' in df.columns else 0
    pct_kendala = (pernah / len(df) * 100) if len(df) > 0 else 0
    
    # Storytelling
    st.markdown(f"""
    <div class="insight-box">
        <h4>🔍 Temuan Utama</h4>
        <p>Berdasarkan analisis data survei terhadap <strong>{len(df)} responden</strong> mahasiswa UNJ, 
        ditemukan bahwa rata-rata skor keseluruhan kuesioner adalah <strong>{avg_all:.2f} dari 5</strong>, 
        yang mengindikasikan bahwa sebagian besar mahasiswa <strong>{'mengalami masalah signifikan' if avg_all > 3 else 'cukup puas'}</strong> 
        dengan SIAKAD UNJ.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="insight-box">
        <h4>⚡ Performa Sistem</h4>
        <p>Kategori <strong>Performa Sistem</strong> mendapat skor rata-rata <strong>{avg_performa:.2f}</strong>. 
        Hal ini menunjukkan bahwa masalah teknis seperti loading lama, error, dan gangguan saat jam sibuk 
        {'menjadi keluhan utama mahasiswa' if avg_performa > 3.5 else 'masih perlu perhatian'}. 
        Sebanyak <strong>{pct_kendala:.0f}%</strong> responden menyatakan pernah mengalami kendala saat menggunakan SIAKAD.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="insight-box">
        <h4>🎨 Antarmuka (UI/UX)</h4>
        <p>Dari segi antarmuka, skor rata-rata adalah <strong>{avg_uiux:.2f}</strong>. 
        {'Banyak mahasiswa merasa tampilan menu membingungkan dan kesulitan menemukan informasi yang dibutuhkan.' if avg_uiux > 3 else 'Sebagian besar mahasiswa cukup memahami navigasi SIAKAD.'} 
        Aspek yang paling bermasalah adalah menu yang terasa tidak terstruktur dengan baik.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="insight-box">
        <h4>😤 Dampak Emosional</h4>
        <p>Kategori <strong>Dampak Emosional</strong> memiliki skor <strong>{avg_emosi:.2f}</strong>, 
        yang merupakan {'skor tertinggi' if avg_emosi >= max(avg_performa, avg_uiux, avg_perilaku) else 'skor signifikan'} 
        di antara semua kategori. Item <strong>"{highest_item}"</strong> mendapat skor tertinggi 
        ({item_means[highest_item]:.2f}), menunjukkan bahwa masalah SIAKAD berdampak kuat terhadap 
        {'kenyamanan emosional' if avg_emosi > 3.5 else 'perasaan'} mahasiswa.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="insight-box">
        <h4>📋 Dampak Perilaku</h4>
        <p>Dari segi perilaku, skor rata-rata <strong>{avg_perilaku:.2f}</strong> menunjukkan bahwa 
        mahasiswa {'cenderung menggunakan SIAKAD hanya karena kewajiban, bukan kenyamanan' if avg_perilaku > 3 else 'masih bertahan menggunakan SIAKAD meski ada keluhan'}. 
        Item terendah adalah <strong>"{lowest_item}"</strong> ({item_means[lowest_item]:.2f}).</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Rekomendasi
    st.markdown('<div class="section-header">💡 Rekomendasi</div>', unsafe_allow_html=True)
    
    st.markdown("""
    Berdasarkan hasil analisis data, berikut rekomendasi yang dapat diberikan:
    
    1. **🔧 Perbaikan Infrastruktur Server** — Tingkatkan kapasitas server SIAKAD terutama saat jam sibuk 
       (pengisian KRS, pembayaran UKT) untuk mengurangi loading lama dan error.
    
    2. **🎨 Redesign Antarmuka (UI/UX)** — Sederhanakan navigasi menu dan perbaiki struktur informasi 
       agar mahasiswa lebih mudah menemukan fitur yang dibutuhkan.
    
    3. **📱 Optimasi Mobile** — Pastikan SIAKAD dapat diakses dengan baik melalui perangkat mobile, 
       mengingat mayoritas mahasiswa mengakses via smartphone.
    
    4. **📞 Peningkatan Support** — Sediakan helpdesk atau FAQ yang mudah diakses untuk membantu 
       mahasiswa yang mengalami kendala teknis.
    
    5. **🔄 Monitoring Real-time** — Implementasikan sistem monitoring untuk mendeteksi dan 
       menangani masalah teknis sebelum berdampak luas ke pengguna.
    """)
    
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #a0a0c0; padding: 20px;">
        <p>📊 <strong>Dashboard PDLR 3 & 4</strong> — Survei Pengalaman Mahasiswa SIAKAD UNJ</p>
        <p>Dibuat menggunakan Python, SQLite3, Pandas, Plotly & Streamlit</p>
    </div>
    """, unsafe_allow_html=True)


# ==================== MAIN APP ====================
def main():
    """Main application."""
    
    # Load data
    df = load_data()
    
    # Sidebar filters
    df_filtered = render_sidebar(df)
    
    # Navigation tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Overview",
        "📈 Visualisasi",
        "🗄️ Data Explorer",
        "📝 Kesimpulan"
    ])
    
    with tab1:
        render_overview(df_filtered)
    
    with tab2:
        render_visualisasi(df_filtered)
    
    with tab3:
        render_data_explorer(df_filtered)
    
    with tab4:
        render_kesimpulan(df_filtered)


if __name__ == "__main__":
    main()
