from sqlalchemy import Column, Integer, String

class Clients:
    __tablename__ = "clients"
    
    id = Column(Integer, primary_key=True,autoincrement=True)
    nombre = Column(String)
    telefono = Column(Integer)