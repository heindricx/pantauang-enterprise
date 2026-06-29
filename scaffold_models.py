import os

backend_dir = r"D:\satdat 2026\sec\pantauang-enterprise\backend"

db_base = os.path.join(backend_dir, "app/db/base.py")
with open(db_base, "w") as f:
    f.write('''from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass
''')

models_py = os.path.join(backend_dir, "app/models/procurement.py")
with open(models_py, "w") as f:
    f.write('''from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.db.base import Base
import datetime

class Agency(Base):
    __tablename__ = "agency"
    id = Column(Integer, primary_key=True, index=True)
    klpdId = Column(String(50), unique=True, index=True)
    nama = Column(String(255))
    jenis = Column(String(100))

class Vendor(Base):
    __tablename__ = "vendor"
    id = Column(Integer, primary_key=True, index=True)
    npwp = Column(String(50), unique=True, index=True)
    nama = Column(String(255))

class Procurement(Base):
    __tablename__ = "procurement"
    id = Column(Integer, primary_key=True, index=True)
    paketId = Column(String(50), unique=True, index=True)
    nama_paket = Column(Text)
    anggaran = Column(Float)
    tanggal = Column(DateTime, default=datetime.datetime.utcnow)
    
    agency_id = Column(Integer, ForeignKey("agency.id"))
    vendor_id = Column(Integer, ForeignKey("vendor.id"))
    
    agency = relationship("Agency")
    vendor = relationship("Vendor")
''')

schemas_py = os.path.join(backend_dir, "app/schemas/procurement.py")
with open(schemas_py, "w") as f:
    f.write('''from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ProcurementBase(BaseModel):
    paketId: str
    nama_paket: str
    anggaran: float
    tanggal: datetime

class ProcurementCreate(ProcurementBase):
    agency_id: Optional[int]
    vendor_id: Optional[int]

class ProcurementResponse(ProcurementBase):
    id: int
    agency_id: Optional[int]
    vendor_id: Optional[int]
    
    class Config:
        from_attributes = True
''')

print("Backend Models and Schemas scaffolded.")
