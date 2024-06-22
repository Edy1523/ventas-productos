import os
from dotenv import load_dotenv
from pathlib import Path
import psycopg

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

DBNAME : str = os.getenv("DBNAME")
#USER : str = os.getenv("USER")
PASSWORD : str = os.getenv("PASSWORD")
HOST : str = os.getenv("HOST")
PORT : str = os.getenv("PORT")

class HandleClientes:
    def __init__(self):
        try:
            self._conn = psycopg.connect(f"dbname={DBNAME} user=postgres password={PASSWORD} host={HOST} port={PORT}")
            self._cur = self._conn.cursor()
        except psycopg.OperationalError as err:
            print("\x1b[1;41m No se hizo la conexion a la db\x1b[0;37m")
            print(err)
            self.conn.close()
        
    def insert(self, data):
        self._cur.execute("""
            INSERT INTO "clientes"(nombre_cliente, correo, telefono, direccion) VALUES (%(nombre_cliente)s,%(correo)s,%(telefono)s,%(direccion)s)
            """, data)
        self._conn.commit()
        
    def __del__(self): #Destructor que cierra la conexion con la base de datos
        self._conn.close()