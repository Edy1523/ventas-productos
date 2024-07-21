from service.database_connection import Base
from sqlalchemy import Column, Integer, String

class Employees(Base):
    __tablename__ = "empleados"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(30), nullable=False)
    puesto = Column(String(15), nullable=False)
    salario = Column(Integer, nullable=False)
    fecha_contratacion = Column(String(15), nullable=False)