from service.database_connection import Base
from sqlalchemy import Column, Integer, String, ForeignKey

class ErrorDeliveryDescription(Base):
    __tablename__ = "error_entrega_decripcion"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    descripcion = Column(String(50), nullable=False)
    tiempo_solucion = Column(String(10), nullable=False)
    id_entrega = Column(Integer, ForeignKey("entregas.id"), nullable=False)