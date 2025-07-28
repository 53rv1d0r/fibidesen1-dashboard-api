from fastapi import APIRouter, HTTPException
from services.etl_service import etl_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/etl", tags=["etl"])

@router.post("/run")
async def run_etl():
    """
    Ejecuta el proceso ETL con datos de ejemplo médicos realistas
    Perfecto para MVP y demostraciones
    """
    try:
        # Verificar si ETL ya está corriendo
        status = etl_service.get_status()
        if status["is_running"]:
            raise HTTPException(
                status_code=409, 
                detail="ETL process is already running. Please wait for it to complete."
            )
        
        logger.info("Iniciando ETL con datos de ejemplo médicos via API")
        
        # Siempre usar datos de ejemplo
        result = await etl_service.run_etl_process(use_sample_data=True)
        
        if result["status"] == "error":
            raise HTTPException(status_code=500, detail=result["message"])
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error en endpoint ETL: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/status")
async def get_etl_status():
    """
    Obtiene el estado actual del proceso ETL
    """
    try:
        return etl_service.get_status()
    except Exception as e:
        logger.error(f"Error obteniendo estado ETL: {e}")
        raise HTTPException(status_code=500, detail="Error obtaining ETL status")

@router.post("/initialize")
async def initialize_dashboard():
    """
    Inicializa el dashboard con datos de ejemplo médicos frescos
    """
    try:
        logger.info("Inicializando dashboard con datos médicos de ejemplo")
        
        result = await etl_service.run_etl_process(use_sample_data=True)
        
        if result["status"] == "success":
            return {
                **result,
                "message": "Dashboard inicializado con datos médicos de ejemplo",
                "ready_for_demo": True,
                "next_steps": [
                    "Dashboard API listo para servir datos",
                    "Frontend puede conectarse y mostrar visualizaciones",
                    "Datos incluyen: desenlaces, estadísticas, demografía"
                ]
            }
        else:
            raise HTTPException(status_code=500, detail=result["message"])
            
    except Exception as e:
        logger.error(f"Error inicializando dashboard: {e}")
        raise HTTPException(status_code=500, detail=f"Error initializing dashboard: {str(e)}")
