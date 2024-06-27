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
            print("\x1b[1;41mThe connection to the database hasn't been succesful\x1b[0;37m")
            print(err)
            self._conn.close()
        
    def insert(self, data):
        try:
            self._cur.execute("""
                INSERT INTO "clientes"(id, nombre_cliente, correo, telefono, direccion) VALUES (%(id)s,%(nombre_cliente)s,%(correo)s,%(telefono)s,%(direccion)s)
                """, data)
            self._conn.commit()
            return True
        except psycopg.errors.UniqueViolation:
            self._conn.rollback()
            return False
        
    def get_all(self):
        self._cur.execute("""
            SELECT * FROM "clientes"              
            """)
        return self._cur.fetchall()
    
    def get_one(self, id):
        get_client = self._cur.execute("""
            SELECT * FROM "clientes" WHERE id = %s
            """,(id,))
        return get_client.fetchone()
    
    def update(self, id, data):
        get_client = self.get_one(id)
        if get_client:
            update_client = self._cur.execute("UPDATE clientes SET id = '{}', nombre_cliente = '{}', correo = '{}', telefono = '{}', direccion = '{}' WHERE id = '{}'".format(
                data["id"],
                data["nombre_cliente"],
                data["correo"],
                data["telefono"],
                data["direccion"],
                id
                ))
            self._conn.commit()
            return update_client
        return None
    
    def delete(self,id):
        get_client = self.get_one(id)
        if get_client:
            delete_client = self._cur.execute("""
                DELETE FROM "clientes" WHERE id = %s                              
                """, (id,))
            self._conn.commit()
            return delete_client
        return None
    
    def __del__(self): #Destructor que cierra la conexion con la base de datos
        self._conn.close()
        
class HandleEmpleados:
    def __init__(self) -> None:
        try:
            self._conn = psycopg.connect(f"dbname={DBNAME} user=postgres password={PASSWORD} host={HOST} port={PORT}")
            self._cur = self._conn.cursor()
        except psycopg.OperationalError as err:
            print("\x1b[1;41mThe connection to the database hasn't been succesful\x1b[0;37m")
            print(err)
            self._conn.close()
            
    def insert(self, data): #SQL para registrar empleados dentro de la base de datos, traidos de la web
        try:
            self._cur.execute("""
                INSERT INTO "empleados"(id, nombre, puesto, salario, fecha_contratacion) VALUES (%(id)s,%(nombre)s,%(puesto)s,%(salario)s,%(fecha_contratacion)s)
                """,data)
            self._conn.commit()
            return True
        except psycopg.errors.UniqueViolation:
            self._conn.rollback()
            return False
    
    def get_all(self):
        get_employees = self._cur.execute("""
            SELECT * FROM "empleados"
            """)
        return get_employees.fetchall()
        
    def get_one(self,id):
        get_employe = self._cur.execute("""
            SELECT * FROM "empleados" WHERE id = %s
            """,(id,))
        return get_employe.fetchone()
    
    def update(self, id, data):
        get_employee = self.get_one(id)
        if get_employee:
            update_employee = self._cur.execute("UPDATE empleados SET id = '{}',nombre = '{}', puesto = '{}', salario = '{}', fecha_contratacion = '{}' WHERE id = '{}'".format(
                    data["id"],
                    data["nombre"],
                    data["puesto"],
                    data["salario"],
                    data["fecha_contratacion"],
                    id
                ))
            self._conn.commit()
            return update_employee
        return None
    
    def delete(self,id):
        get_employee = self.get_one(id)
        if get_employee:
            delete_employee = self._cur.execute("""
                DELETE FROM "empleados" WHERE id = %s                                
                """, (id,))
            self._conn.commit()
            return delete_employee
        return None
        
    def __del__(self):
        self._conn.close()
        
class HandleProveedores:
    def __init__(self) -> None:
        try:
            self._conn = psycopg.connect(f"dbname={DBNAME} user=postgres password={PASSWORD} host={HOST} port={PORT}")
            self._cur = self._conn.cursor()
        except psycopg.OperationalError as err:
            print("\x1b[1;41mThe connection to the database hasn't been succesful\x1b[0;37m")
            print(err)
            self._conn.close()
        
    def insert(self, data):
        try:
            self._cur.execute("""
                INSERT INTO "proveedores"(id, nombre_proveedor, telefono, direccion_proveedor) VALUES (%(id)s,%(nombre_proveedor)s,%(telefono)s,%(direccion_proveedor)s)
                """, data)
            self._conn.commit()
            return True
        except psycopg.errors.UniqueViolation:
            self._conn.rollback()
            return False
        
    def get_all(self):
        get_supliers = self._cur.execute("""
           SELECT * FROM "proveedores"                              
            """)
        return get_supliers.fetchall()
    
    def get_one(self,id):
        get_suplier = self._cur.execute("""
            SELECT * FROM "proveedores" WHERE id= %s                           
            """, (id,))
        return get_suplier.fetchone()
    
    def update(self, data, id):
        get_supplier = self.get_one(id)
        if get_supplier:
            update_supplier = self._cur.execute("UPDATE proveedores SET id = '{}', nombre_proveedor = '{}', telefono = '{}', direccion_proveedor = '{}' WHERE id = '{}'".format(
                data["id"],
                data["nombre_proveedor"],
                data["telefono"],
                data["direccion_proveedor"],
                id
            ))
            self._conn.commit()
            return update_supplier
        return None
    
    def delete(self, id):
        get_supplier = self.get_one(id)
        if get_supplier:
            delete_supplier = self._cur.execute("""
                DELETE FROM "proveedores" WHERE id = %s              
                """, (id,))
            self._conn.commit()
            return delete_supplier
        return None