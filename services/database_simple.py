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
    
    def execute_query(self, query, params=None):
        """Ejecuta una consulta y retorna lista de diccionarios"""
        try:
            with self.engine.connect() as conn:
                if params:
                    result = conn.execute(text(query), params)
                else:
                    result = conn.execute(text(query))
                
                # Convertir a lista de diccionarios
                columns = result.keys()
                rows = result.fetchall()
                return [dict(zip(columns, row)) for row in rows]
        except Exception as e:
            logger.error(f"Error ejecutando consulta: {e}")
            return []
    
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
            nombre_paciente,
            sexo,
            edad,
            nombre_aseguradora,
            condicion_egreso_nombre,
            fecha_procesamiento
        FROM dashboard_desenlaces
        WHERE 1=1
        ORDER BY fecha_ingreso DESC LIMIT 100
        """
        
        return self.execute_query(query)
    
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
            total_pacientes = self.execute_query("""
                SELECT COUNT(DISTINCT numero_historia_clinica) as total
                FROM dashboard_desenlaces
                WHERE numero_historia_clinica IS NOT NULL
            """)
            
            # Ingresos del mes actual
            ingresos_mes = self.execute_query("""
                SELECT COUNT(*) as total
                FROM dashboard_desenlaces
                WHERE EXTRACT(MONTH FROM fecha_ingreso) = EXTRACT(MONTH FROM CURRENT_DATE)
                AND EXTRACT(YEAR FROM fecha_ingreso) = EXTRACT(YEAR FROM CURRENT_DATE)
            """)
            
            # Promedio de estancia
            promedio_estancia = self.execute_query("""
                SELECT AVG(dias_estancia) as promedio
                FROM dashboard_desenlaces
                WHERE dias_estancia IS NOT NULL
            """)
            
            # Casos activos
            casos_activos = self.execute_query("""
                SELECT COUNT(*) as total
                FROM dashboard_desenlaces
                WHERE fecha_egreso IS NULL
            """)
            
            # Tasa de mortalidad
            mortalidad = self.execute_query("""
                SELECT 
                    COUNT(*) as total,
                    COUNT(CASE WHEN condicion_egreso_nombre ILIKE '%fallecido%' THEN 1 END) as fallecidos
                FROM dashboard_desenlaces
                WHERE condicion_egreso_nombre IS NOT NULL
            """)
            
            # Extraer valores
            total_pac = total_pacientes[0]['total'] if total_pacientes else 0
            ing_mes = ingresos_mes[0]['total'] if ingresos_mes else 0
            prom_est = promedio_estancia[0]['promedio'] if promedio_estancia else 0
            activos = casos_activos[0]['total'] if casos_activos else 0
            
            tasa_mort = 0
            if mortalidad and mortalidad[0]['total'] > 0:
                tasa_mort = (mortalidad[0]['fallecidos'] / mortalidad[0]['total']) * 100
            
            return {
                'total_pacientes': int(total_pac) if total_pac else 0,
                'total_ingresos_mes': int(ing_mes) if ing_mes else 0,
                'promedio_estancia': float(prom_est) if prom_est else 0.0,
                'tasa_mortalidad': round(float(tasa_mort), 2) if tasa_mort else 0.0,
                'casos_activos': int(activos) if activos else 0
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