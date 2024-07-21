from service.database_connection import Base
from sqlalchemy import Column, Integer, String, ForeignKey

class Bills(Base):
    __tablename__ = "ordenes_compras"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    fecha_orden = Column(String(25), nullable=False)
    estado_orden = Column(String(15), nullable=False)
    id_cliente = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    id_proveedor = Column(Integer, ForeignKey("proveedores.id"), nullable=False)
    id_pedido = Column(Integer, ForeignKey("pedidos.id"), nullable=False)
    