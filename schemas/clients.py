from pydantic import BaseModel
#from typing import Optional

class ClientSchema(BaseModel):
    # id:Optional[int] Este dato generalmente no lo vamos a estar pasando, ya que es autoincrementable por la base de datos
    nombre_cliente:str
    correo:str
    telefono:int
    direccion:str