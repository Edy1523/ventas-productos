from service.database_connection import Base
from sqlalchemy import Column, Integer, String, ForeignKey

class LoginEmployees(Base):
    __tablename__ = "login_proveedores"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_proveedor = Column(Integer, ForeignKey("proveedores.id"), nullable=False)
    contrasena = Column(String(100), nullable=False)