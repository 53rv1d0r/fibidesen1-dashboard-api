#!/usr/bin/env python3
"""
Script de inicialización para Render
"""

import os
import logging

# Configurar logging básico
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def initialize_database():
    """Inicializa la base de datos con datos de ejemplo"""
    try:
        # Solo si hay variables de entorno de DB
        if not os.getenv('POSTGRES_HOST'):
            logger.info("⚠️ Variables de DB no disponibles, omitiendo inicialización")
            return True
        
        logger.info("🚀 Inicializando base de datos...")
        
        from etl.create_sample_data_simple import SimpleSampleDataGenerator
        generator = SimpleSampleDataGenerator()
        success = generator.generate_simple_data()
        
        if success:
            logger.info("✅ Base de datos inicializada!")
        else:
            logger.warning("⚠️ Error inicializando datos")
        
        return success
        
    except Exception as e:
        logger.error(f"Error en inicialización: {e}")
        return True  # No fallar el build por esto

if __name__ == "__main__":
    initialize_database()