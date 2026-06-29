from pydantic import BaseModel
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
