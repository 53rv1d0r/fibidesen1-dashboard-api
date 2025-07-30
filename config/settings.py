import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # PostgreSQL (Render Postgres)
    POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
    POSTGRES_DB = os.getenv("POSTGRES_DB", "fibidesen1")
    #POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "")
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    # API Configuration
    API_V1_STR = "/api/v1"
    PROJECT_NAME = "Dashboard Médico API - fibidesen1"
    
    # CORS - Actualizar con tu dominio de Hostinger
    ALLOWED_ORIGINS = [
        "http://localhost:3000",
        "http://localhost:8080",
        "https://loveink.me/fibidesen1/pages/",  # Cambiar por tu dominio real
        "https://www.loveink.me/fibidesen1/pages/"  # Cambiar por tu dominio real
    ]
    
    @property
    def postgres_url(self):
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

settings = Settings()
