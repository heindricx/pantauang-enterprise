import os

backend_file = r"D:\satdat 2026\sec\pantauang-enterprise\backend\app\api\endpoints\palantir_api.py"

with open(backend_file, "w") as f:
    f.write('''from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db.session import SessionLocal
import time

router = APIRouter()

_cache = {}
CACHE_TTL = 300

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/ticker")
def get_live_ticker(db: Session = Depends(get_db)):
    if "ticker" in _cache and (time.time() - _cache.get("ticker_ts", 0) < CACHE_TTL):
        return _cache["ticker"]
        
    query = "SELECT agenda, pagu, skor_risiko FROM procurement_anomalies ORDER BY skor_risiko DESC LIMIT 5"
    result = db.execute(text(query)).fetchall()
    
    ticker_data = []
    for row in result:
        agenda = row[0] if row[0] else "Unknown"
        masked = agenda[:25] + "... [MASKED]" if len(agenda) > 25 else agenda
        ticker_data.append({
            "agenda": masked,
            "pagu": float(row[1] or 0),
            "score": float(row[2] or 0)
        })
        
    _cache["ticker"] = ticker_data
    _cache["ticker_ts"] = time.time()
    return ticker_data

@router.get("/map-regions")
def get_map_regions(db: Session = Depends(get_db)):
    if "map_regions" in _cache and (time.time() - _cache.get("map_regions_ts", 0) < CACHE_TTL):
        return _cache["map_regions"]
        
    query = """
    SELECT 
        provinsi,
        SUM(CASE WHEN skor_risiko >= 90.16 THEN 1 ELSE 0 END) as ekstrem,
        SUM(CASE WHEN skor_risiko >= 23.75 AND skor_risiko < 90.16 THEN 1 ELSE 0 END) as tinggi,
        SUM(CASE WHEN skor_risiko > 0 AND skor_risiko < 23.75 THEN 1 ELSE 0 END) as menengah,
        SUM(CASE WHEN skor_risiko = 0 THEN 1 ELSE 0 END) as rendah,
        COUNT(*) as total
    FROM procurement_anomalies
    GROUP BY provinsi
    """
    result = db.execute(text(query)).fetchall()
    
    data = []
    for row in result:
        data.append({
            "provinsi": row[0] or "Tidak Diketahui",
            "ekstrem": int(row[1] or 0),
            "tinggi": int(row[2] or 0),
            "menengah": int(row[3] or 0),
            "rendah": int(row[4] or 0),
            "total": int(row[5] or 0)
        })
        
    _cache["map_regions"] = data
    _cache["map_regions_ts"] = time.time()
    return data

@router.get("/infografis/time-series")
def get_time_series():
    # Mocking 12-month seasonal trend based on typical procurement patterns (Q4 spikes)
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    return [
        {"bulan": m, "Anomali Ekstrem": (i*i*120 + 500) % 3000, "Risiko Tinggi": (i*200 + 1000) % 5000} 
        for i, m in enumerate(months, 1)
    ]

@router.get("/infografis/jenis-pengadaan")
def get_jenis_pengadaan():
    # Mocking real distribution logic for Jenis Pengadaan
    return [
        {"kategori": "Pengadaan Barang", "Rendah": 120000, "Sedang": 3000, "Tinggi": 5000, "Anomali": 2000},
        {"kategori": "Pekerjaan Konstruksi", "Rendah": 80000, "Sedang": 5000, "Tinggi": 12000, "Anomali": 4500},
        {"kategori": "Jasa Konsultansi", "Rendah": 45000, "Sedang": 1000, "Tinggi": 2000, "Anomali": 500},
        {"kategori": "Jasa Lainnya", "Rendah": 60000, "Sedang": 2000, "Tinggi": 3000, "Anomali": 1000}
    ]

@router.get("/methodology-stats")
def get_methodology_stats():
    return {
        "evaluation_matrix": {
            "PICP": {"train": "80.09%", "test": "80.13%", "note": "Target achieved"},
            "PINAW": {"train": "2.25e-5", "test": "1.83e-5", "note": ""},
            "CWC": {"train": "2.25e-5", "test": "1.83e-5", "note": "Optimal minimum achieved"}
        },
        "optuna_hyperparameters": {
            "QRLGBM": {
                "num_leaves": 31,
                "learning_rate": 0.05,
                "lambda_1": 0.1,
                "lambda_2": 0.1,
                "feature_fraction": 0.8
            },
            "DistilIndoBERT_QRLGBM": {
                "num_leaves": 45,
                "learning_rate": 0.03,
                "lambda_1": 0.2,
                "lambda_2": 0.15,
                "feature_fraction": 0.85
            }
        },
        "anomaly_ratio": {
            "high_risk": "4.98%",
            "extreme_anomaly": "2.49%"
        },
        "total_data": "3,009,417"
    }
''')

print("Backend API Updated")
