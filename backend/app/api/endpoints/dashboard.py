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
    
    # Chart 1: Risk Distribution
    risk_dist = db.execute(text("SELECT kategori_risiko, COUNT(*) as count FROM procurement_anomalies GROUP BY kategori_risiko")).fetchall()
    distribution = {row[0]: row[1] for row in risk_dist}
    
    # Chart 2: Budget Trend
    trend_data = db.execute(text("SELECT bulan_pemilihan, SUM(pagu) as pagu, SUM(p90) as p90 FROM procurement_anomalies GROUP BY bulan_pemilihan ORDER BY bulan_pemilihan")).fetchall()
    
    return {
        "total_anggaran": float(total_anggaran_query or 0),
        "total_paket": total_paket_query or 0,
        "risiko_tinggi": risiko_tinggi_query or 0,
        "coverage_analisis": 1.0,
        "estimasi_potensi_anomali": float(potensi_anomali_query or 0),
        "risk_distribution": [
            {"value": distribution.get("Tinggi", 0), "name": "Tinggi", "itemStyle": {"color": "#F28A6A"}},
            {"value": distribution.get("Sedang", 0), "name": "Sedang", "itemStyle": {"color": "#FF7A3D"}},
            {"value": distribution.get("Rendah", 0), "name": "Rendah", "itemStyle": {"color": "#52C7D8"}},
            {"value": distribution.get("Belum Terukur", 0), "name": "Belum Terukur", "itemStyle": {"color": "#E2E8F0"}},
        ],
        "budget_trend": {
            "months": [f"Bulan {row[0]}" for row in trend_data],
            "pagu": [float(row[1] or 0) for row in trend_data],
            "p90": [float(row[2] or 0) for row in trend_data]
        }
    }
