import os
from dotenv import load_dotenv
from pathlib import Path
import psycopg2
import psycopg2.extras

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

DBNAME : str = os.getenv("DBNAME")#''
#USER : str = os.getenv("USER")
PASSWORD : str = os.getenv("PASSWORD")
HOST : str = os.getenv("HOST")
PORT : str = os.getenv("PORT")

class HandleClientes:
    def __init__(self):
        try:
            self._conn = psycopg2.connect(f"dbname={DBNAME} user=postgres password={PASSWORD} host={HOST} port={PORT}")
            self._cur = self._conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        except psycopg2.OperationalError as err:
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
        except psycopg2.errors.UniqueViolation:
            self._conn.rollback()
            return False
        
    def get_all_by_addres(self, addres):
        self._cur.execute("""
            SELECT * FROM "clientes" WHERE direccion=%s
            """,(addres,))
        return self._cur.fetchall()
    
    def get_one(self, id):
        self._cur.execute("""
            SELECT * FROM "clientes" WHERE id = %s
            """,(id,))
        return self._cur.fetchone()
    
    def update(self, id, data):
        get_client = self.get_one(id)
        if get_client:
            self._cur.execute("UPDATE clientes SET id = '{}', nombre_cliente = '{}', correo = '{}', telefono = '{}', direccion = '{}' WHERE id = '{}'".format(
                data["id"],
                data["nombre_cliente"],
                data["correo"],
                data["telefono"],
                data["direccion"],
                id
                ))
            self._conn.commit()
            return True
        return None
    
    def delete(self,id):
        get_client = self.get_one(id)
        if get_client:
            self._cur.execute("""
                DELETE FROM "clientes" WHERE id = %s                              
                """, (id,))
            self._conn.commit()
            return True
        return None
    
    def __del__(self): #Destructor que cierra la conexion con la base de datos
        self._conn.close()
        
class HandleEmpleados:
    def __init__(self) -> None:
        try:
            self._conn = psycopg2.connect(f"dbname={DBNAME} user=postgres password={PASSWORD} host={HOST} port={PORT}")
            self._cur = self._conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        except psycopg2.OperationalError as err:
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
        except psycopg2.errors.UniqueViolation:
            self._conn.rollback()
            return False
    
    def get_all_by_charge(self, charge):
        self._cur.execute("""
            SELECT * FROM "empleados" WHERE puesto=%s
            """, (charge,))
        return self._cur.fetchall()
        
    def get_one(self,id):
        self._cur.execute("""
            SELECT * FROM "empleados" WHERE id = %s
            """,(id,))
        return self._cur.fetchone()
    
    def update(self, id, data):
        get_employee = self.get_one(id)
        if get_employee:
            self._cur.execute("UPDATE empleados SET id = '{}',nombre = '{}', puesto = '{}', salario = '{}', fecha_contratacion = '{}' WHERE id = '{}'".format(
                    data["id"],
                    data["nombre"],
                    data["puesto"],
                    data["salario"],
                    data["fecha_contratacion"],
                    id
                ))
            self._conn.commit()
            return True
        return None
    
    def delete(self,id):
        get_employee = self.get_one(id)
        if get_employee:
            self._cur.execute("""
                DELETE FROM "empleados" WHERE id = %s                                
                """, (id,))
            self._conn.commit()
            return True
        return None
        
    def __del__(self):
        self._conn.close()
        
class HandleProveedores:
    def __init__(self) -> None:
        try:
            self._conn = psycopg2.connect(f"dbname={DBNAME} user=postgres password={PASSWORD} host={HOST} port={PORT}")
            self._cur = self._conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        except psycopg2.OperationalError as err:
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
        except psycopg2.errors.UniqueViolation:
            self._conn.rollback()
            return False
        
    def get_all_by_addres(self, addres):
        self._cur.execute("""
           SELECT * FROM "proveedores" WHERE direccion_proveedor=%s
            """, (addres,))
        return self._cur.fetchall()
    
    def get_one(self,id):
        self._cur.execute("""
            SELECT * FROM "proveedores" WHERE id= %s                           
            """, (id,))
        return self._cur.fetchone()
    
    def update(self, data, id):
        get_supplier = self.get_one(id)
        if get_supplier:
            self._cur.execute("UPDATE proveedores SET id = '{}', nombre_proveedor = '{}', telefono = '{}', direccion_proveedor = '{}' WHERE id = '{}'".format(
                data["id"],
                data["nombre_proveedor"],
                data["telefono"],
                data["direccion_proveedor"],
                id
            ))
            self._conn.commit()
            return True
        return None
    
    def delete(self, id):
        get_supplier = self.get_one(id)
        if get_supplier:
            self._cur.execute("""
                DELETE FROM "proveedores" WHERE id = %s              
                """, (id,))
            self._conn.commit()
            return True
        return None
    
    def __del__(self):
        self._conn.close()
    
class HandleProductos:
    def __init__(self) -> None:
        try:
            self._conn = psycopg2.connect(f"dbname={DBNAME} user=postgres password={PASSWORD} host={HOST} port={PORT}")
            self._cur = self._conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        except psycopg2.OperationalError as err:
            print("\x1b[1;41mThe connection to the database hasn't been succesful\x1b[0;37m")
            print(err)
            self._conn.close()
    
    def insert(self, data):
        self._cur.execute("""
            INSERT INTO "productos"(nombre_producto, descripcion, precio) VALUES (%(nombre_producto)s, %(descripcion)s, %(precio)s)              
            """, data)
        self._conn.commit()
        
    def get_all(self):
        self._cur.execute("""
            SELECT * FROM "productos"                             
            """)
        return self._cur.fetchall()
    
    def get_one(self, nombre):
        self._cur.execute("""
            SELECT * FROM "productos" WHERE nombre_producto = %s                           
            """, (nombre,))
        return self._cur.fetchone()
    
    def update(self, data, nombre):
        get_product =  self.get_one(nombre)
        if get_product:
            self._cur.execute("UPDATE productos SET nombre_producto = '{}', descripcion = '{}', precio = '{}' WHERE nombre_producto = '{}'".format(
                data["nombre_producto"],
                data["descripcion"],
                data["precio"],
                nombre
            ))
            self._conn.commit()
            return True
        return None
    
    def delete(self, nombre): #Al eliminar un producto hay que validar que este llamado en una tabla de inventarios, para eliminarlo completamente
        get_product = self.get_one(nombre)
        inventory = HandleInventarios()
        get_inventory = inventory.get_one(nombre)
        get_id = self.get_id(nombre)
        if get_product and get_inventory:
            self._cur.execute("""
                DELETE FROM inventarios WHERE id_producto = %s;
                DELETE FROM "productos" WHERE nombre_producto = %s;              
                """, (get_id,nombre))
            self._conn.commit()
            return True
        elif get_product and get_inventory == None:
            self._cur.execute("""
                DELETE FROM "productos" WHERE nombre_producto = %s                
                """, (nombre,))
            self._conn.commit()
            return True
        return None
    
    def get_id(self, nombre):
        get_product = self.get_one(nombre)
        if get_product:
            self._cur.execute("""
                SELECT id FROM "productos" WHERE nombre_producto = %s              
                """, (nombre,))
            id = self._cur.fetchone()
            return id['id']
        return None
    
    def get_price(self, nombre):
        get_product = self.get_one(nombre)
        if get_product:
            self._cur.execute("""
                SELECT precio FROM "productos" WHERE nombre_producto = %s              
                """, (nombre,))
            id = self._cur.fetchone()
            return id['precio']
        return None
    
    def __del__(self):
        self._conn.close()
    
class HandleInventarios:
    def __init__(self) -> None:
        try:
            self._conn = psycopg2.connect(f"dbname={DBNAME} user=postgres password={PASSWORD} host={HOST} port={PORT}")
            self._cur = self._conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        except psycopg2.OperationalError as err:
            print("\x1b[1;41mThe connection to the database hasn't been succesful\x1b[0;37m")
            print(err)
            self._conn.close()
    
    def insert(self, data, nombre_producto):
        producto = HandleProductos()
        id_producto = producto.get_id(nombre_producto)
        get_inventory = self.get_one(nombre_producto)
        if id_producto == None:
            return False
        elif get_inventory == None:
            self._cur.execute("INSERT INTO inventarios(cantidad, ubicacion, id_producto) VALUES ('{}', '{}', '{}')".format(
                data["cantidad"],
                data["ubicacion"],
                id_producto
            ))
            self._conn.commit()
            return True
        return None
    
    def get_all(self, ubicacion):
        self._cur.execute("""
            SELECT * FROM "inventarios" WHERE ubicacion = %s                               
            """, (ubicacion,))
        return self._cur.fetchall()
    
    def get_one(self, nombre_producto):
        producto = HandleProductos()
        id_producto = producto.get_id(nombre_producto)
        if id_producto:
            self._cur.execute(" SELECT * FROM inventarios WHERE id_producto = {}".format(id_producto))
            return self._cur.fetchone()
        return None
    
    def update(self, data, nombre_producto):
        producto = HandleProductos()
        id_producto = producto.get_id(nombre_producto)
        if id_producto:
            self._cur.execute("UPDATE inventarios SET cantidad = '{}', ubicacion = '{}', id_producto = '{}' WHERE id_producto = '{}'".format(
                data["cantidad"],
                data["ubicacion"],
                id_producto,
                id_producto
            ))
            self._conn.commit()
            return True
        return None
    
    def update_stock(self, new_stock, nombre_producto):
        get_id_product = HandleProductos().get_id(nombre_producto)
        old_stock = self.get_one(nombre_producto)
        if get_id_product:
            if old_stock["cantidad"] > new_stock:
                actual_stock = old_stock["cantidad"] - new_stock
                self._cur.execute("UPDATE inventarios SET cantidad='{}' WHERE id_producto='{}'".format(
                    actual_stock,
                    get_id_product
                ))
                self._conn.commit()
                return True
            else: 
                return False
        return None
    
    def delete(self, nombre_producto):
        producto = HandleProductos()
        id_producto = producto.get_id(nombre_producto)
        if id_producto:
            self._cur.execute("DELETE FROM inventarios WHERE id_producto = {}".format(id_producto))
            self._conn.commit()
            return True
        return None
    
    def __del__(self):
        self._conn.close()

class HandlePedidos:
    def __init__(self) -> None:
        try:
            self._conn = psycopg2.connect(f"dbname={DBNAME} user=postgres password={PASSWORD} host={HOST} port={PORT}")
            self._cur = self._conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        except psycopg2.OperationalError as err:
            print("\x1b[1;41mThe connection to the database hasn't been succesful\x1b[0;37m")
            print(err)
            self._conn.close()
            
    def insert(self, data, id, nombre):
        id_producto = HandleProductos().get_id(nombre)
        get_client = HandleClientes().get_one(id)
        if id_producto and get_client:
            product_price = HandleProductos().get_price(nombre)
            monto_total = data["cantidad_comprada"] * product_price
            self._cur.execute("INSERT INTO pedidos(fecha_pedido, estado_pedido, monto_total, cantidad_comprada, id_cliente, id_producto) VALUES ('{}','{}','{}','{}','{}','{}') RETURNING id".format(
                data["fecha_pedido"],
                data["estado_pedido"],
                monto_total,
                data["cantidad_comprada"],
                id,
                id_producto
            ))
            update_stock = HandleInventarios().update_stock(data["cantidad_comprada"],nombre)
            if update_stock:
                self._conn.commit()
                return self._cur.fetchone()
            elif update_stock==False:
                self._conn.rollback()
                return False
            return None
        return None
    
    def get_one(self, id):
        self._cur.execute("""
            SELECT * FROM "pedidos" WHERE id=%s              
            """, (id,))
        return self._cur.fetchone()
    
    def get_by_client(self, id_cliente):
        self._cur.execute("""
            SELECT * FROM "pedidos" WHERE id_cliente=%s              
            """, (id_cliente,))
        return self._cur.fetchall()
    
    def get_by_date(self, date):
        self._cur.execute("""
            SELECT * FROM "pedidos" WHERE fecha_pedido=%s              
            """, (date,))
        return self._cur.fetchall()
    
    def get_by_product(self, nombre, id_cliente):
        id_producto = HandleProductos().get_id(nombre)
        if id_producto:
            self._cur.execute("""
            SELECT * FROM "pedidos" WHERE id_producto=%s AND id_cliente=%s             
            """, (id_producto,id_cliente))
            return self._cur.fetchall()
        return None
    
    def __del__(self):
        self._conn.close()
    
class HandleEntregas:
    def __init__(self) -> None:
        try:
            self._conn = psycopg2.connect(f"dbname={DBNAME} user=postgres password={PASSWORD} host={HOST} port={PORT}")
            self._cur = self._conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        except psycopg2.OperationalError as err:
            print("\x1b[1;41mThe connection to the database hasn't been succesful\x1b[0;37m")
            print(err)
            self._conn.close()
            
    def insert(self, data, id_pedido):
        get_order = HandlePedidos().get_one(id_pedido)
        get_by_order = self.get_by_order(id_pedido)
        if get_order == None:
            return False
        elif get_by_order==None:
            get_id_client = HandleClientes().get_one(get_order["id_cliente"])
            self._cur.execute("INSERT INTO entregas(fecha_entrega, direccion_entrega, estado_entrega, id_pedido) VALUES ('{}', '{}', '{}', '{}') RETURNING id".format(
                data["fecha_entrega"],
                get_id_client["direccion"],
                data["estado_entrega"],
                id_pedido
            ))
            self._conn.commit()
            return self._cur.fetchone()
        return None
    
    def get_by_state(self, state):
        self._cur.execute("""
            SELECT * FROM "entregas" WHERE estado_entrega=%s              
            """, (state,))
        return self._cur.fetchall()
    
    def get_by_order(self, id_pedido):
        self._cur.execute("""
            SELECT * FROM "entregas" WHERE id_pedido=%s              
            """, (id_pedido,))
        return self._cur.fetchone()
    
    def get_one(self, id):
        self._cur.execute("""
            SELECT * FROM "entregas" WHERE id=%s              
            """, (id,))
        return self._cur.fetchone()
    
    def get_done_delivery(self, id_pedido):
        get_order = HandlePedidos().get_one(id_pedido)
        if get_order:
            self._cur.execute("""
                SELECT * FROM "entregas" WHERE estado_entrega='Entregado' AND id_pedido=%s             
                """, (id_pedido,))
            return self._cur.fetchone()
        return False
    
    def update_state(self, id, state):
        get_delivery = self.get_one(id)
        if get_delivery:
            self._cur.execute("UPDATE entregas SET estado_entrega='{}' WHERE id='{}'". format(
                state,
                id
            ))
            self._conn.commit()
            return True
        return None
    
    def update_date(self, id_pedido, date):
        get_done_delivery = self.get_by_order(id_pedido)
        if get_done_delivery:
            self._cur.execute("UPDATE entregas SET fecha_entrega='{}' WHERE id_pedido={}".format(
                date,
                id_pedido
            ))
            self._conn.commit()
            return True
        return None
    
    def delete_done_deliveries(self, id_pedido):
        get_delivery = self.get_done_delivery(id_pedido)
        if get_delivery==False:
            return False
        elif get_delivery:
            self._cur.execute("""
            DELETE FROM "entregas" WHERE estado_entrega='Entregado' AND id_pedido=%s                
            """, (id_pedido,))
            self._conn.commit()
            return True
        return None
    
    def __del__(self):
        self._conn.close()

class HandleOrdenesCompras:
    def __init__(self) -> None:
        try:
            self._conn = psycopg2.connect(f"dbname={DBNAME} user=postgres password={PASSWORD} host={HOST} port={PORT}")
            self._cur = self._conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        except psycopg2.OperationalError as err:
            print("\x1b[1;41mThe connection to the database hasn't been succesful\x1b[0;37m")
            print(err)
            self._conn.close()
    
    def insert(self, data, id_pedido, id_proveedor):
        get_order = HandlePedidos().get_one(id_pedido)
        get_supplier = HandleProveedores().get_one(id_proveedor)
        get_one = self.get_one(id_pedido)
        if get_order==None or get_supplier==None:
            return False
        elif get_one==None:
            id_cliente = HandleClientes().get_one(get_order["id_cliente"])
            self._cur.execute("INSERT INTO ordenes_compras(fecha_orden,estado_orden,id_cliente,id_proveedor,id_pedido) VALUES ('{}','{}','{}','{}','{}')". format(
                data["fecha_orden"],
                data["estado_orden"],
                id_cliente["id"],
                id_proveedor,
                id_pedido
            ))
            self._conn.commit()
            return True
        return None
    
    def get_one(self, id_pedido):
        self._cur.execute("""
            SELECT * FROM "ordenes_compras" WHERE id_pedido=%s              
            """,(id_pedido,))
        return self._cur.fetchone()
    
    def get_all_client_buys(self, id_cliente):
        get_client = HandleClientes().get_one(id_cliente)
        if get_client:
            self._cur.execute("""
                SELECT * FROM "ordenes_compras" WHERE id_cliente=%s              
                """,(id_cliente,))
            return self._cur.fetchall()
        return False
    
    def get_done_buy(self, id_pedido):
        get_order = HandlePedidos().get_one(id_pedido)
        if get_order:
            self._cur.execute("""
                SELECT * FROM "ordenes_compras" WHERE estado_orden='Terminado' AND id_pedido=%s             
                """, (id_pedido,))
            return self._cur.fetchone()
        return False
    
    def update_state(self, state, id_pedido):
        get_order = HandlePedidos().get_one(id_pedido)
        if get_order:
            self._cur.execute("UPDATE ordenes_compras SET estado_orden='{}' WHERE id_pedido='{}'".format(
                state,
                id_pedido
            ))
            self._conn.commit()
            return True
        return None
    
    def delete_done_buy(self, id_pedido):
        done_buy = self.get_done_buy(id_pedido)
        if done_buy==False:
            return False
        elif done_buy:
            self._cur.execute("""
                DELETE FROM "ordenes_compras" WHERE estado_orden='Terminado' AND id_pedido=%s              
                """, (id_pedido,))
            self._conn.commit()
            return True
        return None
    
    def __del__(self):
        self._conn.close()