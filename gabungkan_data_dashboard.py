
import pandas as pd

# 1. Membaca data
df_hybrid = pd.read_csv(
    "outputs/hasil_hybrid_ai_testing_no_tvoc.csv"
)

df_severity = pd.read_csv(
    "notebooks/outputs/hasil_severity_scoring_4sensor.csv"
)

# 2. Memilih kolom Severity yang diperlukan
kolom_severity = [
    "id_monitoring_udara",
    "skor_severity_tanpa_barometer",
    "tingkat_severity_final"
]

df_severity_pilihan = df_severity[kolom_severity].copy()

# 3. Menggabungkan berdasarkan ID monitoring
df_dashboard = df_hybrid.merge(
    df_severity_pilihan,
    on="id_monitoring_udara",
    how="left"
)

# 4. Memberi kategori untuk data normal
df_dashboard["tingkat_severity_final"] = (
    df_dashboard["tingkat_severity_final"].fillna("Normal")
)

# 5. Mengisi skor Severity data normal dengan 0
df_dashboard["skor_severity_tanpa_barometer"] = (
    df_dashboard["skor_severity_tanpa_barometer"].fillna(0)
)

# 6. Menyimpan hasil
df_dashboard.to_csv(
    "outputs/data_dashboard.csv",
    index=False
)

# 7. Menampilkan ringkasan
print("TOTAL DATA:", len(df_dashboard))

print("\nKATEGORI HYBRID:")
print(df_dashboard["kategori_hybrid"].value_counts())

print("\nTINGKAT SEVERITY:")
print(df_dashboard["tingkat_severity_final"].value_counts())

print("\nJUMLAH ID DUPLIKAT:")
print(df_dashboard["id_monitoring_udara"].duplicated().sum())

print("\nFILE BERHASIL DISIMPAN:")
print("outputs/data_dashboard.csv")
