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

@app.get("/api/v1/estadisticas/resumen")
def get_resumen():
    return {
        "total_pacientes": 45,
        "total_ingresos_mes": 12,
        "promedio_estancia": 15.5,
        "tasa_mortalidad": 8.2,
        "casos_activos": 8
    }

@app.get("/api/v1/desenlaces/")
def get_desenlaces():
    return [
        {
            "id": 1,
            "fecha_ingreso": "2025-01-15",
            "nombre_paciente": "María García",
            "edad": 45,
            "sexo": "Femenino",
            "diagnostico": "Quemadura térmica grado II",
            "nombre_aseguradora": "SURA EPS",
            "dias_estancia": 12,
            "condicion_egreso_nombre": "Mejorado"
        },
        {
            "id": 2,
            "fecha_ingreso": "2025-01-20",
            "nombre_paciente": "Juan Rodríguez",
            "edad": 32,
            "sexo": "Masculino",
            "diagnostico": "Quemadura eléctrica",
            "nombre_aseguradora": "Nueva EPS",
            "dias_estancia": 8,
            "condicion_egreso_nombre": "Alta médica"
        }
    ]

@app.get("/api/v1/estadisticas/aseguradoras")
def get_aseguradoras():
    return [
        {"nombre_aseguradora": "SURA EPS", "total_casos": 15, "promedio_estancia": 14.2},
        {"nombre_aseguradora": "Nueva EPS", "total_casos": 12, "promedio_estancia": 16.8},
        {"nombre_aseguradora": "Sanitas EPS", "total_casos": 8, "promedio_estancia": 12.5}
    ]

@app.get("/api/v1/estadisticas/mensuales")
def get_mensuales():
    return [
        {"año": 2025, "mes": 1, "total_ingresos": 12, "promedio_estancia": 15.2},
        {"año": 2024, "mes": 12, "total_ingresos": 18, "promedio_estancia": 14.8},
        {"año": 2024, "mes": 11, "total_ingresos": 15, "promedio_estancia": 16.1}
    ]

@app.post("/api/v1/etl/run")
def run_etl():
    return {
        "status": "success",
        "message": "ETL ejecutado exitosamente con datos de ejemplo",
        "timestamp": "2025-01-30T10:00:00"
    }

@app.post("/api/v1/etl/initialize")
def initialize_etl():
    return {
        "status": "success",
        "message": "Dashboard inicializado con datos de ejemplo",
        "ready_for_demo": True
    }
