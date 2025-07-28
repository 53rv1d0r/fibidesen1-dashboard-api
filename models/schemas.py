from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional, List
from decimal import Decimal

class DesenlaceBase(BaseModel):
    desenlaceq_id: int
    numero_episodio: int
    fecha_ingreso: date
    fecha_egreso: Optional[date] = None
    dias_estancia: Optional[int] = None
    diagnostico: Optional[str] = None
    sala_egreso: Optional[str] = None
    causa: Optional[str] = None
    nombre_paciente: str
    sexo: Optional[str] = None
    edad: Optional[int] = None
    medico_tratante: Optional[str] = None
    numero_historia_clinica: Optional[str] = None
    nombre_aseguradora: Optional[str] = None
    condicion_egreso_nombre: Optional[str] = None

class DesenlaceResponse(DesenlaceBase):
    id: int
    fecha_procesamiento: datetime
    
    class Config:
        from_attributes = True

class EstadisticaAseguradora(BaseModel):
    nombre_aseguradora: str
    total_casos: int
    promedio_estancia: Optional[Decimal] = None
    casos_mejorados: int
    casos_fallecidos: int

class EstadisticaMensual(BaseModel):
    año: int
    mes: int
    total_ingresos: int
    promedio_estancia: Optional[Decimal] = None
    casos_mejorados: int
    casos_fallecidos: int

class EstadisticaDemografia(BaseModel):
    sexo: str
    rango_edad: str
    total_casos: int
    promedio_estancia: Optional[Decimal] = None

class DashboardSummary(BaseModel):
    total_pacientes: int
    total_ingresos_mes: int
    promedio_estancia: float
    tasa_mortalidad: float
    casos_activos: int

class FiltroDesenlaces(BaseModel):
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None
    aseguradora: Optional[str] = None
    sexo: Optional[str] = None
    edad_min: Optional[int] = None
    edad_max: Optional[int] = None
    condicion_egreso: Optional[str] = None
