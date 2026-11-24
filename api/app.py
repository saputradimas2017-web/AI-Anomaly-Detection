
from flask import Flask, request, jsonify
import joblib
import pandas as pd
import numpy as np
from pathlib import Path

# Membuat aplikasi Flask
app = Flask(__name__)

# Menentukan lokasi model AI
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "isolation_forest_05.joblib"

# Memuat model Isolation Forest
model = joblib.load(MODEL_PATH)

# Urutan fitur harus sama dengan saat model dilatih
FITUR_SENSOR = [
    "suhu",
    "kelembaban",
    "pm10",
    "pm25",
    "barometer",
    "tvoc"
]


# Endpoint untuk memeriksa API
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "success",
        "message": "AI Sensor Anomaly Detection API aktif",
        "model": "Isolation Forest",
        "contamination": 0.05
    })


# Endpoint untuk melakukan prediksi
@app.route("/predict", methods=["POST"])
def predict():

    try:
        # Mengambil data JSON
        data = request.get_json(silent=True)

        if not isinstance(data, dict):
            return jsonify({
                "status": "error",
                "message": "Data JSON tidak valid"
            }), 400

        # Memastikan semua fitur tersedia
        fitur_hilang = [
            fitur for fitur in FITUR_SENSOR
            if fitur not in data
        ]

        if fitur_hilang:
            return jsonify({
                "status": "error",
                "message": "Ada data sensor yang belum diisi",
                "fitur_hilang": fitur_hilang
            }), 400

        # Mengambil dan memeriksa nilai sensor
        nilai_sensor = {}

        for fitur in FITUR_SENSOR:
            nilai = float(data[fitur])

            if not np.isfinite(nilai):
                raise ValueError(
                    f"Nilai {fitur} harus berupa angka yang valid"
                )

            nilai_sensor[fitur] = nilai

        # Mengubah data menjadi DataFrame
        data_sensor = pd.DataFrame(
            [nilai_sensor],
            columns=FITUR_SENSOR
        )

        # Melakukan prediksi
        hasil = model.predict(data_sensor)[0]

        # Menghitung skor anomali
        skor = model.decision_function(data_sensor)[0]

        # Mengubah hasil prediksi menjadi label
        status = "Normal" if hasil == 1 else "Anomali"

        return jsonify({
            "status": "success",
            "hasil_prediksi": int(hasil),
            "kategori": status,
            "skor_anomali": float(skor),
            "data_sensor": nilai_sensor
        })

    except (TypeError, ValueError, OverflowError) as error:
        return jsonify({
            "status": "error",
            "message": str(error)
        }), 400

    except Exception:
        app.logger.exception("Terjadi kesalahan saat prediksi")

        return jsonify({
            "status": "error",
            "message": "Terjadi kesalahan pada proses prediksi"
        }), 500


# Menjalankan server Flask
if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )
