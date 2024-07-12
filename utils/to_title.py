#Este archivo sera especificamente para convertir los parametros de estado de entrega, en la primera letra de cada palabra en mayuscula
#Para que el cliente pueda filtrar por estado de envio y asi saber que productos estan por llegar o cuales o no
def to_title(x:str) -> str:
    return x.title()