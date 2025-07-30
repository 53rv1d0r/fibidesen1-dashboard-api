#!/usr/bin/env python3
"""
Script de inicialización simple para Render
"""

import os
import logging

# Configurar logging básico
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_environment():
    """Verifica que las variables de entorno estén disponibles"""
    required_vars = ['POSTGRES_HOST', 'POSTGRES_USER', 'POSTGRES_PASSWORD', 'POSTGRES_DB']
    
    logger.info("🔍 Verificando variables de entorno...")
    for var in required_vars:
        value = os.getenv(var)
        if value:
            logger.info(f"✅ {var}: configurado")
        else:
            logger.warning(f"⚠️ {var}: no configurado")
    
    return True

if __name__ == "__main__":
    logger.info("🚀 Iniciando verificación de entorno...")
    check_environment()
    logger.info("✅ Verificación completada")