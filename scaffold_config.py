import os
import urllib.parse

backend_dir = r"D:\satdat 2026\sec\pantauang-enterprise\backend"

config_py = os.path.join(backend_dir, "app/core/config.py")
with open(config_py, "w") as f:
    f.write('''from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "PantaUang Kita Enterprise API"
    # TiDB Connection
    # Using pantauang_db as requested
    TIDB_HOST: str = "gateway01.ap-southeast-1.prod.alicloud.tidbcloud.com"
    TIDB_PORT: int = 4000
    TIDB_USER: str = "KnokxJmGN7Viird.root"
    TIDB_PASSWORD: str = "O3GrrtV167xYXanO"
    TIDB_DB: str = "pantauang_db"
    
    @property
    def DATABASE_URI(self) -> str:
        import urllib.parse
        encoded_pass = urllib.parse.quote_plus(self.TIDB_PASSWORD)
        return f"mysql+pymysql://{self.TIDB_USER}:{encoded_pass}@{self.TIDB_HOST}:{self.TIDB_PORT}/{self.TIDB_DB}?ssl_verify_cert=true&ssl_verify_identity=true"

    class Config:
        case_sensitive = True

settings = Settings()
''')

db_session_py = os.path.join(backend_dir, "app/db/session.py")
with open(db_session_py, "w") as f:
    f.write('''from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

engine = create_engine(
    settings.DATABASE_URI, 
    pool_pre_ping=True, 
    pool_recycle=3600,
    connect_args={"ssl": {"ssl_cert_reqs": "CERT_NONE"}}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
''')

print("Backend Config and Session scaffolded.")
