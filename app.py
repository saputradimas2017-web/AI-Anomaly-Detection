
import streamlit as st
import pandas as pd

# =====================================================
# 1. KONFIGURASI HALAMAN
# =====================================================

st.set_page_config(
    page_title="Air Quality AI Dashboard",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# 2. CUSTOM CSS
# =====================================================

st.markdown("""
<style>

.stApp {
    background-color: #F4F7FB;
}

[data-testid="stHeader"] {
    background-color: transparent;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1500px;
}

h1, h2, h3 {
    color: #172B4D;
    font-weight: 700;
}

p {
    color: #526078;
}

[data-testid="stMetric"] {
    background-color: white;
    border: 1px solid #E5EAF2;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(20, 40, 80, 0.04);
}

[data-testid="stMetricLabel"] {
    color: #64748B;
    font-weight: 600;
}

[data-testid="stMetricValue"] {
    color: #172B4D;
    font-weight: 700;
}

[data-testid="stSidebar"] {
    background-color: #17243A;
}

[data-testid="stSidebar"] * {
    color: #FFFFFF;
}

[data-testid="stSidebar"] [data-baseweb="select"] * {
    color: #172B4D;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 12px;
}

.stTabs [data-baseweb="tab"] {
    height: 48px;
    background-color: white;
    border-radius: 8px;
    padding: 10px 20px;
}

.stTabs [aria-selected="true"] {
    background-color: #DBEAFE;
    color: #1D4ED8;
}

div[data-testid="stDataFrame"] {
    border: 1px solid #E5EAF2;
    border-radius: 10px;
}

.stDownloadButton button {
    background-color: #2563EB;
    color: white;
    border-radius: 8px;
    border: none;
}

.stDownloadButton button:hover {
    background-color: #1D4ED8;
    color: white;
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# 3. MEMBACA DATA
# =====================================================

@st.cache_data
def load_data():

    data = pd.read_csv("outputs/data_dashboard.csv")

    data["waktu_tercatat"] = pd.to_datetime(
        data["waktu_tercatat"],
        errors="coerce"
    )

    # Memastikan kolom numerik terbaca dengan benar
    kolom_numerik = [
        "suhu",
        "kelembaban",
        "pm10",
        "pm25",
        "barometer",
        "prediksi_if",
        "skor_severity_tanpa_barometer"
    ]

    for kolom in kolom_numerik:
        if kolom in data.columns:
            data[kolom] = pd.to_numeric(
                data[kolom],
                errors="coerce"
            )

    # Mengamankan pembacaan nilai boolean
    kolom_boolean = [
        "rule_based_anomaly",
        "ai_anomaly",
        "hybrid_anomaly"
    ]

    for kolom in kolom_boolean:
        data[kolom] = (
            data[kolom]
            .astype(str)
            .str.lower()
            .map({"true": True, "false": False})
            .fillna(False)
            .astype(bool)
        )

    return data


try:
    df = load_data()

except Exception as e:
    st.error(f"Gagal membaca data dashboard: {e}")
    st.stop()


if df.empty:
    st.warning("Data dashboard masih kosong.")
    st.stop()


# =====================================================
# 4. PERHITUNGAN STATISTIK
# =====================================================

total_data = len(df)

total_normal = (~df["hybrid_anomaly"]).sum()

total_anomali = df["hybrid_anomaly"].sum()

persentase_anomali = (
    total_anomali / total_data * 100
    if total_data > 0 else 0
)

severity = (
    df["tingkat_severity_final"]
    .value_counts()
)

waktu_terakhir = df["waktu_tercatat"].max()


# =====================================================
# 5. SIDEBAR
# =====================================================

with st.sidebar:

    st.markdown("# 🌐 AIR QUALITY AI")

    st.caption("ANOMALY DETECTION SYSTEM")

    st.divider()

    st.markdown("### Navigation")

    st.markdown("""
    Dashboard ini digunakan untuk memantau
    kualitas udara dan mendeteksi anomali
    menggunakan metode AI.
    """)

    st.divider()

    st.markdown("### Dataset Information")

    st.write(f"Total Data: **{total_data:,}**")

    if pd.notna(waktu_terakhir):
        st.write(
            "Data Terakhir:",
            waktu_terakhir.strftime("%d-%m-%Y %H:%M:%S")
        )

    st.divider()

    st.caption("AI Anomaly Detection Project")
    st.caption("Hybrid Rule-Based + Isolation Forest")


# =====================================================
# 6. HEADER DASHBOARD
# =====================================================

st.markdown(
    """
    <div style="
        background: linear-gradient(120deg, #172B4D, #2563EB);
        padding: 30px;
        border-radius: 16px;
        margin-bottom: 25px;
    ">
        <h1 style="color:white; margin:0;">
            Air Quality Monitoring
        </h1>
        <p style="color:#DBEAFE; margin-top:10px;">
            Dashboard Monitoring Kualitas Udara
            Berbasis Artificial Intelligence
        </p>
        <span style="
            background:#DBEAFE;
            color:#1D4ED8;
            padding:6px 12px;
            border-radius:20px;
            font-size:12px;
            font-weight:bold;
        ">
            HYBRID AI DETECTION SYSTEM
        </span>
    </div>
    """,
    unsafe_allow_html=True
)


# =====================================================
# 7. OVERVIEW STATISTIK
# =====================================================

st.subheader("Overview Monitoring")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Monitoring",
    f"{total_data:,}"
)

col2.metric(
    "Data Normal",
    f"{total_normal:,}"
)

col3.metric(
    "Data Anomali",
    f"{total_anomali:,}"
)

col4.metric(
    "Anomaly Rate",
    f"{persentase_anomali:.2f}%"
)

st.write("")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Severity Rendah",
    f"{severity.get('Rendah', 0):,}"
)

col2.metric(
    "Severity Sedang",
    f"{severity.get('Sedang', 0):,}"
)

col3.metric(
    "Severity Tinggi",
    f"{severity.get('Tinggi', 0):,}"
)


# =====================================================
# 8. TAB DASHBOARD
# =====================================================

tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Overview & Detection",
    "🌡️ Sensor Monitoring",
    "🕒 Riwayat Data",
    "🚨 Detail Anomali"
])


# =====================================================
# TAB 1 - OVERVIEW DAN DETECTION
# =====================================================

with tab1:

    st.subheader("Perbandingan Metode Deteksi")

    perbandingan = pd.DataFrame({
        "Metode": [
            "Rule-Based",
            "Isolation Forest",
            "Hybrid AI"
        ],

        "Normal": [
            (~df["rule_based_anomaly"]).sum(),
            (df["prediksi_if"] == 1).sum(),
            (~df["hybrid_anomaly"]).sum()
        ],

        "Anomali": [
            df["rule_based_anomaly"].sum(),
            (df["prediksi_if"] == -1).sum(),
            df["hybrid_anomaly"].sum()
        ]
    })

    col1, col2 = st.columns([1.5, 1])

    with col1:

        st.markdown("#### Hasil Deteksi")

        st.bar_chart(
            perbandingan.set_index("Metode")
        )

    with col2:

        st.markdown("#### Ringkasan Deteksi")

        st.dataframe(
            perbandingan,
            use_container_width=True,
            hide_index=True
        )

    st.divider()

    st.subheader("Distribusi Tingkat Severity")

    severity_data = (
        df[df["tingkat_severity_final"] != "Normal"]
        ["tingkat_severity_final"]
        .value_counts()
        .reindex(
            ["Rendah", "Sedang", "Tinggi"],
            fill_value=0
        )
    )

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("#### Jumlah Anomali")

        st.bar_chart(severity_data)

    with col2:

        st.markdown("#### Persentase Severity")

        total_severity = severity_data.sum()

        if total_severity > 0:

            tabel_severity = pd.DataFrame({
                "Tingkat Severity": severity_data.index,
                "Jumlah": severity_data.values,
                "Persentase (%)": (
                    severity_data.values /
                    total_severity * 100
                ).round(2)
            })

            st.dataframe(
                tabel_severity,
                use_container_width=True,
                hide_index=True
            )


# =====================================================
# TAB 2 - SENSOR MONITORING
# =====================================================

with tab2:

    st.subheader("Monitoring Nilai Sensor")

    df_sensor = df.dropna(
        subset=["waktu_tercatat"]
    ).sort_values("waktu_tercatat")

    daftar_sensor = {
        "Suhu": ("suhu", "°C"),
        "Kelembaban": ("kelembaban", "%"),
        "PM10": ("pm10", "µg/m³"),
        "PM2.5": ("pm25", "µg/m³"),
        "Barometer": ("barometer", "hPa")
    }

    pilihan_sensor = st.selectbox(
        "Pilih Sensor",
        list(daftar_sensor.keys())
    )

    nama_kolom, satuan = daftar_sensor[pilihan_sensor]

    jumlah_titik = st.select_slider(
        "Jumlah data yang ditampilkan",
        options=[100, 250, 500, 1000, 2000, 5000],
        value=1000
    )

    grafik_sensor = df_sensor[
        ["waktu_tercatat", nama_kolom]
    ].dropna().tail(jumlah_titik)

    st.markdown(f"#### Grafik {pilihan_sensor}")

    if not grafik_sensor.empty:

        st.line_chart(
            grafik_sensor.set_index("waktu_tercatat"),
            y=nama_kolom
        )

        nilai_min = grafik_sensor[nama_kolom].min()
        nilai_mean = grafik_sensor[nama_kolom].mean()
        nilai_max = grafik_sensor[nama_kolom].max()

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Nilai Minimum",
            f"{nilai_min:.2f} {satuan}"
        )

        col2.metric(
            "Nilai Rata-rata",
            f"{nilai_mean:.2f} {satuan}"
        )

        col3.metric(
            "Nilai Maksimum",
            f"{nilai_max:.2f} {satuan}"
        )

    else:
        st.info("Tidak ada data sensor yang tersedia.")


# =====================================================
# TAB 3 - RIWAYAT DATA
# =====================================================

with tab3:

    st.subheader("Riwayat Data Monitoring")

    if pd.notna(waktu_terakhir):

        rentang_waktu = st.radio(
            "Pilih rentang waktu",
            ["10 Menit Terakhir", "30 Menit Terakhir"],
            horizontal=True
        )

        menit = (
            10 if rentang_waktu == "10 Menit Terakhir"
            else 30
        )

        batas_waktu = (
            waktu_terakhir -
            pd.Timedelta(minutes=menit)
        )

        df_riwayat = df[
            (df["waktu_tercatat"] >= batas_waktu) &
            (df["waktu_tercatat"] <= waktu_terakhir)
        ].sort_values(
            "waktu_tercatat",
            ascending=False
        )

        st.caption(
            f"Periode: {batas_waktu} sampai {waktu_terakhir}"
        )

        st.metric(
            "Jumlah Data dalam Periode",
            f"{len(df_riwayat):,}"
        )

        kolom_riwayat = [
            "waktu_tercatat",
            "suhu",
            "kelembaban",
            "pm10",
            "pm25",
            "barometer",
            "kategori_hybrid",
            "tingkat_severity_final"
        ]

        st.dataframe(
            df_riwayat[kolom_riwayat],
            use_container_width=True,
            hide_index=True
        )

        st.download_button(
            "Download Riwayat CSV",
            data=df_riwayat[kolom_riwayat].to_csv(index=False),
            file_name="riwayat_monitoring.csv",
            mime="text/csv"
        )

    else:
        st.warning("Timestamp data tidak tersedia.")


# =====================================================
# TAB 4 - DETAIL ANOMALI
# =====================================================

with tab4:

    st.subheader("Detail Data Anomali")

    df_anomali = df[
        df["hybrid_anomaly"] == True
    ].copy()

    col1, col2 = st.columns(2)

    with col1:

        pilihan_severity = st.multiselect(
            "Filter Severity",
            ["Rendah", "Sedang", "Tinggi"],
            default=["Rendah", "Sedang", "Tinggi"]
        )

    with col2:

        daftar_metode = sorted(
            df_anomali["kategori_hybrid"]
            .dropna()
            .unique()
            .tolist()
        )

        pilihan_metode = st.multiselect(
            "Filter Metode Deteksi",
            daftar_metode,
            default=daftar_metode
        )

    df_anomali = df_anomali[
        df_anomali["tingkat_severity_final"].isin(
            pilihan_severity
        )
        &
        df_anomali["kategori_hybrid"].isin(
            pilihan_metode
        )
    ]

    df_anomali = df_anomali.sort_values(
        "waktu_tercatat",
        ascending=False
    )

    st.metric(
        "Total Anomali Sesuai Filter",
        f"{len(df_anomali):,}"
    )

    kolom_anomali = [
        "id_monitoring_udara",
        "waktu_tercatat",
        "suhu",
        "kelembaban",
        "pm10",
        "pm25",
        "barometer",
        "kategori_hybrid",
        "skor_severity_tanpa_barometer",
        "tingkat_severity_final"
    ]

    st.dataframe(
        df_anomali[kolom_anomali],
        use_container_width=True,
        hide_index=True
    )

    st.download_button(
        label="📥 Download Data Anomali CSV",
        data=df_anomali[kolom_anomali].to_csv(index=False),
        file_name="data_anomali_dashboard.csv",
        mime="text/csv"
    )


# =====================================================
# 9. FOOTER
# =====================================================

st.divider()

st.markdown(
    """
    <div style="text-align:center; padding:10px;">
        <p style="color:#64748B; font-size:13px;">
            AI Anomaly Detection System
            <br>
            Air Quality Monitoring Dashboard
            <br>
            Hybrid Rule-Based & Isolation Forest
        </p>
    </div>
    """,
    unsafe_allow_html=True
)
