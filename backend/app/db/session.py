from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

engine = create_engine(
    settings.DATABASE_URI, 
    pool_pre_ping=True, 
    pool_recycle=3600,
    connect_args={"ssl": {"ssl_cert_reqs": "CERT_NONE"}}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
