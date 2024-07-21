from service.database_connection import Base
from sqlalchemy import Column, Integer, String, ForeignKey

class Deliveries(Base):
    __tablename__ = "entregas"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    fecha_entrega = Column(String(25), nullable=False)
    direccion_entrega = Column(String(25), nullable=False)
    estado_entrega = Column(String(25), nullable=False)
    id_pedido = Column(Integer, ForeignKey("pedidos.id"), nullable=False)