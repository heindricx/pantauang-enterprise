import os

backend_dir = r"D:\satdat 2026\sec\pantauang-enterprise\backend"

dashboard_py = os.path.join(backend_dir, "app/api/endpoints/dashboard.py")
with open(dashboard_py, "w") as f:
    f.write('''from fastapi import APIRouter, Depends
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
''')

procurement_py = os.path.join(backend_dir, "app/api/endpoints/procurement.py")
with open(procurement_py, "w") as f:
    f.write('''from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db.session import SessionLocal
from typing import Optional

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def get_procurements(
    limit: int = 50, 
    offset: int = 0, 
    risiko: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = "SELECT id, agenda, lembaga, satker, provinsi, kota, metode, jenis, pagu, p10, p90, fraud_value, skor_risiko, kategori_risiko FROM procurement_anomalies"
    
    params = {}
    if risiko:
        query += " WHERE kategori_risiko = :risiko"
        params["risiko"] = risiko
        
    query += " ORDER BY skor_risiko DESC LIMIT :limit OFFSET :offset"
    params["limit"] = limit
    params["offset"] = offset
    
    result = db.execute(text(query), params).fetchall()
    
    data = []
    for row in result:
        data.append(dict(row._mapping))
        
    return {"data": data}
''')

# Update main.py to include routers
main_py = os.path.join(backend_dir, "main.py")
with open(main_py, "r") as f:
    content = f.read()

content = content.replace(
    '# app.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])',
    'app.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])\napp.include_router(procurement.router, prefix="/procurement", tags=["Procurement"])'
)

with open(main_py, "w") as f:
    f.write(content)

print("Backend API endpoints created successfully!")
