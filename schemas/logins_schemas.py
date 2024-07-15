from pydantic import BaseModel, Field

class LoginEmpleadosSchema(BaseModel):
    contrasena:str = Field(min_length=5, max_length=40)
    
    class Config:
        json_schema_extra = {
            "example":{
                "contrasena":''
            }            
        }
        
class LoginProveedoresSchema(BaseModel):
    contrasena:str = Field(min_length=5, max_length=40)
    
    class Config:
        json_schema_extra = {
            "example":{
                "contrasena":''
            }            
        }