from service.database_connection import Base
from sqlalchemy import Column, Integer, String

class Products(Base):
    __tablename__ = "productos"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre_producto = Column(String(25), nullable=False)
    descripcion = Column(String(50), nullable=False)
    precio = Column(Integer, nullable=False)