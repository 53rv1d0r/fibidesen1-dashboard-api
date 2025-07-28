from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Optional
from datetime import date
import pandas as pd
from models.schemas import DesenlaceResponse, FiltroDesenlaces
from services.database import db_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/desenlaces", tags=["desenlaces"])

@router.get("/", response_model=List[dict])
async def get_desenlaces(
    fecha_inicio: Optional[date] = Query(None, description="Fecha de inicio (YYYY-MM-DD)"),
    fecha_fin: Optional[date] = Query(None, description="Fecha de fin (YYYY-MM-DD)"),
    aseguradora: Optional[str] = Query(None, description="Nombre de la aseguradora"),
    sexo: Optional[str] = Query(None, description="Sexo del paciente"),
    edad_min: Optional[int] = Query(None, description="Edad mínima"),
    edad_max: Optional[int] = Query(None, description="Edad máxima"),
    condicion_egreso: Optional[str] = Query(None, description="Condición de egreso"),
    limit: int = Query(100, le=1000, description="Límite de registros")
):
    """
    Obtiene lista de desenlaces de pacientes quemados con filtros opcionales
    """
    try:
        # Construir filtros
        filtros = {}
        if fecha_inicio:
            filtros['fecha_inicio'] = fecha_inicio
        if fecha_fin:
            filtros['fecha_fin'] = fecha_fin
        if aseguradora:
            filtros['aseguradora'] = aseguradora
        if sexo:
            filtros['sexo'] = sexo
        if edad_min:
            filtros['edad_min'] = edad_min
        if edad_max:
            filtros['edad_max'] = edad_max
        if condicion_egreso:
            filtros['condicion_egreso'] = condicion_egreso
        
        # Obtener datos
        df = db_service.get_desenlaces(filtros)
        
        if df.empty:
            return []
        
        # Limitar resultados
        df = df.head(limit)
        
        # Convertir a diccionario y manejar valores NaN
        records = df.to_dict('records')
        
        # Limpiar valores NaN para JSON
        for record in records:
            for key, value in record.items():
                if pd.isna(value):
                    record[key] = None
        
        logger.info(f"Retornando {len(records)} registros de desenlaces")
        return records
        
    except Exception as e:
        logger.error(f"Error obteniendo desenlaces: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@router.get("/{desenlace_id}")
async def get_desenlace_by_id(desenlace_id: int):
    """
    Obtiene un desenlace específico por ID
    """
    try:
        query = """
        SELECT *
        FROM dashboard_desenlaces
        WHERE desenlaceq_id = %(desenlace_id)s
        """
        
        df = db_service.execute_query(query, {'desenlace_id': desenlace_id})
        
        if df.empty:
            raise HTTPException(status_code=404, detail="Desenlace no encontrado")
        
        record = df.iloc[0].to_dict()
        
        # Limpiar valores NaN
        for key, value in record.items():
            if pd.isna(value):
                record[key] = None
        
        return record
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error obteniendo desenlace {desenlace_id}: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@router.get("/paciente/{historia_clinica}")
async def get_desenlaces_by_historia(historia_clinica: str):
    """
    Obtiene todos los desenlaces de un paciente por número de historia clínica
    """
    try:
        query = """
        SELECT *
        FROM dashboard_desenlaces
        WHERE numero_historia_clinica = %(historia_clinica)s
        ORDER BY fecha_ingreso DESC
        """
        
        df = db_service.execute_query(query, {'historia_clinica': historia_clinica})
        
        if df.empty:
            raise HTTPException(status_code=404, detail="No se encontraron registros para esta historia clínica")
        
        records = df.to_dict('records')
        
        # Limpiar valores NaN
        for record in records:
            for key, value in record.items():
                if pd.isna(value):
                    record[key] = None
        
        return {
            "historia_clinica": historia_clinica,
            "total_registros": len(records),
            "desenlaces": records
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error obteniendo desenlaces para historia {historia_clinica}: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@router.get("/export/csv")
async def export_desenlaces_csv(
    fecha_inicio: Optional[date] = Query(None),
    fecha_fin: Optional[date] = Query(None),
    aseguradora: Optional[str] = Query(None)
):
    """
    Exporta desenlaces en formato CSV
    """
    try:
        from fastapi.responses import StreamingResponse
        import io
        
        # Construir filtros
        filtros = {}
        if fecha_inicio:
            filtros['fecha_inicio'] = fecha_inicio
        if fecha_fin:
            filtros['fecha_fin'] = fecha_fin
        if aseguradora:
            filtros['aseguradora'] = aseguradora
        
        # Obtener datos
        df = db_service.get_desenlaces(filtros)
        
        if df.empty:
            raise HTTPException(status_code=404, detail="No hay datos para exportar")
        
        # Crear CSV en memoria
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False, encoding='utf-8')
        csv_buffer.seek(0)
        
        # Crear respuesta de streaming
        def iter_csv():
            yield csv_buffer.getvalue()
        
        return StreamingResponse(
            iter_csv(),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=desenlaces_quemados.csv"}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error exportando CSV: {e}")
        raise HTTPException(status_code=500, detail="Error generando archivo CSV")
