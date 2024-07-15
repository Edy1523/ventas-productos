import os
from dotenv import load_dotenv
from pathlib import Path
import psycopg2
import psycopg2.extras
from werkzeug.security import check_password_hash
from config.handle_db import HandleEmpleados, HandleProveedores
from werkzeug.security import generate_password_hash

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

DBNAME : str = os.getenv("DBNAME")
#USER : str = os.getenv("USER")
PASSWORD : str = os.getenv("PASSWORD")
HOST : str = os.getenv("HOST")
PORT : str = os.getenv("PORT")


class HandleLoginEmpleados:
    def __init__(self) -> None:
        try:
            self._conn = psycopg2.connect(f"dbname={DBNAME} user=postgres password={PASSWORD} host={HOST} port={PORT}")
            self._cur = self._conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        except psycopg2.OperationalError as err:
            print("\x1b[1;41mThe connection to the database hasn't been succesful\x1b[0;37m")
            print(err)
            self._conn.close()
            
    def insert(self, data, id_empleado):
        get_employee = HandleEmpleados().get_one(id_empleado)
        get_one = self.get_one(id_empleado)
        data["contrasena"] = generate_password_hash(data["contrasena"],'pbkdf2:sha256:15',15)
        if get_employee==None:
            return False
        elif get_one==None:
            self._cur.execute("INSERT INTO login_empleados(id_empleado, contrasena) VALUES ('{}','{}')".format(
                id_empleado,
                data["contrasena"]
            ))
            self._conn.commit()
            return True
        return None
    
    def get_one(self, id_empleado):
        self._cur.execute("""
            SELECT * FROM "login_empleados" WHERE id_empleado=%s              
            """,(id_empleado,))
        return self._cur.fetchone()
    
    def check_password(self, id_empleado, password):
        get_employee = self.get_one(id_empleado)
        if get_employee:
            same_password = check_password_hash(get_employee["contrasena"],password["contrasena"])
            if same_password:
                return True
            return False
        return None
    
class HandleLoginProveedores:
    def __init__(self) -> None:
        try:
            self._conn = psycopg2.connect(f"dbname={DBNAME} user=postgres password={PASSWORD} host={HOST} port={PORT}")
            self._cur = self._conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        except psycopg2.OperationalError as err:
            print("\x1b[1;41mThe connection to the database hasn't been succesful\x1b[0;37m")
            print(err)
            self._conn.close()
            
    def insert(self, data, id_proveedor):
        get_supplier = HandleProveedores().get_one(id_proveedor)
        get_one = self.get_one(id_proveedor)
        data["contrasena"] = generate_password_hash(data["contrasena"],'pbkdf2:sha256:15',15)
        if get_supplier==None:
            return False
        elif get_one==None:
            self._cur.execute("INSERT INTO login_proveedores(id_proveedor, contrasena) VALUES ('{}','{}')".format(
                id_proveedor,
                data["contrasena"]
            ))
            self._conn.commit()
            return True
        return None
    
    def get_one(self, id_proveedor):
        self._cur.execute("""
            SELECT * FROM "login_proveedores" WHERE id_proveedor=%s              
            """,(id_proveedor,))
        return self._cur.fetchone()
    
    def check_password(self, id_proveedor, password):
        get_supplier = self.get_one(id_proveedor)
        if get_supplier:
            same_password = check_password_hash(get_supplier["contrasena"],password["contrasena"])
            if same_password:
                return True
            return False
        return None
            