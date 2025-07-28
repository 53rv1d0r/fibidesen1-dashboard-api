import pandas as pd
import pyodbc
from sqlalchemy import create_engine
import logging
from config.settings import settings

logger = logging.getLogger(__name__)

class SQLServerConnector:
    def __init__(self):
        self.engine = None
        self.connection_string = settings.sqlserver_url
    
    def connect(self):
        """Establece conexión con SQL Server - Base de datos fibidesen1"""
        try:
            self.engine = create_engine(self.connection_string)
            logger.info("Conexión establecida con SQL Server - fibidesen1")
            return True
        except Exception as e:
            logger.error(f"Error conectando a SQL Server fibidesen1: {e}")
            return False
    
    def extract_data(self, query):
        """Extrae datos usando una consulta SQL"""
        try:
            if not self.engine:
                self.connect()
            
            df = pd.read_sql_query(query, self.engine)
            logger.info(f"Extraídos {len(df)} registros de fibidesen1")
            return df
        except Exception as e:
            logger.error(f"Error extrayendo datos de fibidesen1: {e}")
            return pd.DataFrame()
    
    def get_desenlaces_data(self):
        """Extrae datos de desenlaces quemados con información completa"""
        query = """
        SELECT 
            dq.desenlaceq_id,
            dq.numero_episodio,
            dq.fecha_ingreso,
            dq.fecha_egreso,
            dq.condicion_egreso,
            dq.dias_estancia,
            dq.diagnostico,
            dq.sala_egreso,
            dq.aseguradora,
            dq.causa,
            a.nombre_aseguradora,
            ce.nombre_estado as condicion_egreso_nombre,
            e.nombre_paciente,
            e.sexo,
            e.edad,
            e.medico_tratante,
            e.numero_historia_clinica
        FROM desenlaces_quemados dq
        LEFT JOIN aseguradora a ON dq.aseguradora = a.aseguradora_id
        LEFT JOIN condicion_egreso ce ON dq.condicion_egreso = ce.condicion_egreso_id
        LEFT JOIN episodio e ON dq.numero_episodio = e.numero_episodio_id
        WHERE dq.fecha_ingreso >= DATEADD(day, -90, GETDATE())
        ORDER BY dq.fecha_ingreso DESC
        """
        return self.extract_data(query)
    
    def get_episodios_data(self):
        """Extrae datos de episodios médicos"""
        query = """
        SELECT 
            numero_episodio_id,
            nombre_paciente,
            sexo,
            edad,
            medico_tratante,
            numero_historia_clinica
        FROM episodio
        ORDER BY numero_episodio_id DESC
        """
        return self.extract_data(query)
    
    def get_aseguradoras_data(self):
        """Extrae datos de aseguradoras"""
        query = """
        SELECT 
            aseguradora_id,
            nombre_aseguradora
        FROM aseguradora
        ORDER BY nombre_aseguradora
        """
        return self.extract_data(query)
    
    def get_condiciones_egreso_data(self):
        """Extrae datos de condiciones de egreso"""
        query = """
        SELECT 
            condicion_egreso_id,
            nombre_estado
        FROM condicion_egreso
        ORDER BY nombre_estado
        """
        return self.extract_data(query)
    
    def get_estadisticas_por_aseguradora(self):
        """Genera estadísticas por aseguradora"""
        query = """
        SELECT 
            a.nombre_aseguradora,
            COUNT(dq.desenlaceq_id) as total_casos,
            AVG(CAST(dq.dias_estancia AS FLOAT)) as promedio_estancia,
            COUNT(CASE WHEN ce.nombre_estado = 'Mejorado' THEN 1 END) as casos_mejorados,
            COUNT(CASE WHEN ce.nombre_estado = 'Fallecido' THEN 1 END) as casos_fallecidos
        FROM desenlaces_quemados dq
        LEFT JOIN aseguradora a ON dq.aseguradora = a.aseguradora_id
        LEFT JOIN condicion_egreso ce ON dq.condicion_egreso = ce.condicion_egreso_id
        WHERE dq.fecha_ingreso >= DATEADD(day, -90, GETDATE())
        GROUP BY a.nombre_aseguradora
        ORDER BY total_casos DESC
        """
        return self.extract_data(query)
    
    def get_estadisticas_por_mes(self):
        """Genera estadísticas mensuales"""
        query = """
        SELECT 
            YEAR(dq.fecha_ingreso) as año,
            MONTH(dq.fecha_ingreso) as mes,
            COUNT(dq.desenlaceq_id) as total_ingresos,
            AVG(CAST(dq.dias_estancia AS FLOAT)) as promedio_estancia,
            COUNT(CASE WHEN ce.nombre_estado = 'Mejorado' THEN 1 END) as casos_mejorados,
            COUNT(CASE WHEN ce.nombre_estado = 'Fallecido' THEN 1 END) as casos_fallecidos
        FROM desenlaces_quemados dq
        LEFT JOIN condicion_egreso ce ON dq.condicion_egreso = ce.condicion_egreso_id
        WHERE dq.fecha_ingreso >= DATEADD(month, -12, GETDATE())
        GROUP BY YEAR(dq.fecha_ingreso), MONTH(dq.fecha_ingreso)
        ORDER BY año DESC, mes DESC
        """
        return self.extract_data(query)
    
    def get_estadisticas_por_edad_sexo(self):
        """Genera estadísticas por edad y sexo"""
        query = """
        SELECT 
            e.sexo,
            CASE 
                WHEN e.edad < 18 THEN 'Menor de 18'
                WHEN e.edad BETWEEN 18 AND 30 THEN '18-30'
                WHEN e.edad BETWEEN 31 AND 50 THEN '31-50'
                WHEN e.edad BETWEEN 51 AND 70 THEN '51-70'
                ELSE 'Mayor de 70'
            END as rango_edad,
            COUNT(dq.desenlaceq_id) as total_casos,
            AVG(CAST(dq.dias_estancia AS FLOAT)) as promedio_estancia
        FROM desenlaces_quemados dq
        LEFT JOIN episodio e ON dq.numero_episodio = e.numero_episodio_id
        WHERE dq.fecha_ingreso >= DATEADD(day, -90, GETDATE())
        GROUP BY e.sexo, 
                CASE 
                    WHEN e.edad < 18 THEN 'Menor de 18'
                    WHEN e.edad BETWEEN 18 AND 30 THEN '18-30'
                    WHEN e.edad BETWEEN 31 AND 50 THEN '31-50'
                    WHEN e.edad BETWEEN 51 AND 70 THEN '51-70'
                    ELSE 'Mayor de 70'
                END
        ORDER BY e.sexo, rango_edad
        """
        return self.extract_data(query)
    
    def close(self):
        """Cierra la conexión"""
        if self.engine:
            self.engine.dispose()
            logger.info("Conexión cerrada con SQL Server fibidesen1")
