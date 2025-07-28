from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import desenlaces, estadisticas
from config.settings import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(desenlaces.router, prefix=settings.API_V1_STR)
app.include_router(estadisticas.router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {
        "message": "Dashboard Médico API - fibidesen1",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "dashboard_api"}
