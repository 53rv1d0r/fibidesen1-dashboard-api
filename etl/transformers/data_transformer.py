import pandas as pd
import numpy as np
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class DataTransformer:
    """Clase para transformar y limpiar datos médicos"""
    
    def clean_desenlaces_data(self, df):
        """Limpia y transforma datos de desenlaces"""
        try:
            logger.info(f"Iniciando limpieza de {len(df)} registros de desenlaces")
            
            # Hacer una copia para no modificar el original
            cleaned_df = df.copy()
            
            # Limpiar fechas
            date_columns = ['fecha_ingreso', 'fecha_egreso']
            for col in date_columns:
                if col in cleaned_df.columns:
                    cleaned_df[col] = pd.to_datetime(cleaned_df[col], errors='coerce')
            
            # Limpiar datos numéricos
            numeric_columns = ['edad', 'dias_estancia', 'desenlaceq_id', 'numero_episodio']
            for col in numeric_columns:
                if col in cleaned_df.columns:
                    cleaned_df[col] = pd.to_numeric(cleaned_df[col], errors='coerce')
            
            # Limpiar strings
            string_columns = ['nombre_paciente', 'diagnostico', 'sala_egreso', 'causa', 
                            'medico_tratante', 'nombre_aseguradora', 'condicion_egreso_nombre']
            for col in string_columns:
                if col in cleaned_df.columns:
                    cleaned_df[col] = cleaned_df[col].astype(str).str.strip()
                    cleaned_df[col] = cleaned_df[col].replace('nan', np.nan)
            
            # Normalizar sexo
            if 'sexo' in cleaned_df.columns:
                cleaned_df['sexo'] = cleaned_df['sexo'].str.upper().str.strip()
                cleaned_df['sexo'] = cleaned_df['sexo'].map({
                    'M': 'Masculino',
                    'F': 'Femenino',
                    'MASCULINO': 'Masculino',
                    'FEMENINO': 'Femenino',
                    'MALE': 'Masculino',
                    'FEMALE': 'Femenino'
                }).fillna(cleaned_df['sexo'])
            
            # Validar rangos de edad
            if 'edad' in cleaned_df.columns:
                cleaned_df.loc[cleaned_df['edad'] < 0, 'edad'] = np.nan
                cleaned_df.loc[cleaned_df['edad'] > 150, 'edad'] = np.nan
            
            # Validar días de estancia
            if 'dias_estancia' in cleaned_df.columns:
                cleaned_df.loc[cleaned_df['dias_estancia'] < 0, 'dias_estancia'] = np.nan
                cleaned_df.loc[cleaned_df['dias_estancia'] > 365, 'dias_estancia'] = np.nan
            
            # Eliminar registros completamente duplicados
            initial_count = len(cleaned_df)
            cleaned_df = cleaned_df.drop_duplicates()
            duplicates_removed = initial_count - len(cleaned_df)
            
            if duplicates_removed > 0:
                logger.info(f"Eliminados {duplicates_removed} registros duplicados")
            
            # Agregar metadata de procesamiento
            cleaned_df['fecha_procesamiento'] = datetime.now()
            
            logger.info(f"Limpieza completada. Registros finales: {len(cleaned_df)}")
            return cleaned_df
            
        except Exception as e:
            logger.error(f"Error limpiando datos de desenlaces: {e}")
            return df
    
    def calculate_mortality_rate(self, df):
        """Calcula tasa de mortalidad"""
        try:
            if 'condicion_egreso_nombre' not in df.columns:
                return 0
            
            total_cases = len(df)
            if total_cases == 0:
                return 0
            
            deaths = len(df[df['condicion_egreso_nombre'].str.contains('Fallecido', case=False, na=False)])
            mortality_rate = (deaths / total_cases) * 100
            
            return round(mortality_rate, 2)
            
        except Exception as e:
            logger.error(f"Error calculando tasa de mortalidad: {e}")
            return 0
    
    def calculate_average_stay(self, df):
        """Calcula estancia promedio"""
        try:
            if 'dias_estancia' not in df.columns:
                return 0
            
            avg_stay = df['dias_estancia'].mean()
            return round(avg_stay, 1) if not pd.isna(avg_stay) else 0
            
        except Exception as e:
            logger.error(f"Error calculando estancia promedio: {e}")
            return 0
    
    def categorize_age(self, age):
        """Categoriza edades en rangos"""
        try:
            if pd.isna(age):
                return 'No especificado'
            
            if age < 18:
                return 'Menor de 18'
            elif 18 <= age <= 30:
                return '18-30'
            elif 31 <= age <= 50:
                return '31-50'
            elif 51 <= age <= 70:
                return '51-70'
            else:
                return 'Mayor de 70'
                
        except Exception:
            return 'No especificado'
    
    def validate_data_quality(self, df, table_name):
        """Valida la calidad de los datos"""
        try:
            logger.info(f"Validando calidad de datos para tabla: {table_name}")
            
            total_rows = len(df)
            if total_rows == 0:
                logger.warning(f"No hay datos para validar en {table_name}")
                return False
            
            # Calcular porcentaje de valores nulos por columna
            null_percentages = (df.isnull().sum() / total_rows) * 100
            
            # Reportar columnas con más del 50% de valores nulos
            high_null_cols = null_percentages[null_percentages > 50]
            if not high_null_cols.empty:
                logger.warning(f"Columnas con >50% valores nulos en {table_name}: {high_null_cols.to_dict()}")
            
            # Validaciones específicas por tabla
            if table_name == 'dashboard_desenlaces':
                required_cols = ['desenlaceq_id', 'fecha_ingreso']
                missing_required = [col for col in required_cols if col not in df.columns or df[col].isnull().all()]
                if missing_required:
                    logger.error(f"Columnas requeridas faltantes en {table_name}: {missing_required}")
                    return False
            
            logger.info(f"Validación completada para {table_name}. Registros válidos: {total_rows}")
            return True
            
        except Exception as e:
            logger.error(f"Error validando calidad de datos: {e}")
            return False
