from service.database_connection import Base
from sqlalchemy import Column, Integer, String, ForeignKey

class Orders(Base):
    __tablename__ = "pedidos"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    fecha_pedido = Column(String(20), nullable=False)
    estado_pedido = Column(String(25), nullable=False)
    monto_total = Column(Integer, nullable=False)
    cantidad_comprada = Column(Integer, nullable=False)
    id_cliente = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    id_producto = Column(Integer, ForeignKey("productos.id"), nullable=False)