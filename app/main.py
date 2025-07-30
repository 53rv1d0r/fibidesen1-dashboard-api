from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Dashboard Médico API")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {
        "message": "Dashboard Médico API - fibidesen1",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "dashboard_api"}

@app.get("/api/v1/test")
def test_endpoint():
    return {"message": "API funcionando correctamente", "timestamp": "2025-01-30"}
