from service.database_connection import Base
from sqlalchemy import Column, Integer, String, ForeignKey

class LoginEmployees(Base):
    __tablename__ = "login_empleados"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_empleado = Column(Integer, ForeignKey("empleados.id"), nullable=False)
    contrasena = Column(String(100), nullable=False)