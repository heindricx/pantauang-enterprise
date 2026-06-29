from fastapi import APIRouter, Depends, Query
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
