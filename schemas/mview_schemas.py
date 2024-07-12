from pydantic import BaseModel, Field

class ErrorDeliveriesSchema(BaseModel):
    descripcion:str = Field(min_length=1, max_length=50)
    tiempo_solucion:str = Field(min_length=1, max_length=10)
    
    class Config:
        json_schema_extra = {
            "example":{
                "descripcion":"descripcion de por qué fallo el envio",
                "tiempo_solucion":"10 días"
            }
        }