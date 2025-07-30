from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse

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
        "timestamp": "2025-01-30T10:00:00",
        "execution_time_seconds": 2.5,
        "data_source": "sample_data",
        "statistics": {
            "desenlaces_count": 45,
            "aseguradoras_count": 8,
            "meses_count": 12,
            "grupos_demograficos_count": 6
        }
    }

@app.post("/api/v1/etl/initialize")
def initialize_etl():
    return {
        "status": "success",
        "message": "Dashboard inicializado con datos de ejemplo",
        "ready_for_demo": True,
        "execution_time_seconds": 3.2,
        "timestamp": "2025-01-30T10:00:00",
        "statistics": {
            "desenlaces_count": 45,
            "aseguradoras_count": 8,
            "meses_count": 12,
            "grupos_demograficos_count": 6
        },
        "next_steps": [
            "Dashboard API listo para servir datos",
            "Frontend puede conectarse y mostrar visualizaciones",
            "Datos incluyen: desenlaces, estadísticas, demografía"
        ]
    }

@app.get("/api/v1/estadisticas/demografia")
def get_demografia():
    return [
        {"sexo": "Masculino", "rango_edad": "18-30", "total_casos": 8},
        {"sexo": "Masculino", "rango_edad": "31-50", "total_casos": 12},
        {"sexo": "Masculino", "rango_edad": "51-70", "total_casos": 6},
        {"sexo": "Femenino", "rango_edad": "18-30", "total_casos": 5},
        {"sexo": "Femenino", "rango_edad": "31-50", "total_casos": 9},
        {"sexo": "Femenino", "rango_edad": "51-70", "total_casos": 5}
    ]

@app.get("/api/v1/estadisticas/condiciones-egreso")
def get_condiciones_egreso():
    return [
        {"condicion": "Mejorado", "total": 25, "porcentaje": 55.6},
        {"condicion": "Alta médica", "total": 12, "porcentaje": 26.7},
        {"condicion": "Traslado", "total": 5, "porcentaje": 11.1},
        {"condicion": "Fallecido", "total": 3, "porcentaje": 6.7}
    ]

@app.get("/api/v1/estadisticas/diagnosticos")
def get_diagnosticos():
    return [
        {"diagnostico": "Quemadura térmica grado II", "total_casos": 15},
        {"diagnostico": "Quemadura eléctrica", "total_casos": 8},
        {"diagnostico": "Quemadura química", "total_casos": 6},
        {"diagnostico": "Quemadura por llama", "total_casos": 5},
        {"diagnostico": "Quemadura por contacto", "total_casos": 4}
    ]

@app.get("/api/v1/estadisticas/estancia")
def get_estancia():
    return [
        {"rango": "1-7 días", "total_casos": 12, "porcentaje": 26.7},
        {"rango": "8-15 días", "total_casos": 18, "porcentaje": 40.0},
        {"rango": "16-30 días", "total_casos": 10, "porcentaje": 22.2},
        {"rango": "Más de 30 días", "total_casos": 5, "porcentaje": 11.1}
    ]

@app.get("/api/v1/etl/status")
def get_etl_status():
    return {
        "status": "completed",
        "last_run": "2025-01-30T10:00:00",
        "last_error": None,
        "is_running": False
    }

@app.get("/api/v1/desenlaces/export/csv")
def export_desenlaces_csv():
    csv_content = """fecha_ingreso,nombre_paciente,edad,sexo,diagnostico,aseguradora,dias_estancia,estado
2025-01-15,María García,45,Femenino,Quemadura térmica grado II,SURA EPS,12,Mejorado
2025-01-20,Juan Rodríguez,32,Masculino,Quemadura eléctrica,Nueva EPS,8,Alta médica
2025-01-18,Ana Martínez,28,Femenino,Quemadura química,Sanitas EPS,15,Mejorado"""
    
    return PlainTextResponse(
        content=csv_content,
        headers={
            "Content-Disposition": "attachment; filename=desenlaces_fibidesen1.csv",
            "Content-Type": "text/csv"
        }
    )
