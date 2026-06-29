from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db.session import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/metrics")
def get_dashboard_metrics(db: Session = Depends(get_db)):
    # Using the existing procurement_anomalies table in test db
    total_anggaran_query = db.execute(text("SELECT SUM(pagu) FROM procurement_anomalies")).scalar()
    total_paket_query = db.execute(text("SELECT COUNT(*) FROM procurement_anomalies")).scalar()
    risiko_tinggi_query = db.execute(text("SELECT COUNT(*) FROM procurement_anomalies WHERE kategori_risiko='Tinggi'")).scalar()
    potensi_anomali_query = db.execute(text("SELECT SUM(fraud_value) FROM procurement_anomalies")).scalar()
    
    return {
        "total_anggaran": float(total_anggaran_query or 0),
        "total_paket": total_paket_query or 0,
        "risiko_tinggi": risiko_tinggi_query or 0,
        "coverage_analisis": 1.0,  # 100% covered based on DB
        "estimasi_potensi_anomali": float(potensi_anomali_query or 0)
    }
