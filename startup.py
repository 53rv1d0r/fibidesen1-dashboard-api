#!/usr/bin/env python3
"""
Script de inicialización para Render
Se ejecuta automáticamente al desplegar
"""

import logging
import asyncio
from etl.connectors.postgres_connector import PostgresConnector
from etl.create_sample_data import SampleDataGenerator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def initialize_database():
    """Inicializa la base de datos con datos de ejemplo"""
    try:
        logger.info("🚀 Inicializando base de datos...")
        
        # 1. Crear tablas
        postgres = PostgresConnector()
        if not postgres.create_tables():
            raise Exception("No se pudieron crear las tablas")
        
        # 2. Verificar si ya hay datos
        existing_data = postgres.get_data("SELECT COUNT(*) as count FROM dashboard_desenlaces")
        if not existing_data.empty and existing_data.iloc[0]['count'] > 0:
            logger.info("✅ Base de datos ya tiene datos, omitiendo inicialización")
            return True
        
        # 3. Generar datos de ejemplo
        logger.info("📊 Generando datos de ejemplo...")
        generator = SampleDataGenerator()
        success = generator.load_sample_data()
        
        if success:
            logger.info("🎉 Base de datos inicializada correctamente!")
            return True
        else:
            logger.error("❌ Error inicializando base de datos")
            return False
            
    except Exception as e:
        logger.error(f"Error en inicialización: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(initialize_database())
    exit(0 if success else 1)
