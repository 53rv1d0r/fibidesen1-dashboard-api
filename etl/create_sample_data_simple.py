#!/usr/bin/env python3
"""
Generador de datos de ejemplo SIN pandas
Para despliegue inicial en Render
"""

import logging
import random
from datetime import datetime, timedelta
from connectors.postgres_connector import PostgresConnector

logger = logging.getLogger(__name__)

class SimpleSampleDataGenerator:
    def __init__(self):
        self.postgres = PostgresConnector()
        
        self.aseguradoras = [
            "SURA EPS", "Nueva EPS", "Sanitas EPS", "Salud Total",
            "EPS Famisanar", "Comfenalco", "Coomeva EPS", 
            "Medimás EPS", "Capital Salud EPS", "Particular"
        ]
        
        self.diagnosticos = [
            "Quemadura térmica grado II",
            "Quemadura eléctrica múltiple",
            "Quemadura química en cara", 
            "Quemadura por llama en tórax",
            "Quemadura por contacto",
            "Quemadura por líquido caliente",
            "Quemadura solar severa",
            "Quemadura por explosión",
            "Quemadura por fricción",
            "Síndrome de inhalación"
        ]
        
        self.condiciones = ["Mejorado", "Alta médica", "Traslado", "Fallecido"]
        self.nombres = [
            "María García", "Juan Rodríguez", "Ana Martínez",
            "Carlos Sánchez", "Luz Vargas", "Pedro Gómez",
            "Carmen Jiménez", "Miguel Torres", "Sandra López"
        ]
    
    def generate_simple_data(self):
        """Genera datos directamente en la base de datos"""
        try:
            if not self.postgres.connect():
                raise Exception("No se pudo conectar a PostgreSQL")
            
            if not self.postgres.create_tables():
                raise Exception("No se pudieron crear las tablas")
            
            # Limpiar tablas
            with self.postgres.engine.connect() as conn:
                conn.execute("DELETE FROM dashboard_desenlaces")
                conn.execute("DELETE FROM dashboard_stats_aseguradora")
                conn.execute("DELETE FROM dashboard_stats_mensual")
                conn.execute("DELETE FROM dashboard_stats_demografia")
                conn.commit()
            
            # Generar 50 registros de ejemplo
            base_date = datetime.now() - timedelta(days=90)
            
            for i in range(50):
                fecha_ingreso = base_date + timedelta(days=random.randint(0, 90))
                dias_estancia = random.randint(1, 30)
                fecha_egreso = fecha_ingreso + timedelta(days=dias_estancia)
                
                # Insertar desenlace
                query = """
                INSERT INTO dashboard_desenlaces 
                (desenlaceq_id, numero_episodio, fecha_ingreso, fecha_egreso, 
                 dias_estancia, diagnostico, nombre_paciente, sexo, edad, 
                 nombre_aseguradora, condicion_egreso_nombre, fecha_procesamiento)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                
                values = (
                    i + 1,
                    i + 1000,
                    fecha_ingreso.date(),
                    fecha_egreso.date(),
                    dias_estancia,
                    random.choice(self.diagnosticos),
                    random.choice(self.nombres),
                    random.choice(['Masculino', 'Femenino']),
                    random.randint(18, 80),
                    random.choice(self.aseguradoras),
                    random.choice(self.condiciones),
                    datetime.now()
                )
                
                with self.postgres.engine.connect() as conn:
                    conn.execute(query, values)
                    conn.commit()
            
            # Generar estadísticas básicas
            self._generate_basic_stats()
            
            logger.info("✅ Datos de ejemplo generados exitosamente")
            return True
            
        except Exception as e:
            logger.error(f"Error generando datos: {e}")
            return False
        finally:
            self.postgres.close()
    
    def _generate_basic_stats(self):
        """Genera estadísticas básicas"""
        # Stats por aseguradora
        for aseg in self.aseguradoras[:5]:  # Solo 5 para ejemplo
            query = """
            INSERT INTO dashboard_stats_aseguradora 
            (nombre_aseguradora, total_casos, promedio_estancia, casos_mejorados, casos_fallecidos)
            VALUES (%s, %s, %s, %s, %s)
            """
            values = (aseg, random.randint(5, 15), random.randint(10, 25), random.randint(3, 12), random.randint(0, 2))
            
            with self.postgres.engine.connect() as conn:
                conn.execute(query, values)
                conn.commit()
        
        # Stats mensuales (últimos 3 meses)
        for i in range(3):
            mes = datetime.now().month - i
            año = datetime.now().year
            if mes <= 0:
                mes += 12
                año -= 1
            
            query = """
            INSERT INTO dashboard_stats_mensual 
            (año, mes, total_ingresos, promedio_estancia, casos_mejorados, casos_fallecidos)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            values = (año, mes, random.randint(10, 20), random.randint(12, 22), random.randint(8, 18), random.randint(0, 3))
            
            with self.postgres.engine.connect() as conn:
                conn.execute(query, values)
                conn.commit()

def main():
    """Función principal"""
    logger.info("=== Generador Simple de Datos ===")
    
    generator = SimpleSampleDataGenerator()
    success = generator.generate_simple_data()
    
    if success:
        logger.info("🎉 Datos listos para el dashboard!")
    else:
        logger.error("❌ Error generando datos")
    
    return success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)