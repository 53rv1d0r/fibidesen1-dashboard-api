#!/usr/bin/env python3
"""
Script para crear datos de ejemplo médicos realistas para el dashboard
Ejecutar DESPUÉS de crear las tablas con init_db.py
"""

import logging
import pandas as pd
from datetime import datetime, timedelta
import random
import uuid
from connectors.postgres_connector import PostgresConnector
from config.settings import settings

# Configurar logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SampleDataGenerator:
    def __init__(self):
        self.postgres = PostgresConnector()
        
        # Datos base para generar ejemplos realistas
        self.aseguradoras = [
            "SURA EPS", "Nueva EPS", "Sanitas EPS", "Salud Total",
            "EPS Famisanar", "Comfenalco", "Coomeva EPS", 
            "Medimás EPS", "Capital Salud EPS", "Particular/Prepagada"
        ]
        
        self.diagnosticos = [
            "Quemadura térmica grado II en brazo",
            "Quemadura eléctrica múltiple",
            "Quemadura química en cara y cuello", 
            "Quemadura por llama en tórax",
            "Quemadura por contacto en mano",
            "Quemadura por líquido caliente en pierna",
            "Quemadura solar severa",
            "Quemadura por explosión multiple",
            "Quemadura por fricción",
            "Síndrome de inhalación de humo"
        ]
        
        self.condiciones_egreso = [
            "Mejorado", "Mejorado", "Mejorado", "Mejorado", "Mejorado",  # 50% mejorados
            "Alta médica", "Alta médica", "Alta médica",  # 30% alta médica
            "Traslado", "Fallecido"  # 10% traslado, 10% fallecido
        ]
        
        self.salas = [
            "UCI Quemados", "Hospitalización General", 
            "Cirugía Plástica", "Cuidados Intermedios"
        ]
        
        self.nombres = [
            "María García López", "Juan Carlos Rodríguez", "Ana Sofía Martínez",
            "Carlos Alberto Sánchez", "Luz Elena Vargas", "Pedro Antonio Gómez",
            "Carmen Rosa Jiménez", "Miguel Ángel Torres", "Sandra Patricia López",
            "José Luis Hernández", "Gloria Inés Morales", "Roberto Carlos Díaz",
            "Patricia Elena Ruiz", "Fernando José Castro", "Claudia Marcela Silva"
        ]
    
    def generate_desenlaces_data(self, num_records=150):
        """Genera datos de desenlaces médicos realistas"""
        logger.info(f"Generando {num_records} registros de desenlaces...")
        
        data = []
        base_date = datetime.now() - timedelta(days=90)
        
        for i in range(num_records):
            # Fechas realistas
            fecha_ingreso = base_date + timedelta(days=random.randint(0, 90))
            dias_estancia = random.randint(1, 45)
            fecha_egreso = fecha_ingreso + timedelta(days=dias_estancia) if random.random() > 0.1 else None
            
            # Datos del paciente
            sexo = random.choice(['Masculino', 'Femenino'])
            edad = random.randint(5, 85)
            
            # Severity correlation - casos más severos tienen más días
            if dias_estancia > 30:
                condicion = random.choice(['Fallecido', 'Traslado', 'Mejorado'])
            elif dias_estancia > 15:
                condicion = random.choice(['Mejorado', 'Alta médica', 'Traslado'])
            else:
                condicion = random.choice(['Mejorado', 'Alta médica'])
            
            record = {
                'desenlaceq_id': i + 1,
                'numero_episodio': i + 1000,
                'fecha_ingreso': fecha_ingreso.date(),
                'fecha_egreso': fecha_egreso.date() if fecha_egreso else None,
                'dias_estancia': dias_estancia,
                'diagnostico': random.choice(self.diagnosticos),
                'sala_egreso': random.choice(self.salas),
                'causa': random.choice(['Accidente doméstico', 'Accidente laboral', 'Accidente vehicular', 'Agresión', 'Intento suicidio', 'Otros']),
                'nombre_paciente': random.choice(self.nombres),
                'sexo': sexo,
                'edad': edad,
                'medico_tratante': random.choice(['Dr. García', 'Dra. Martínez', 'Dr. López', 'Dra. Rodríguez', 'Dr. Sánchez']),
                'numero_historia_clinica': f"HC{random.randint(100000, 999999)}",
                'nombre_aseguradora': random.choice(self.aseguradoras),
                'condicion_egreso_nombre': condicion,
                'fecha_procesamiento': datetime.now()
            }
            data.append(record)
        
        return pd.DataFrame(data)
    
    def generate_stats_aseguradora(self, desenlaces_df):
        """Genera estadísticas por aseguradora"""
        logger.info("Generando estadísticas por aseguradora...")
        
        stats = desenlaces_df.groupby('nombre_aseguradora').agg({
            'desenlaceq_id': 'count',
            'dias_estancia': 'mean'
        }).reset_index()
        
        stats.columns = ['nombre_aseguradora', 'total_casos', 'promedio_estancia']
        
        # Calcular casos mejorados y fallecidos
        mejoras = desenlaces_df[desenlaces_df['condicion_egreso_nombre'].isin(['Mejorado', 'Alta médica'])].groupby('nombre_aseguradora').size().to_dict()
        fallecidos = desenlaces_df[desenlaces_df['condicion_egreso_nombre'] == 'Fallecido'].groupby('nombre_aseguradora').size().to_dict()
        
        stats['casos_mejorados'] = stats['nombre_aseguradora'].map(mejoras).fillna(0).astype(int)
        stats['casos_fallecidos'] = stats['nombre_aseguradora'].map(fallecidos).fillna(0).astype(int)
        stats['promedio_estancia'] = stats['promedio_estancia'].round(1)
        stats['fecha_procesamiento'] = datetime.now()
        
        return stats
    
    def generate_stats_mensual(self, desenlaces_df):
        """Genera estadísticas mensuales"""
        logger.info("Generando estadísticas mensuales...")
        
        desenlaces_df['año'] = desenlaces_df['fecha_ingreso'].dt.year
        desenlaces_df['mes'] = desenlaces_df['fecha_ingreso'].dt.month
        
        stats = desenlaces_df.groupby(['año', 'mes']).agg({
            'desenlaceq_id': 'count',
            'dias_estancia': 'mean'
        }).reset_index()
        
        stats.columns = ['año', 'mes', 'total_ingresos', 'promedio_estancia']
        
        # Calcular casos mejorados y fallecidos por mes
        mejoras_mes = desenlaces_df[desenlaces_df['condicion_egreso_nombre'].isin(['Mejorado', 'Alta médica'])].groupby(['año', 'mes']).size().to_dict()
        fallecidos_mes = desenlaces_df[desenlaces_df['condicion_egreso_nombre'] == 'Fallecido'].groupby(['año', 'mes']).size().to_dict()
        
        stats['casos_mejorados'] = stats.apply(lambda x: mejoras_mes.get((x['año'], x['mes']), 0), axis=1)
        stats['casos_fallecidos'] = stats.apply(lambda x: fallecidos_mes.get((x['año'], x['mes']), 0), axis=1)
        stats['promedio_estancia'] = stats['promedio_estancia'].round(1)
        stats['fecha_procesamiento'] = datetime.now()
        
        return stats
    
    def generate_stats_demografia(self, desenlaces_df):
        """Genera estadísticas demográficas"""
        logger.info("Generando estadísticas demográficas...")
        
        # Categorizar edades
        def categorizar_edad(edad):
            if edad < 18:
                return 'Menor de 18'
            elif 18 <= edad <= 30:
                return '18-30'
            elif 31 <= edad <= 50:
                return '31-50'
            elif 51 <= edad <= 70:
                return '51-70'
            else:
                return 'Mayor de 70'
        
        desenlaces_df['rango_edad'] = desenlaces_df['edad'].apply(categorizar_edad)
        
        stats = desenlaces_df.groupby(['sexo', 'rango_edad']).agg({
            'desenlaceq_id': 'count',
            'dias_estancia': 'mean'
        }).reset_index()
        
        stats.columns = ['sexo', 'rango_edad', 'total_casos', 'promedio_estancia']
        stats['promedio_estancia'] = stats['promedio_estancia'].round(1)
        stats['fecha_procesamiento'] = datetime.now()
        
        return stats
    
    def load_sample_data(self):
        """Carga todos los datos de ejemplo"""
        try:
            logger.info("Iniciando carga de datos de ejemplo...")
            
            # 1. Generar datos de desenlaces
            desenlaces_df = self.generate_desenlaces_data(150)
            
            # 2. Generar estadísticas
            stats_aseg = self.generate_stats_aseguradora(desenlaces_df)
            stats_mensual = self.generate_stats_mensual(desenlaces_df)
            stats_demo = self.generate_stats_demografia(desenlaces_df)
            
            # 3. Cargar en base de datos
            logger.info("Cargando datos en PostgreSQL...")
            
            success1 = self.postgres.load_data(desenlaces_df, 'dashboard_desenlaces')
            success2 = self.postgres.load_data(stats_aseg, 'dashboard_stats_aseguradora')  
            success3 = self.postgres.load_data(stats_mensual, 'dashboard_stats_mensual')
            success4 = self.postgres.load_data(stats_demo, 'dashboard_stats_demografia')
            
            if all([success1, success2, success3, success4]):
                logger.info("✅ Datos de ejemplo cargados exitosamente!")
                logger.info(f"📊 Estadísticas:")
                logger.info(f"   - {len(desenlaces_df)} desenlaces")
                logger.info(f"   - {len(stats_aseg)} aseguradoras")
                logger.info(f"   - {len(stats_mensual)} meses")
                logger.info(f"   - {len(stats_demo)} grupos demográficos")
                return True
            else:
                logger.error("❌ Error cargando algunos datos")
                return False
                
        except Exception as e:
            logger.error(f"Error generando datos de ejemplo: {e}")
            return False
        finally:
            self.postgres.close()

def main():
    """Función principal"""
    logger.info("=== Generador de Datos de Ejemplo - Dashboard Médico ===")
    
    generator = SampleDataGenerator()
    success = generator.load_sample_data()
    
    if success:
        logger.info("🎉 ¡Datos de ejemplo listos! Tu dashboard ya tiene información para mostrar.")
        logger.info("💡 Ahora puedes desplegar el API y probar el frontend.")
    else:
        logger.error("❌ Error generando datos de ejemplo.")
        return False
    
    return success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
