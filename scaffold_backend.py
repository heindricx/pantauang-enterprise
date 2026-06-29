import os

backend_dir = r"D:\satdat 2026\sec\pantauang-enterprise\backend"
dirs = [
    "app",
    "app/api",
    "app/api/endpoints",
    "app/core",
    "app/db",
    "app/models",
    "app/schemas",
    "app/services",
    "app/worker",
    "tests"
]

for d in dirs:
    os.makedirs(os.path.join(backend_dir, d), exist_ok=True)
    init_file = os.path.join(backend_dir, d, "__init__.py")
    with open(init_file, "w") as f:
        pass

main_py = os.path.join(backend_dir, "main.py")
with open(main_py, "w") as f:
    f.write('''from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import dashboard, procurement, anomalies, risk_map, ml

app = FastAPI(
    title="PantaUang Kita Enterprise API",
    version="1.0.0",
    description="Backend API for National Procurement Analytics"
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
    return {"message": "Welcome to PantaUang Kita API"}

# Include routers here
# app.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])
''')

req_txt = os.path.join(backend_dir, "requirements.txt")
with open(req_txt, "w") as f:
    f.write('''fastapi
uvicorn[standard]
sqlalchemy
alembic
pydantic
pydantic-settings
pymysql
cryptography
celery
redis
lightgbm
pandas
numpy
scikit-learn
pytest
locust
''')

print("Backend scaffolded successfully.")
