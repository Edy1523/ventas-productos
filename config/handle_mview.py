import os
from dotenv import load_dotenv
from pathlib import Path
import psycopg2
import psycopg2.extras

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

URL : str = os.getenv("URL")

class HandleErrorDeliveries:
    def __init__(self):
        try:
            self._conn = psycopg2.connect(URL)
            self._cur = self._conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        except psycopg2.OperationalError as err:
            print("\x1b[1;41mThe connection to the database hasn't been succesful\x1b[0;37m")
            print(err)
            self._conn.close()
            
    def insert(self, data, id_entrega):
        get_mview = self.get_one(id_entrega)
        get_error_delivery = self.get_error_delivery(id_entrega)
        if get_mview == None:
            return False
        elif get_error_delivery == None:
            self._cur.execute("INSERT INTO error_entrega_descripcion(descripcion, tiempo_solucion, id_entrega)  VALUES ('{}','{}','{}')".format(
                data["descripcion"],
                data["tiempo_solucion"],
                get_mview["id"]
            ))
            self._conn.commit()
            return True
        return None
    
    def get_all(self):
        self._cur.execute("""
            REFRESH MATERIALIZED VIEW error_deliveries_mview;
            SELECT * FROM error_deliveries_mview;              
            """)
        self._conn.commit()
        return self._cur.fetchall()
    
    def get_one(self, id_entrega):
        self._cur.execute("""
            REFRESH MATERIALIZED VIEW error_deliveries_mview;
            SELECT * FROM error_deliveries_mview WHERE id=%s;              
            """, (id_entrega,))
        self._conn.commit()
        return self._cur.fetchone()
    
    def get_error_delivery(self, id_entrega):
        self._cur.execute("""
            SELECT * FROM "error_entrega_descripcion" WHERE id_entrega=%s
            """, (id_entrega,))
        return self._cur.fetchone()
    
    def delete(self, id_entrega):
        get_error_delivery = self.get_error_delivery(id_entrega)
        if get_error_delivery:
            self._cur.execute("""
                DELETE FROM "error_entrega_descripcion" WHERE id_entrega=%s              
                """,(id_entrega,))     
            self._conn.commit()
            return True
        return None   
    
    def __del__(self):
        self._conn.close()