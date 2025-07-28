# Dashboard API - fibidesen1

API REST construida con FastAPI que sirve datos médicos procesados para el dashboard de la Unidad de Quemados.

## 🔌 Funcionalidad

- **API REST** con FastAPI y documentación automática
- **Endpoints** para KPIs, estadísticas y datos médicos
- **Validación** de datos con Pydantic
- **CORS** configurado para frontend web
- **Exportación** CSV de datos

## 📋 Endpoints Disponibles

### KPIs y Resumen
- `GET /api/v1/estadisticas/resumen` - KPIs principales del dashboard
- `GET /health` - Health check del servicio

### Desenlaces Médicos
- `GET /api/v1/desenlaces/` - Lista de desenlaces con filtros
- `GET /api/v1/desenlaces/{id}` - Desenlace específico
- `GET /api/v1/desenlaces/paciente/{historia}` - Por historia clínica
- `GET /api/v1/desenlaces/export/csv` - Exportar a CSV

### Estadísticas
- `GET /api/v1/estadisticas/aseguradoras` - Por aseguradora
- `GET /api/v1/estadisticas/mensuales` - Tendencias mensuales  
- `GET /api/v1/estadisticas/demografia` - Por edad y sexo
- `GET /api/v1/estadisticas/mortalidad` - Análisis de mortalidad
- `GET /api/v1/estadisticas/top-diagnosticos` - Diagnósticos frecuentes
- `GET /api/v1/estadisticas/estancia-promedio` - Análisis de estancia

## 🚀 Deployment en Render

### Variables de Entorno Requeridas
```
POSTGRES_HOST=<render_postgres_host>
POSTGRES_PORT=5432
POSTGRES_DB=fibidesen1
POSTGRES_USER=<render_user>
POSTGRES_PASSWORD=<render_password>
```

### Configuración Render
- **Service Type**: Web Service
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- **Health Check Path**: `/health`

## 🔧 Desarrollo Local

### Instalación
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

### Configuración
1. Copiar `.env.example` a `.env`
2. Configurar credenciales PostgreSQL

### Ejecución
```bash
uvicorn app.main:app --reload --port 8000
```

### Documentación
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📊 Modelos de Datos

### Respuestas Principales
- **DashboardSummary**: KPIs del dashboard
- **DesenlaceResponse**: Datos de desenlaces médicos
- **EstadisticaAseguradora**: Estadísticas por aseguradora
- **EstadisticaMensual**: Tendencias mensuales
- **EstadisticaDemografia**: Análisis demográfico

### Filtros Disponibles
- Rango de fechas
- Aseguradora específica
- Sexo del paciente
- Rango de edad
- Condición de egreso

## 🏗️ Arquitectura

```
PostgreSQL (Render)
    ↓
Database Service
    ↓
FastAPI Routes
    ↓
Pydantic Validation
    ↓
JSON Response
    ↓
Frontend Dashboard
```

## 🔒 Características

- **Validación automática** de datos con Pydantic
- **Documentación** API automática con OpenAPI
- **CORS** habilitado para desarrollo y producción
- **Manejo de errores** estructurado
- **Logging** integrado
- **Health checks** para monitoreo

---

**Dashboard API** - Parte del Dashboard Médico fibidesen1
