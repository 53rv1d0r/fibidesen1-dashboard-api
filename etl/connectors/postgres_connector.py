import pandas as pd
from sqlalchemy import create_engine, text
import logging
from config.settings import settings

logger = logging.getLogger(__name__)

class PostgresConnector:
    def __init__(self):
        self.engine = None
        self.connection_string = settings.postgres_url
    
    def connect(self):
        """Establece conexión con PostgreSQL en Render"""
        try:
            self.engine = create_engine(self.connection_string)
            logger.info("Conexión establecida con PostgreSQL - Render")
            return True
        except Exception as e:
            logger.error(f"Error conectando a PostgreSQL: {e}")
            return False
    
    def create_tables(self):
        """Crea las tablas necesarias para el dashboard"""
        try:
            if not self.engine:
                self.connect()
            
            # Tabla para datos de desenlaces procesados
            create_desenlaces_table = text("""
                CREATE TABLE IF NOT EXISTS dashboard_desenlaces (
                    id SERIAL PRIMARY KEY,
                    desenlaceq_id INTEGER,
                    numero_episodio INTEGER,
                    fecha_ingreso DATE,
                    fecha_egreso DATE,
                    dias_estancia INTEGER,
                    diagnostico TEXT,
                    sala_egreso VARCHAR(100),
                    causa TEXT,
                    nombre_paciente VARCHAR(200),
                    sexo VARCHAR(10),
                    edad INTEGER,
                    medico_tratante VARCHAR(200),
                    numero_historia_clinica VARCHAR(50),
                    nombre_aseguradora VARCHAR(200),
                    condicion_egreso_nombre VARCHAR(100),
                    fecha_procesamiento TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Tabla para estadísticas por aseguradora
            create_stats_aseguradora_table = text("""
                CREATE TABLE IF NOT EXISTS dashboard_stats_aseguradora (
                    id SERIAL PRIMARY KEY,
                    nombre_aseguradora VARCHAR(200),
                    total_casos INTEGER,
                    promedio_estancia DECIMAL(10,2),
                    casos_mejorados INTEGER,
                    casos_fallecidos INTEGER,
                    fecha_procesamiento TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Tabla para estadísticas mensuales
            create_stats_mensual_table = text("""
                CREATE TABLE IF NOT EXISTS dashboard_stats_mensual (
                    id SERIAL PRIMARY KEY,
                    año INTEGER,
                    mes INTEGER,
                    total_ingresos INTEGER,
                    promedio_estancia DECIMAL(10,2),
                    casos_mejorados INTEGER,
                    casos_fallecidos INTEGER,
                    fecha_procesamiento TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Tabla para estadísticas por edad y sexo
            create_stats_demografia_table = text("""
                CREATE TABLE IF NOT EXISTS dashboard_stats_demografia (
                    id SERIAL PRIMARY KEY,
                    sexo VARCHAR(10),
                    rango_edad VARCHAR(20),
                    total_casos INTEGER,
                    promedio_estancia DECIMAL(10,2),
                    fecha_procesamiento TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            with self.engine.connect() as connection:
                connection.execute(create_desenlaces_table)
                connection.execute(create_stats_aseguradora_table)
                connection.execute(create_stats_mensual_table)
                connection.execute(create_stats_demografia_table)
                connection.commit()
            
            logger.info("Tablas creadas exitosamente en PostgreSQL")
            return True
            
        except Exception as e:
            logger.error(f"Error creando tablas: {e}")
            return False
    
    def load_data(self, df, table_name, if_exists='replace'):
        """Carga datos a PostgreSQL"""
        try:
            if not self.engine:
                self.connect()
            
            # Limpiar tabla antes de insertar nuevos datos
            if if_exists == 'replace':
                with self.engine.connect() as connection:
                    connection.execute(text(f"DELETE FROM {table_name}"))
                    connection.commit()
            
            df.to_sql(table_name, self.engine, if_exists='append', index=False)
            logger.info(f"Cargados {len(df)} registros en tabla {table_name}")
            return True
            
        except Exception as e:
            logger.error(f"Error cargando datos en tabla {table_name}: {e}")
            return False
    
    def get_data(self, query):
        """Extrae datos de PostgreSQL"""
        try:
            if not self.engine:
                self.connect()
            
            df = pd.read_sql_query(query, self.engine)
            return df
            
        except Exception as e:
            logger.error(f"Error extrayendo datos: {e}")
            return pd.DataFrame()
    
    def close(self):
        """Cierra la conexión"""
        if self.engine:
            self.engine.dispose()
            logger.info("Conexión cerrada con PostgreSQL")
