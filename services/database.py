import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import logging
from config.settings import settings

logger = logging.getLogger(__name__)

class DatabaseService:
    def __init__(self):
        self.engine = None
        self.SessionLocal = None
        self.connection_string = settings.postgres_url
        self._connect()
    
    def _connect(self):
        """Establece conexión con PostgreSQL"""
        try:
            self.engine = create_engine(self.connection_string)
            self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
            logger.info("Conexión establecida con PostgreSQL")
        except Exception as e:
            logger.error(f"Error conectando a PostgreSQL: {e}")
            raise
    
    def get_session(self):
        """Obtiene una sesión de base de datos"""
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()
    
    def execute_query(self, query, params=None):
        """Ejecuta una consulta y retorna DataFrame"""
        try:
            if params:
                df = pd.read_sql_query(query, self.engine, params=params)
            else:
                df = pd.read_sql_query(query, self.engine)
            return df
        except Exception as e:
            logger.error(f"Error ejecutando consulta: {e}")
            return pd.DataFrame()
    
    def get_desenlaces(self, filtros=None):
        """Obtiene datos de desenlaces con filtros opcionales"""
        query = """
        SELECT 
            id,
            desenlaceq_id,
            numero_episodio,
            fecha_ingreso,
            fecha_egreso,
            dias_estancia,
            diagnostico,
            sala_egreso,
            causa,
            nombre_paciente,
            sexo,
            edad,
            medico_tratante,
            numero_historia_clinica,
            nombre_aseguradora,
            condicion_egreso_nombre,
            fecha_procesamiento
        FROM dashboard_desenlaces
        WHERE 1=1
        """
        
        params = {}
        
        if filtros:
            if filtros.get('fecha_inicio'):
                query += " AND fecha_ingreso >= %(fecha_inicio)s"
                params['fecha_inicio'] = filtros['fecha_inicio']
            
            if filtros.get('fecha_fin'):
                query += " AND fecha_ingreso <= %(fecha_fin)s"
                params['fecha_fin'] = filtros['fecha_fin']
            
            if filtros.get('aseguradora'):
                query += " AND nombre_aseguradora ILIKE %(aseguradora)s"
                params['aseguradora'] = f"%{filtros['aseguradora']}%"
            
            if filtros.get('sexo'):
                query += " AND sexo = %(sexo)s"
                params['sexo'] = filtros['sexo']
            
            if filtros.get('edad_min'):
                query += " AND edad >= %(edad_min)s"
                params['edad_min'] = filtros['edad_min']
            
            if filtros.get('edad_max'):
                query += " AND edad <= %(edad_max)s"
                params['edad_max'] = filtros['edad_max']
            
            if filtros.get('condicion_egreso'):
                query += " AND condicion_egreso_nombre ILIKE %(condicion_egreso)s"
                params['condicion_egreso'] = f"%{filtros['condicion_egreso']}%"
        
        query += " ORDER BY fecha_ingreso DESC LIMIT 1000"
        
        return self.execute_query(query, params)
    
    def get_estadisticas_aseguradoras(self):
        """Obtiene estadísticas por aseguradora"""
        query = """
        SELECT 
            nombre_aseguradora,
            total_casos,
            promedio_estancia,
            casos_mejorados,
            casos_fallecidos
        FROM dashboard_stats_aseguradora
        ORDER BY total_casos DESC
        """
        return self.execute_query(query)
    
    def get_estadisticas_mensuales(self):
        """Obtiene estadísticas mensuales"""
        query = """
        SELECT 
            año,
            mes,
            total_ingresos,
            promedio_estancia,
            casos_mejorados,
            casos_fallecidos
        FROM dashboard_stats_mensual
        ORDER BY año DESC, mes DESC
        LIMIT 12
        """
        return self.execute_query(query)
    
    def get_estadisticas_demografia(self):
        """Obtiene estadísticas demográficas"""
        query = """
        SELECT 
            sexo,
            rango_edad,
            total_casos,
            promedio_estancia
        FROM dashboard_stats_demografia
        ORDER BY sexo, rango_edad
        """
        return self.execute_query(query)
    
    def get_dashboard_summary(self):
        """Obtiene resumen para el dashboard"""
        try:
            # Total de pacientes únicos
            total_pacientes_query = """
            SELECT COUNT(DISTINCT numero_historia_clinica) as total
            FROM dashboard_desenlaces
            WHERE numero_historia_clinica IS NOT NULL
            """
            
            # Ingresos del mes actual
            ingresos_mes_query = """
            SELECT COUNT(*) as total
            FROM dashboard_desenlaces
            WHERE EXTRACT(MONTH FROM fecha_ingreso) = EXTRACT(MONTH FROM CURRENT_DATE)
            AND EXTRACT(YEAR FROM fecha_ingreso) = EXTRACT(YEAR FROM CURRENT_DATE)
            """
            
            # Promedio de estancia
            promedio_estancia_query = """
            SELECT AVG(dias_estancia) as promedio
            FROM dashboard_desenlaces
            WHERE dias_estancia IS NOT NULL
            """
            
            # Tasa de mortalidad
            mortalidad_query = """
            SELECT 
                COUNT(*) as total,
                COUNT(CASE WHEN condicion_egreso_nombre ILIKE '%fallecido%' THEN 1 END) as fallecidos
            FROM dashboard_desenlaces
            WHERE condicion_egreso_nombre IS NOT NULL
            """
            
            # Casos activos (sin fecha de egreso)
            casos_activos_query = """
            SELECT COUNT(*) as total
            FROM dashboard_desenlaces
            WHERE fecha_egreso IS NULL
            """
            
            total_pacientes = self.execute_query(total_pacientes_query).iloc[0]['total'] if not self.execute_query(total_pacientes_query).empty else 0
            ingresos_mes = self.execute_query(ingresos_mes_query).iloc[0]['total'] if not self.execute_query(ingresos_mes_query).empty else 0
            promedio_estancia = self.execute_query(promedio_estancia_query).iloc[0]['promedio'] if not self.execute_query(promedio_estancia_query).empty else 0
            casos_activos = self.execute_query(casos_activos_query).iloc[0]['total'] if not self.execute_query(casos_activos_query).empty else 0
            
            mortalidad_df = self.execute_query(mortalidad_query)
            tasa_mortalidad = 0
            if not mortalidad_df.empty and mortalidad_df.iloc[0]['total'] > 0:
                tasa_mortalidad = (mortalidad_df.iloc[0]['fallecidos'] / mortalidad_df.iloc[0]['total']) * 100
            
            return {
                'total_pacientes': int(total_pacientes) if total_pacientes else 0,
                'total_ingresos_mes': int(ingresos_mes) if ingresos_mes else 0,
                'promedio_estancia': float(promedio_estancia) if promedio_estancia else 0.0,
                'tasa_mortalidad': round(float(tasa_mortalidad), 2) if tasa_mortalidad else 0.0,
                'casos_activos': int(casos_activos) if casos_activos else 0
            }
            
        except Exception as e:
            logger.error(f"Error obteniendo resumen del dashboard: {e}")
            return {
                'total_pacientes': 0,
                'total_ingresos_mes': 0,
                'promedio_estancia': 0.0,
                'tasa_mortalidad': 0.0,
                'casos_activos': 0
            }

# Instancia global del servicio de base de datos
db_service = DatabaseService()
