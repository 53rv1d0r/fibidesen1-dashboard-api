from fastapi import APIRouter, HTTPException
from typing import List
import pandas as pd
from models.schemas import (
    EstadisticaAseguradora, 
    EstadisticaMensual, 
    EstadisticaDemografia,
    DashboardSummary
)
from services.database import db_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/estadisticas", tags=["estadisticas"])

@router.get("/resumen", response_model=DashboardSummary)
async def get_dashboard_summary():
    """
    Obtiene resumen general del dashboard con KPIs principales
    """
    try:
        summary = db_service.get_dashboard_summary()
        return summary
        
    except Exception as e:
        logger.error(f"Error obteniendo resumen del dashboard: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@router.get("/aseguradoras", response_model=List[dict])
async def get_estadisticas_aseguradoras():
    """
    Obtiene estadísticas agrupadas por aseguradora
    """
    try:
        df = db_service.get_estadisticas_aseguradoras()
        
        if df.empty:
            return []
        
        # Convertir a diccionario y limpiar NaN
        records = df.to_dict('records')
        
        for record in records:
            for key, value in record.items():
                if pd.isna(value):
                    record[key] = None
                elif key == 'promedio_estancia' and value is not None:
                    record[key] = float(value)
        
        logger.info(f"Retornando estadísticas de {len(records)} aseguradoras")
        return records
        
    except Exception as e:
        logger.error(f"Error obteniendo estadísticas por aseguradora: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@router.get("/mensuales", response_model=List[dict])
async def get_estadisticas_mensuales():
    """
    Obtiene estadísticas mensuales de los últimos 12 meses
    """
    try:
        df = db_service.get_estadisticas_mensuales()
        
        if df.empty:
            return []
        
        records = df.to_dict('records')
        
        # Limpiar y formatear datos
        for record in records:
            for key, value in record.items():
                if pd.isna(value):
                    record[key] = None
                elif key == 'promedio_estancia' and value is not None:
                    record[key] = float(value)
            
            # Agregar nombre del mes
            meses = {
                1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril',
                5: 'Mayo', 6: 'Junio', 7: 'Julio', 8: 'Agosto',
                9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
            }
            record['nombre_mes'] = meses.get(record['mes'], 'Desconocido')
        
        logger.info(f"Retornando estadísticas de {len(records)} meses")
        return records
        
    except Exception as e:
        logger.error(f"Error obteniendo estadísticas mensuales: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@router.get("/demografia", response_model=List[dict])
async def get_estadisticas_demografia():
    """
    Obtiene estadísticas demográficas por edad y sexo
    """
    try:
        df = db_service.get_estadisticas_demografia()
        
        if df.empty:
            return []
        
        records = df.to_dict('records')
        
        # Limpiar valores NaN
        for record in records:
            for key, value in record.items():
                if pd.isna(value):
                    record[key] = None
                elif key == 'promedio_estancia' and value is not None:
                    record[key] = float(value)
        
        logger.info(f"Retornando estadísticas demográficas de {len(records)} grupos")
        return records
        
    except Exception as e:
        logger.error(f"Error obteniendo estadísticas demográficas: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@router.get("/mortalidad")
async def get_estadisticas_mortalidad():
    """
    Obtiene estadísticas detalladas de mortalidad
    """
    try:
        query = """
        SELECT 
            condicion_egreso_nombre,
            COUNT(*) as total_casos,
            ROUND((COUNT(*) * 100.0 / SUM(COUNT(*)) OVER()), 2) as porcentaje
        FROM dashboard_desenlaces
        WHERE condicion_egreso_nombre IS NOT NULL
        GROUP BY condicion_egreso_nombre
        ORDER BY total_casos DESC
        """
        
        df = db_service.execute_query(query)
        
        if df.empty:
            return {"total_casos": 0, "distribución": []}
        
        records = df.to_dict('records')
        total_casos = sum(record['total_casos'] for record in records)
        
        return {
            "total_casos": total_casos,
            "distribución": records
        }
        
    except Exception as e:
        logger.error(f"Error obteniendo estadísticas de mortalidad: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@router.get("/top-diagnosticos")
async def get_top_diagnosticos():
    """
    Obtiene los diagnósticos más frecuentes
    """
    try:
        query = """
        SELECT 
            diagnostico,
            COUNT(*) as total_casos,
            ROUND(AVG(dias_estancia), 1) as promedio_estancia
        FROM dashboard_desenlaces
        WHERE diagnostico IS NOT NULL AND diagnostico != ''
        GROUP BY diagnostico
        ORDER BY total_casos DESC
        LIMIT 10
        """
        
        df = db_service.execute_query(query)
        
        if df.empty:
            return []
        
        records = df.to_dict('records')
        
        # Limpiar valores NaN
        for record in records:
            for key, value in record.items():
                if pd.isna(value):
                    record[key] = None
        
        return records
        
    except Exception as e:
        logger.error(f"Error obteniendo top diagnósticos: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@router.get("/estancia-promedio")
async def get_analisis_estancia():
    """
    Obtiene análisis detallado de días de estancia
    """
    try:
        query = """
        SELECT 
            CASE 
                WHEN dias_estancia <= 7 THEN '1-7 días'
                WHEN dias_estancia <= 14 THEN '8-14 días'
                WHEN dias_estancia <= 21 THEN '15-21 días'
                WHEN dias_estancia <= 30 THEN '22-30 días'
                ELSE 'Más de 30 días'
            END as rango_estancia,
            COUNT(*) as total_casos,
            ROUND(AVG(dias_estancia), 1) as promedio_estancia,
            MIN(dias_estancia) as minimo,
            MAX(dias_estancia) as maximo
        FROM dashboard_desenlaces
        WHERE dias_estancia IS NOT NULL AND dias_estancia > 0
        GROUP BY 
            CASE 
                WHEN dias_estancia <= 7 THEN '1-7 días'
                WHEN dias_estancia <= 14 THEN '8-14 días'
                WHEN dias_estancia <= 21 THEN '15-21 días'
                WHEN dias_estancia <= 30 THEN '22-30 días'
                ELSE 'Más de 30 días'
            END
        ORDER BY MIN(dias_estancia)
        """
        
        df = db_service.execute_query(query)
        
        if df.empty:
            return []
        
        records = df.to_dict('records')
        
        # Calcular estadísticas generales
        query_general = """
        SELECT 
            COUNT(*) as total_casos,
            ROUND(AVG(dias_estancia), 1) as promedio_general,
            MIN(dias_estancia) as minimo_general,
            MAX(dias_estancia) as maximo_general
        FROM dashboard_desenlaces
        WHERE dias_estancia IS NOT NULL AND dias_estancia > 0
        """
        
        df_general = db_service.execute_query(query_general)
        general = df_general.iloc[0].to_dict() if not df_general.empty else {}
        
        return {
            "resumen_general": general,
            "distribución_por_rangos": records
        }
        
    except Exception as e:
        logger.error(f"Error obteniendo análisis de estancia: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")
