import os

BACKEND_DIR = r"D:\satdat 2026\sec\pantauang-enterprise\backend\app\api\endpoints"
FRONTEND_APP = r"D:\satdat 2026\sec\pantauang-enterprise\frontend\src\app"
FRONTEND_COMPONENTS = r"D:\satdat 2026\sec\pantauang-enterprise\frontend\src\components"

# ─── 1. BACKEND: Upgrade procurement.py to full pagination + multi-filter ───
with open(os.path.join(BACKEND_DIR, "procurement.py"), "w") as f:
    f.write('''from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db.session import SessionLocal
from typing import Optional, List

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def get_procurements(
    limit: int = Query(25, le=100),
    offset: int = 0,
    search: Optional[str] = None,
    risiko: Optional[str] = None,
    provinsi: Optional[str] = None,
    metode: Optional[str] = None,
    lembaga: Optional[str] = None,
    sort_by: Optional[str] = "skor_risiko",
    sort_dir: Optional[str] = "desc",
    db: Session = Depends(get_db)
):
    base = "FROM procurement_anomalies"
    where_clauses = []
    params = {}

    if search:
        where_clauses.append("(agenda LIKE :search OR id LIKE :search)")
        params["search"] = f"%{search}%"
    if risiko:
        where_clauses.append("kategori_risiko = :risiko")
        params["risiko"] = risiko
    if provinsi:
        where_clauses.append("provinsi = :provinsi")
        params["provinsi"] = provinsi
    if metode:
        where_clauses.append("metode = :metode")
        params["metode"] = metode
    if lembaga:
        where_clauses.append("lembaga LIKE :lembaga")
        params["lembaga"] = f"%{lembaga}%"

    where_sql = (" WHERE " + " AND ".join(where_clauses)) if where_clauses else ""

    # Safe sort column whitelist
    allowed_sort = {"skor_risiko", "pagu", "agenda", "provinsi"}
    sort_col = sort_by if sort_by in allowed_sort else "skor_risiko"
    direction = "DESC" if sort_dir == "desc" else "ASC"

    count_result = db.execute(text(f"SELECT COUNT(*) {base}{where_sql}"), params).fetchone()
    total_count = count_result[0] if count_result else 0

    query = f"""
        SELECT id, agenda, lembaga, satker, provinsi, kota, metode, jenis, pagu,
               p10, p90, fraud_value, skor_risiko, kategori_risiko
        {base}{where_sql}
        ORDER BY {sort_col} {direction}
        LIMIT :limit OFFSET :offset
    """
    params["limit"] = limit
    params["offset"] = offset

    result = db.execute(text(query), params).fetchall()
    data = [dict(row._mapping) for row in result]

    return {
        "data": data,
        "total": total_count,
        "page": (offset // limit) + 1,
        "page_size": limit,
        "total_pages": max(1, -(-total_count // limit))
    }

@router.get("/filters")
def get_filter_options(db: Session = Depends(get_db)):
    """Return distinct values for filter dropdowns"""
    def fetch_distinct(col):
        rows = db.execute(text(f"SELECT DISTINCT {col} FROM procurement_anomalies WHERE {col} IS NOT NULL ORDER BY {col} LIMIT 200")).fetchall()
        return [r[0] for r in rows]

    return {
        "kategori_risiko": ["Rendah", "Sedang", "Tinggi", "Anomali"],
        "provinsi": fetch_distinct("provinsi"),
        "metode": fetch_distinct("metode"),
    }
''')

print("Backend procurement.py upgraded")
