from service.database_connection import Base
from sqlalchemy import Column, Integer, String, BIGINT

class Clients(Base):
    __tablename__ = "clientes"
    
    id = Column(Integer, primary_key=True,autoincrement=True)
    nombre_cliente = Column(String(30), nullable=False)
    correo = Column(String(25), nullable=False)
    telefono = Column(BIGINT)
    direccion = Column(String(30), nullable=False)