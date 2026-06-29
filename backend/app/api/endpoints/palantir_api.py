from fastapi import APIRouter, Depends
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
