"""
Servicio ETL integrado en el Dashboard API
Permite ejecutar ETL bajo demanda via endpoint HTTP
"""

import logging
import pandas as pd
from datetime import datetime
import asyncio
from typing import Dict, Any

from etl.connectors.sqlserver_connector import SQLServerConnector
from etl.connectors.postgres_connector import PostgresConnector
from etl.transformers.data_transformer import DataTransformer
from config.settings import settings

logger = logging.getLogger(__name__)

class ETLService:
    def __init__(self):
        self.sqlserver = None
        self.postgres = None
        self.transformer = DataTransformer()
        self.status = "idle"
        self.last_run = None
        self.last_error = None
    
    async def run_etl_process(self, use_sample_data: bool = False) -> Dict[str, Any]:
        """
        Ejecuta el proceso ETL completo
        Args:
            use_sample_data: Si True, genera datos de ejemplo en lugar de extraer de SQL Server
        """
        self.status = "running"
        start_time = datetime.now()
        
        try:
            logger.info("=== Iniciando proceso ETL bajo demanda ===")
            
            # Inicializar conectores
            self.postgres = PostgresConnector()
            
            # 1. Crear tablas si no existen
            logger.info("Verificando/creando tablas en PostgreSQL...")
            tables_created = self.postgres.create_tables()
            if not tables_created:
                raise Exception("No se pudieron crear las tablas en PostgreSQL")
            
            if use_sample_data:
                # Usar generador de datos de ejemplo
                logger.info("Generando datos de ejemplo médicos...")
                result = await self._generate_sample_data()
            else:
                # Extraer de SQL Server real
                logger.info("Extrayendo datos de SQL Server fibidesen1...")
                result = await self._extract_from_sqlserver()
            
            # Actualizar estado
            self.status = "completed"
            self.last_run = datetime.now()
            self.last_error = None
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            return {
                "status": "success",
                "message": "ETL ejecutado exitosamente",
                "execution_time_seconds": round(execution_time, 2),
                "timestamp": self.last_run.isoformat(),
                "data_source": "sample_data" if use_sample_data else "sql_server",
                "statistics": result
            }
            
        except Exception as e:
            self.status = "error"
            self.last_error = str(e)
            execution_time = (datetime.now() - start_time).total_seconds()
            
            logger.error(f"Error en proceso ETL: {e}")
            
            return {
                "status": "error",
                "message": f"Error ejecutando ETL: {str(e)}",
                "execution_time_seconds": round(execution_time, 2),
                "timestamp": datetime.now().isoformat(),
                "error": str(e)
            }
        
        finally:
            # Limpiar conexiones
            if self.postgres:
                self.postgres.close()
            if self.sqlserver:
                self.sqlserver.close()
    
    async def _generate_sample_data(self) -> Dict[str, Any]:
        """Genera datos de ejemplo médicos"""
        try:
            # Importar el generador de datos de ejemplo
            from etl.create_sample_data import SampleDataGenerator
            
            generator = SampleDataGenerator()
            
            # Generar datos
            desenlaces_df = generator.generate_desenlaces_data(150)
            stats_aseg = generator.generate_stats_aseguradora(desenlaces_df)
            stats_mensual = generator.generate_stats_mensual(desenlaces_df)
            stats_demo = generator.generate_stats_demografia(desenlaces_df)
            
            # Cargar en base de datos
            success1 = self.postgres.load_data(desenlaces_df, 'dashboard_desenlaces')
            success2 = self.postgres.load_data(stats_aseg, 'dashboard_stats_aseguradora')
            success3 = self.postgres.load_data(stats_mensual, 'dashboard_stats_mensual')
            success4 = self.postgres.load_data(stats_demo, 'dashboard_stats_demografia')
            
            if not all([success1, success2, success3, success4]):
                raise Exception("Error cargando algunos conjuntos de datos")
            
            return {
                "desenlaces_count": len(desenlaces_df),
                "aseguradoras_count": len(stats_aseg),
                "meses_count": len(stats_mensual),
                "grupos_demograficos_count": len(stats_demo)
            }
            
        except Exception as e:
            logger.error(f"Error generando datos de ejemplo: {e}")
            raise
    
    async def _extract_from_sqlserver(self) -> Dict[str, Any]:
        """Extrae datos reales de SQL Server"""
        try:
            self.sqlserver = SQLServerConnector()
            
            if not self.sqlserver.connect():
                raise Exception("No se pudo conectar a SQL Server")
            
            # Extraer datos
            desenlaces_df = self.sqlserver.get_desenlaces_data()
            stats_aseg_df = self.sqlserver.get_estadisticas_por_aseguradora()
            stats_mensual_df = self.sqlserver.get_estadisticas_por_mes()
            stats_demo_df = self.sqlserver.get_estadisticas_por_edad_sexo()
            
            # Transformar datos
            if not desenlaces_df.empty:
                desenlaces_cleaned = self.transformer.clean_desenlaces_data(desenlaces_df)
            else:
                desenlaces_cleaned = pd.DataFrame()
            
            # Cargar en PostgreSQL
            if not desenlaces_cleaned.empty:
                self.postgres.load_data(desenlaces_cleaned, 'dashboard_desenlaces')
            
            if not stats_aseg_df.empty:
                self.postgres.load_data(stats_aseg_df, 'dashboard_stats_aseguradora')
            
            if not stats_mensual_df.empty:
                self.postgres.load_data(stats_mensual_df, 'dashboard_stats_mensual')
            
            if not stats_demo_df.empty:
                self.postgres.load_data(stats_demo_df, 'dashboard_stats_demografia')
            
            return {
                "desenlaces_count": len(desenlaces_cleaned),
                "aseguradoras_count": len(stats_aseg_df),
                "meses_count": len(stats_mensual_df),
                "grupos_demograficos_count": len(stats_demo_df)
            }
            
        except Exception as e:
            logger.error(f"Error extrayendo de SQL Server: {e}")
            raise
    
    def get_status(self) -> Dict[str, Any]:
        """Obtiene el estado actual del ETL"""
        return {
            "status": self.status,
            "last_run": self.last_run.isoformat() if self.last_run else None,
            "last_error": self.last_error,
            "is_running": self.status == "running"
        }

# Instancia global del servicio ETL
etl_service = ETLService()
