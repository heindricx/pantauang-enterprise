import os
import shutil

backend_dir = r"D:\satdat 2026\sec\pantauang-enterprise\backend"

# 1. Update main.py to include new routes
main_py = os.path.join(backend_dir, "main.py")
with open(main_py, "w") as f:
    f.write('''from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import dashboard, procurement, palantir_api

app = FastAPI(
    title="PantaUang Kita Enterprise API",
    version="2.0.0",
    description="Palantir-Style Backend API for National Procurement Analytics"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to PantaUang Kita Mission Control API"}

app.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])
app.include_router(procurement.router, prefix="/procurement", tags=["Procurement"])
app.include_router(palantir_api.router, prefix="/api", tags=["Palantir Core"])
''')

# 2. Create palantir_api.py
palantir_api_py = os.path.join(backend_dir, "app/api/endpoints/palantir_api.py")
with open(palantir_api_py, "w") as f:
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
    
    # Secure string masking at backend
    ticker_data = []
    for row in result:
        agenda = row[0] if row[0] else "Unknown"
        # Masking: Keep first 25 chars, then [MASKED]
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
    if "map" in _cache and (time.time() - _cache.get("map_ts", 0) < CACHE_TTL):
        return _cache["map"]
        
    query = """
    SELECT provinsi, SUM(pagu) as total_budget, AVG(skor_risiko) as avg_risk, COUNT(*) as incident_count 
    FROM procurement_anomalies 
    WHERE kategori_risiko IN ('Tinggi', 'Ekstrem')
    GROUP BY provinsi 
    ORDER BY avg_risk DESC
    LIMIT 10
    """
    result = db.execute(text(query)).fetchall()
    
    data = []
    for row in result:
        data.append({
            "provinsi": row[0],
            "total_budget": float(row[1] or 0),
            "avg_risk": float(row[2] or 0),
            "incident_count": int(row[3] or 0)
        })
        
    _cache["map"] = data
    _cache["map_ts"] = time.time()
    return data

@router.get("/methodology-stats")
def get_methodology_stats():
    # Hardcoded technical transparency as per exact user spec
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

# Update dashboard metrics to include extreme anomalies
dashboard_py = os.path.join(backend_dir, "app/api/endpoints/dashboard.py")
with open(dashboard_py, "r") as f:
    code = f.read()

# I will just write a new dashboard.py since I need to add extreme anomalies logic precisely
with open(dashboard_py, "w") as f:
    f.write('''from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db.session import SessionLocal
import time

router = APIRouter()
_cache = {"metrics": None, "timestamp": 0}
CACHE_TTL = 300 

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/metrics")
def get_dashboard_metrics(db: Session = Depends(get_db)):
    current_time = time.time()
    if _cache["metrics"] and (current_time - _cache["timestamp"] < CACHE_TTL):
        return _cache["metrics"]

    total_anggaran = db.execute(text("SELECT SUM(pagu) FROM procurement_anomalies")).scalar()
    total_paket = db.execute(text("SELECT COUNT(*) FROM procurement_anomalies")).scalar()
    
    # In a real Palantir system, we use actual risk bands.
    # High Risk: 23.75 <= R < 90.16
    # Extreme Anomaly: R >= 90.16
    risiko_tinggi = db.execute(text("SELECT COUNT(*) FROM procurement_anomalies WHERE skor_risiko >= 23.75 AND skor_risiko < 90.16")).scalar()
    ekstrem = db.execute(text("SELECT COUNT(*) FROM procurement_anomalies WHERE skor_risiko >= 90.16")).scalar()
    
    result = {
        "total_anggaran": float(total_anggaran or 0),
        "total_paket": total_paket or 0,
        "risiko_tinggi": risiko_tinggi or 0,
        "ekstrem": ekstrem or 0,
        "anomaly_ratio": 7.47, # 4.98% + 2.49%
        "total_data_exact": 3009417
    }
    
    _cache["metrics"] = result
    _cache["timestamp"] = current_time
    return result
''')

print("Backend API Updated.")
