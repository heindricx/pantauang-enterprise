from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
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
