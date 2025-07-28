#!/usr/bin/env python3
"""
Script de inicialización para crear tablas en PostgreSQL
Ejecutar una vez antes del primer ETL
"""

import logging
from connectors.postgres_connector import PostgresConnector
from config.settings import settings

logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Inicializa la base de datos PostgreSQL"""
    logger.info("Iniciando inicialización de base de datos...")
    
    try:
        postgres = PostgresConnector()
        
        # Crear tablas
        success = postgres.create_tables()
        
        if success:
            logger.info("Base de datos inicializada correctamente")
            
            # Verificar conexión
            test_query = "SELECT COUNT(*) as count FROM information_schema.tables WHERE table_schema = 'public'"
            df = postgres.execute_query(test_query)
            
            if not df.empty:
                table_count = df.iloc[0]['count']
                logger.info(f"Se encontraron {table_count} tablas en la base de datos")
            
        else:
            logger.error("Error inicializando base de datos")
            return False
            
        postgres.close()
        return True
        
    except Exception as e:
        logger.error(f"Error en inicialización: {e}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
