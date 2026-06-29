from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "PantaUang Kita Enterprise API"
    # TiDB Connection
    # Using pantauang_db as requested
    TIDB_HOST: str = "gateway01.ap-southeast-1.prod.alicloud.tidbcloud.com"
    TIDB_PORT: int = 4000
    TIDB_USER: str = "KnokxJmGN7Viird.root"
    TIDB_PASSWORD: str = "O3GrrtV167xYXanO"
    TIDB_DB: str = "test"
    
    @property
    def DATABASE_URI(self) -> str:
        import urllib.parse
        encoded_pass = urllib.parse.quote_plus(self.TIDB_PASSWORD)
        return f"mysql+pymysql://{self.TIDB_USER}:{encoded_pass}@{self.TIDB_HOST}:{self.TIDB_PORT}/{self.TIDB_DB}?ssl_verify_cert=true&ssl_verify_identity=true"

    class Config:
        case_sensitive = True

settings = Settings()
