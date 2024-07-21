from service.database_connection import Base
from sqlalchemy import Column, Integer, String, BIGINT

class Suppliers(Base):
    __tablename__ = "proveedores"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre_proveedor = Column(String(30), nullable=False)
    telefono = Column(BIGINT, nullable=False)
    direccion_proveedor = Column(String(20), nullable=False)