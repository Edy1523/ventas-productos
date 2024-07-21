from service.database_connection import Base
from sqlalchemy import Column, Integer, String, ForeignKey

class Inventories(Base):
    __tablename__ = "inventarios"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    cantidad = Column(Integer, nullable=False)
    ubicacion = Column(String(25), nullable=False)
    id_producto = Column(Integer, ForeignKey("productos.id"), nullable=False)