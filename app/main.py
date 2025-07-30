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
        {"id": 1, "fecha_ingreso": "2025-01-15", "nombre_paciente": "María García", "edad": 45, "sexo": "Femenino", "diagnostico": "Quemadura térmica grado II", "nombre_aseguradora": "SURA EPS", "dias_estancia": 12, "condicion_egreso_nombre": "Mejorado"},
        {"id": 2, "fecha_ingreso": "2025-01-20", "nombre_paciente": "Juan Rodríguez", "edad": 32, "sexo": "Masculino", "diagnostico": "Quemadura eléctrica", "nombre_aseguradora": "Nueva EPS", "dias_estancia": 8, "condicion_egreso_nombre": "Alta médica"},
        {"id": 3, "fecha_ingreso": "2025-01-18", "nombre_paciente": "Ana Martínez", "edad": 28, "sexo": "Femenino", "diagnostico": "Quemadura química", "nombre_aseguradora": "Sanitas EPS", "dias_estancia": 15, "condicion_egreso_nombre": "Mejorado"},
        {"id": 4, "fecha_ingreso": "2025-01-22", "nombre_paciente": "Carlos Sánchez", "edad": 38, "sexo": "Masculino", "diagnostico": "Quemadura por llama", "nombre_aseguradora": "Salud Total", "dias_estancia": 20, "condicion_egreso_nombre": "Traslado"},
        {"id": 5, "fecha_ingreso": "2025-01-25", "nombre_paciente": "Luz Vargas", "edad": 52, "sexo": "Femenino", "diagnostico": "Quemadura por contacto", "nombre_aseguradora": "EPS Famisanar", "dias_estancia": 6, "condicion_egreso_nombre": "Alta médica"},
        {"id": 6, "fecha_ingreso": "2025-01-12", "nombre_paciente": "Pedro Gómez", "edad": 41, "sexo": "Masculino", "diagnostico": "Quemadura solar severa", "nombre_aseguradora": "Comfenalco", "dias_estancia": 4, "condicion_egreso_nombre": "Mejorado"},
        {"id": 7, "fecha_ingreso": "2025-01-28", "nombre_paciente": "Carmen Jiménez", "edad": 35, "sexo": "Femenino", "diagnostico": "Quemadura por explosión", "nombre_aseguradora": "Coomeva EPS", "dias_estancia": 25, "condicion_egreso_nombre": "Fallecido"},
        {"id": 8, "fecha_ingreso": "2025-01-10", "nombre_paciente": "Miguel Torres", "edad": 29, "sexo": "Masculino", "diagnostico": "Quemadura por fricción", "nombre_aseguradora": "Medimás EPS", "dias_estancia": 9, "condicion_egreso_nombre": "Alta médica"},
        {"id": 9, "fecha_ingreso": "2025-01-14", "nombre_paciente": "Sandra López", "edad": 47, "sexo": "Femenino", "diagnostico": "Síndrome de inhalación", "nombre_aseguradora": "Capital Salud EPS", "dias_estancia": 18, "condicion_egreso_nombre": "Mejorado"},
        {"id": 10, "fecha_ingreso": "2025-01-26", "nombre_paciente": "José Hernández", "edad": 55, "sexo": "Masculino", "diagnostico": "Quemadura térmica grado III", "nombre_aseguradora": "Particular", "dias_estancia": 30, "condicion_egreso_nombre": "Traslado"}
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

@app.get("/api/v1/estadisticas/top-diagnosticos")
def get_top_diagnosticos():
    return [
        {"diagnostico": "Quemadura térmica grado II", "total_casos": 15, "promedio_estancia": 14.2},
        {"diagnostico": "Quemadura eléctrica", "total_casos": 8, "promedio_estancia": 18.5},
        {"diagnostico": "Quemadura química", "total_casos": 6, "promedio_estancia": 16.8},
        {"diagnostico": "Quemadura por llama", "total_casos": 5, "promedio_estancia": 22.1},
        {"diagnostico": "Síndrome de inhalación", "total_casos": 4, "promedio_estancia": 25.3}
    ]

@app.get("/api/v1/estadisticas/estancia-promedio")
def get_estancia_promedio():
    return {
        "resumen_general": {
            "promedio_general": 16.8,
            "total_casos": 45,
            "mediana": 15.0
        },
        "distribución_por_rangos": [
            {"rango_estancia": "1-7 días", "total_casos": 12, "promedio_estancia": 4.5},
            {"rango_estancia": "8-15 días", "total_casos": 18, "promedio_estancia": 11.2},
            {"rango_estancia": "16-30 días", "total_casos": 10, "promedio_estancia": 22.8},
            {"rango_estancia": "Más de 30 días", "total_casos": 5, "promedio_estancia": 38.4}
        ]
    }

@app.get("/api/v1/estadisticas/mortalidad")
def get_mortalidad():
    return {
        "resumen": {
            "total_casos": 45,
            "total_fallecidos": 3,
            "tasa_mortalidad": 6.7
        },
        "distribución": [
            {"condicion_egreso_nombre": "Mejorado", "total_casos": 25, "porcentaje": 55.6},
            {"condicion_egreso_nombre": "Alta médica", "total_casos": 12, "porcentaje": 26.7},
            {"condicion_egreso_nombre": "Traslado", "total_casos": 5, "porcentaje": 11.1},
            {"condicion_egreso_nombre": "Fallecido", "total_casos": 3, "porcentaje": 6.7}
        ]
    }

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
2025-01-18,Ana Martínez,28,Femenino,Quemadura química,Sanitas EPS,15,Mejorado
2025-01-22,Carlos Sánchez,38,Masculino,Quemadura por llama,Salud Total,20,Traslado
2025-01-25,Luz Vargas,52,Femenino,Quemadura por contacto,EPS Famisanar,6,Alta médica
2025-01-12,Pedro Gómez,41,Masculino,Quemadura solar severa,Comfenalco,4,Mejorado
2025-01-28,Carmen Jiménez,35,Femenino,Quemadura por explosión,Coomeva EPS,25,Fallecido
2025-01-10,Miguel Torres,29,Masculino,Quemadura por fricción,Medimás EPS,9,Alta médica
2025-01-14,Sandra López,47,Femenino,Síndrome de inhalación,Capital Salud EPS,18,Mejorado
2025-01-26,José Hernández,55,Masculino,Quemadura térmica grado III,Particular,30,Traslado"""
    
    return PlainTextResponse(
        content=csv_content,
        headers={
            "Content-Disposition": "attachment; filename=desenlaces_fibidesen1.csv",
            "Content-Type": "text/csv"
        }
    )
