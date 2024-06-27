from pydantic import BaseModel, Field

class ClientesSchema(BaseModel):
    id:int = Field(ge=1000000)
    nombre_cliente:str = Field(min_length=1, max_length=30)
    correo:str = Field(min_length=10, max_length=25)
    telefono:int = Field(ge=3000000000)
    direccion:str  = Field(min_length=5, max_length=30)
    
    class Config:
        json_schema_extra = {
            "example":{
                "id":1000000,
                "nombre_cliente":"default",
                "correo":"ex@gmail.com",
                "telefono":3000000000,
                "direccion":"cr cll av #"
            }            
        }
    
class EmpleadosSchema(BaseModel):
    id:int = Field(ge=1000000)
    nombre:str = Field(min_length=1, max_length=30)
    puesto:str = Field(min_length=1, max_length=15)
    salario:int = Field(ge=500000)
    fecha_contratacion:str = Field(min_length=5, max_length=15)
    
    class Config:
        json_schema_extra = {
            "example":{
                "id":1000000,
                "nombre":"default",
                "puesto":"example",
                "salario":500000,
                "fecha_contratacion":"2000/00/00"
            }            
        }

class ProveedoresSchema(BaseModel):
    id:int = Field(ge=1000000)
    nombre_proveedor:str = Field(min_length=1, max_length=30)
    telefono:int = Field(ge=3000000000)
    direccion_proveedor:str = Field(min_length=1, max_length=20)
    
    class Config:
        json_schema_extra = {
            "example":{
                "id":1000000,
                "nombre_proveedor":"default",
                "telefono":3000000000,
                "direccion_proveedor":"cr cll av #"
            }            
        }