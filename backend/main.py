from fastapi import FastAPI
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
