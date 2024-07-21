from fastapi import FastAPI, Query, Path
from config.handle_db import HandleClientes, HandleEmpleados, HandleProveedores, HandleProductos, HandleInventarios, HandlePedidos, HandleEntregas, HandleOrdenesCompras
from config.handle_mview import HandleErrorDeliveries
from config.handle_login import HandleLoginEmpleados, HandleLoginProveedores
from schemas.tables_schemas import ClientesSchema, EmpleadosSchema, ProveedoresSchema, ProductosSchema, InventariosSchema, PedidosSchema, EntregasSchemas, OrdenesComprasSchemas
from schemas.mview_schemas import ErrorDeliveriesSchema
from schemas.logins_schemas import LoginEmpleadosSchema, LoginProveedoresSchema
from utils.to_lowercase import to_lowercase
from utils.to_title import to_title
from fastapi.responses import JSONResponse
from middleware.error_handler import ErrorHandler
from service.database_connection import engine, Base

#-->Application variables
app = FastAPI()
app.title = "Entregas Condor ltda."
app.add_middleware(ErrorHandler) #Manejador de errores, que muestra el error sin saltar un error que detenga toda la aplicacion

#-->Creation of the tables in the serverless database
Base.metadata.create_all(bind=engine)

#-->Handle DB variables
client = HandleClientes()
employee = HandleEmpleados()
supplier = HandleProveedores()
product = HandleProductos()
inventory = HandleInventarios()
order = HandlePedidos()
delivery = HandleEntregas()
bill = HandleOrdenesCompras()

#-->Handle mview variables
error_delivery = HandleErrorDeliveries()

#-->Handle Logins variables
login_eployee = HandleLoginEmpleados()
login_supplier = HandleLoginProveedores()

#-->Utils variables
lower = to_lowercase
title = to_title

#-------HOME---------
@app.get("/", tags=['Home'])
def home():
    return "App has been started"

#-------CLIENT---------
@app.post("/client", tags=['Clients'], response_model=dict)
def create_client(client_data:ClientesSchema):
    client_data.direccion = client_data.direccion.strip()
    data_dict = client_data.model_dump()
    new_client = client.insert(data_dict)
    if new_client:
        return JSONResponse(status_code=201, content={"Message":"¡Cliente creado con exito!"})
    return JSONResponse(status_code=400, content={"Message":"¡El cliente no se pudo crear, porque tiene la id duplicada de otro cliente!"})

@app.get("/client/", tags=["Clients"], response_model=ClientesSchema)
def get_clients_by_addres(direccion:str=Query(min_length=5, max_length=30)):
    correct_addres = direccion.strip()
    all_clients = client.get_all_by_addres(correct_addres)
    if all_clients:
        return JSONResponse(status_code=200, content=all_clients)
    return JSONResponse(status_code=404, content={"Message":"¡No hay clientes guardados con esa dirreción!"})
    
@app.get("/client/{id}", tags=["Clients"], response_model=ClientesSchema)
def get_one_client(id:int = Path(gt=0)):
    one_client = client.get_one(id)
    if one_client:
        return JSONResponse(status_code=200, content=one_client)
    return JSONResponse(status_code=404, content={"Message":"¡Cliente no encontrado!"})

@app.put("/client/{id}", tags=["Clients"], response_model=dict)
def update_client(data:ClientesSchema, id:int= Path(gt=0)):
    data.direccion = data.direccion.strip()
    data_client = data.model_dump()
    new_client = client.update(id,data_client)
    if new_client:
        return JSONResponse(status_code=201, content={"Message":"¡Cliente actualizado con exito!"})
    return JSONResponse(status_code=404, content={"Message":"¡El cliente no se pudo actualizar, vuelva a intentarlo!"})

@app.delete("/client/{id}", tags=["Clients"], response_model=dict)
def delete_client(id:int = Path(gt=0)):
    less_client = client.delete(id)
    if less_client:
        return JSONResponse(status_code=200, content={"Message":"¡Cliente eliminado con exito!"})
    return JSONResponse(status_code=400, content={"Message":"¡El cliente no se pudo eliminar, vuelva a intentarlo!"})

#----ACCOUNT EMPLOYEE----
@app.post("/account-employee/{id_empleado}", tags=["AccountEmployees"])
def create_account_eployee(data:LoginEmpleadosSchema,id_empleado:int = Path(gt=0)):
    data_dict = data.model_dump()
    new_login = login_eployee.insert(data_dict,id_empleado)
    if new_login:
        return JSONResponse(status_code=201, content={"Message":"¡Sesión creada con exito!"})
    elif new_login==False:
        return JSONResponse(status_code=404, content={"Message":"¡No existe ningún empleado con esa id en la empresa!"})
    return JSONResponse(status_code=400, content={"Message":"¡No ha se ha podido crear la sesión, porque ya existe una para esa id de empleado!"})

#----LOGIN EMPLOYEE----
@app.post("/login-employee/{id_empleado}", tags=["LoginEmployee"])
def login_employees(contrasena:LoginEmpleadosSchema,id_empleado:int = Path(gt=0)):
    contrasena_dict = contrasena.model_dump()
    login = login_eployee.check_password(id_empleado,contrasena_dict)
    if login:
        return JSONResponse(status_code=200, content={"Message":"¡Te has logeado con exito!"})
    elif login==False:
        return JSONResponse(status_code=401, content={"Message":"¡Identificación o contraseña incorrecta!"})
    return JSONResponse(status_code=404, content={"Message":"¡No existe ningún empleado con esa id en la empresa!"})

#-------EMPLOYEE---------
@app.post("/employee", tags=['Employees'], response_model=dict)
def create_employee(employee_data:EmpleadosSchema):
    employee_data.puesto = employee_data.puesto.lower().replace(' ','')
    data_dict = employee_data.model_dump()
    new_employee = employee.insert(data_dict)
    if new_employee:
        return JSONResponse(status_code=201, content={"Message":"¡Empleado creado con exito!"})
    return JSONResponse(status_code=400, content={"Message":"¡El empleado no se pudo crear, porque tiene la id duplicada de otro empleado!"})
    
@app.get("/employee/", tags=['Employees'], response_model=EmpleadosSchema)
def get_employees_by_charge(puesto:str=Query(min_length=1, max_length=15)):
    correct_charge = lower(puesto).replace(' ','')
    print(correct_charge)
    employees = employee.get_all_by_charge(correct_charge)
    if employees:
        return JSONResponse(status_code=200, content=employees)
    return JSONResponse(status_code=404, content={"Message":"¡No hay empleados con ese cargo por mostrar!"})

@app.get("/employee/{id}", tags=['Employees'], response_model=EmpleadosSchema)
def get_one_employee(id:int = Path(gt=0)) -> EmpleadosSchema:
    one_employee = employee.get_one(id)
    if one_employee:
        return JSONResponse(status_code=200, content=one_employee)
    return JSONResponse(status_code=404, content={"Message":"¡Empleado no encontrado!"})

@app.put("/employee/{id}", tags=['Employees'], response_model=dict)
def update_employee(id:int, data:EmpleadosSchema):
    data.puesto = data.puesto.lower().replace(' ','')
    data_employee = data.model_dump()
    new_employee = employee.update(id,data_employee)
    if new_employee:
        return JSONResponse(status_code=201, content={"Message":"¡Empleado actualizado con exito!"})
    return JSONResponse(status_code=404, content={"Message":"¡El empleado no se pudo actualizar, vuelva a intentarlo!"})

@app.delete("/employee/{id}", tags=["Employees"], response_model=dict)
def delete_employee(id:int = Path(gt=0)):
    less_employee = employee.delete(id)
    if less_employee:
        return JSONResponse(status_code=200, content={"Message":"¡Empleado eliminado con exito!"})
    return JSONResponse(status_code=400, content={"Message":"¡El empleado no se pudo eliminar, vuelva a intentarlo!"})

#----ACCOUNT SUPPLIER----
@app.post("/account-supplier/{id_proveedor}", tags=["AccountSuppliers"])
def create_account_supplier(data:LoginProveedoresSchema,id_proveedor:int = Path(gt=0)):
    data_dict = data.model_dump()
    new_login = login_supplier.insert(data_dict,id_proveedor)
    if new_login:
        return JSONResponse(status_code=201, content={"Message":"¡Sesión creada con exito!"})
    elif new_login==False:
        return JSONResponse(status_code=404, content={"Message":"¡No existe ningún proveedor con esa id en la empresa!"})
    return JSONResponse(status_code=400, content={"Message":"¡No ha se ha podido crear la sesión, porque ya existe una para esa id de proveedor!"})

#----LOGIN SUPPLIER----
@app.post("/login-supplier/{id_proveedor}", tags=["LoginSuppliers"])
def login_suppliers(contrasena:LoginProveedoresSchema,id_proveedor:int = Path(gt=0)):
    contrasena_dict = contrasena.model_dump()
    login = login_supplier.check_password(id_proveedor,contrasena_dict)
    if login:
        return JSONResponse(status_code=200, content={"Message":"¡Te has logeado con exito!"})
    elif login==False:
        return JSONResponse(status_code=401, content={"Message":"¡Identificación o contraseña incorrecta!"})
    return JSONResponse(status_code=404, content={"Message":"¡No existe ningún proveedor con esa id en la empresa!"})

#-------SUPPLIER-------
@app.post("/supplier", tags=["Suppliers"], response_model=dict)
def create_supplier(data:ProveedoresSchema):
    data.direccion_proveedor = data.direccion_proveedor.strip()
    data_dict = data.model_dump()
    new_supplier = supplier.insert(data_dict)
    if new_supplier:
        return JSONResponse(status_code=201, content={"Message":"¡Proveedor creado con exito!"})
    return JSONResponse(status_code=400, content={"Message":"¡El proveedor no se pudo crear, porque tiene la id duplicada de otro proveedor!"})

@app.get("/suplier/", tags=["Suppliers"], response_model=ProveedoresSchema)
def get_suppliers_by_address(direccion_proveedor:str=Query(min_length=1, max_length=20)):
    correct_addres = direccion_proveedor.strip()
    suppliers = supplier.get_all_by_addres(correct_addres)
    if suppliers:
        return JSONResponse(status_code=200, content=suppliers)
    return JSONResponse(status_code=404, content={"Message":"¡No hay proveedores guardados con esa dirección para mostrar!"})

@app.get("/supplier/{id}", tags=["Suppliers"], response_model=ProveedoresSchema)
def get_one_suppliers(id:int = Path(gt=0)):
    one_supplier = supplier.get_one(id)
    if one_supplier:
        return JSONResponse(status_code=200, content=one_supplier)
    return JSONResponse(status_code=404, content={"Message":"¡Proveedor no encontrado!"})

@app.put("/supplier/{id}", tags=["Suppliers"], response_model=dict)
def update_supplier(id:int, data:ProveedoresSchema):
    data.direccion_proveedor = data.direccion_proveedor.strip()
    data_dict = data.model_dump()
    new_supplier = supplier.update(data_dict, id)
    if new_supplier:
        return JSONResponse(status_code=201, content={"Message":"¡Proveedor actualizado con exito!"})
    return JSONResponse(status_code=404, content={"Message":"¡El proveedor no se pudo actualizar, vuelva a intentarlo!"})

@app.delete("/supplier/{id}", tags=["Suppliers"], response_model=dict)
def delete_supplier(id:int = Path(gt=0)):
    less_supplier = supplier.delete(id)
    if less_supplier:
        return JSONResponse(status_code=200, content={"Message":"¡Proveedor eliminado con exito!"})
    return JSONResponse(status_code=400, content={"Message":"¡El proveedor no se pudo eliminar, vuelva a intentarlo!"})

#-------PRODUCT-------
@app.post("/product", tags=["Products"], response_model=dict)
def create_product(data:ProductosSchema):
    data.nombre_producto = data.nombre_producto.lower()
    data_dict = data.model_dump()
    new_product = product.insert(data_dict)
    return JSONResponse(status_code=201, content={"Message":"¡Producto creado con exito!"})

@app.get("/product", tags=["Products"], response_model=ProductosSchema)
def get_all_products():
    products = product.get_all()
    if products:
        return JSONResponse(status_code=200, content=products)
    return JSONResponse(status_code=404, content={"Message":"¡No hay productos para mostrar!"})

@app.get("/product/", tags=["Products"], response_model=ProductosSchema)
def get_one_product(nombre_producto:str = Query(min_length=1, max_length=25)):
    lower_nombre_producto = to_lowercase(nombre_producto)
    one_product = product.get_one(lower_nombre_producto)
    if one_product:
        return JSONResponse(status_code=200, content=one_product)
    return JSONResponse(status_code=404, content={"Message":"¡Producto no encontrado!"})

@app.put("/product/", tags=["Products"], response_model=dict)
def update_product(data:ProductosSchema, nombre_producto:str=Query(min_length=1, max_length=25)):
    data.nombre_producto = data.nombre_producto.lower()
    lower_nombre_producto = to_lowercase(nombre_producto)
    data_dict = data.model_dump()
    new_product = product.update(data_dict, lower_nombre_producto)
    if new_product:
        return JSONResponse(status_code=201, content={"Message":"¡Producto actualizado con exito!"})
    return JSONResponse(status_code=404, content={"Message":"¡El producto no se pudo actualizar, vuelva a intentarlo!"})

@app.delete("/product/", tags=["Products"], response_model=dict)
def delete_product(nombre_producto:str=Query(min_length=1, max_length=25)):
    lower_nombre_producto = to_lowercase(nombre_producto)
    less_product = product.delete(lower_nombre_producto)
    if less_product:
        return JSONResponse(status_code=200, content={"Message":"¡Producto eliminado con exito!"})
    return JSONResponse(status_code=400, content={"Message":"¡El producto no se pudo eliminar, vuelva a intentarlo!"})

#-------INVENTORIES-------
@app.post("/inventory/", tags=["Inventories"], response_model=dict)
def create_inventory(data:InventariosSchema, nombre_producto:str=Query(min_length=1, max_length=25)):
    lower_nombre_producto = lower(nombre_producto)
    data_dict = data.model_dump()
    new_inventory = inventory.insert(data_dict, lower_nombre_producto)
    if new_inventory:
        return JSONResponse(status_code=201, content={"Message":"¡Inventario creado con exito!"})
    elif new_inventory == False:
        return JSONResponse(status_code=404, content={"Message":"¡El inventario no se pudo crear, porque el producto no existe!"})
    return JSONResponse(status_code=400, content={"Message":"¡El inventario no se pudo crear, porque ya existe uno para ese producto!"})

@app.get("/inventory/{ubicacion}", tags=["Inventories"], response_model=dict)
def get_all_inventories_by_warehouse(ubicacion:str=Path(min_length=1, max_length=10, example="Bodega 1")):
    inventories = inventory.get_all(ubicacion)
    if inventories:
        return JSONResponse(status_code=201, content={"Message":"¡En esta bodega hay {} productos!".format(len(inventories))})
    return JSONResponse(status_code=404, content={"Message":"¡No hay inventarios para mostrar!"})

@app.get("/inventory/", tags=["Inventories"], response_model=InventariosSchema)
def get_one_inventory(nombre_producto:str=Query(min_length=1, max_length=25)):
    lower_nombre_producto = lower(nombre_producto)
    one_inventory = inventory.get_one(lower_nombre_producto)
    if one_inventory:
        return JSONResponse(status_code=200, content=one_inventory)
    return JSONResponse(status_code=404, content={"Message":"¡Inventario no encontrado!"})

@app.put("/inventory/", tags=["Inventories"], response_model=dict)
def update_inventory(data:InventariosSchema, nombre_producto:str=Query(min_length=1, max_length=25)):
    lower_nombre_producto = lower(nombre_producto)
    data_dict = data.model_dump()
    new_inventory = inventory.update(data_dict, lower_nombre_producto)
    if new_inventory:
        return JSONResponse(status_code=201, content={"Message":"¡Inventario actualizado con exito!"})
    return JSONResponse(status_code=404, content={"Message":"¡El inventario no se pudo actualizar, vuelva a intentarlo!"})

@app.delete("/inventory/", tags=["Inventories"], response_model=dict)
def delete_inventory(nombre_producto:str=Query(min_length=1, max_length=25)):
    lower_nombre_producto = lower(nombre_producto)
    less_inventory = inventory.delete(lower_nombre_producto)
    if less_inventory:
        return JSONResponse(status_code=200, content={"Message":"¡Inventario eliminado con exito!"})
    return JSONResponse(status_code=400, content={"Message":"¡El producto no se pudo eliminar, vuelva a intentarlo!"})

#-------ORDERS-------
@app.post("/order/", tags=["Orders"], response_model=dict)
def create_order(data:PedidosSchema, id_cliente:int=Query(gt=0), nombre_producto:str=Query(min_length=1, max_length=25)):
    lower_nombre_producto = lower(nombre_producto)
    data_dict = data.model_dump() #La idea es que el cliente cuando haga un pedido obtenga un id de este, para que le haga seguimiento
    new_order = order.insert(data_dict, id_cliente, lower_nombre_producto)
    if new_order:
        return JSONResponse(status_code=201, content={"Message":"¡El pedido con ID => {}, fue creado con exito!".format(new_order["id"])})
    elif new_order==False:
        return JSONResponse(status_code=400, content={"Message":"¡El pedido no se pudo crear, porque no hay mas stock del producto!"})
    return JSONResponse(status_code=404, content={"Message":"¡El pedido no se pudo crear, vuelva a intentarlo!"})

@app.get("/order/", tags=["Orders"], response_model=PedidosSchema)
def get_order_by_date(fecha_pedido:str=Query(min_length=4, max_length=20, example="2000-00-00")):
    correct_date = fecha_pedido.replace(' ','')
    date_order = order.get_by_date(correct_date)
    if date_order:
        return JSONResponse(status_code=200, content=date_order)
    return JSONResponse(status_code=404, content={"Message":"¡No hay pedidos hechos en esta fecha!"})

@app.get("/order/{id_cliente}", tags=["Orders"], response_model=PedidosSchema)
def get_order_by_product(nombre_producto:str=Query(min_length=1, max_length=25), id_cliente:int=Path(gt=0)):
    lower_nombre_producto = lower(nombre_producto)
    product_order = order.get_by_product(lower_nombre_producto,id_cliente)
    if product_order:
        return JSONResponse(status_code=200, content=product_order)
    return JSONResponse(status_code=404, content={"Message":"¡Este cliente no ha hecho ningun pedido de este producto!"})

#-------DELIVERY-------
@app.post("/delivery/{id_pedido}", tags=["Deliveries"], response_model=dict)
def create_delivery(data:EntregasSchemas,id_pedido:int=Path(gt=0)):
    data.estado_entrega = data.estado_entrega.title()
    data_dict = data.model_dump()
    new_delivery = delivery.insert(data_dict,id_pedido)
    if new_delivery:
        return JSONResponse(status_code=201, content={"Message":"¡La entrega con el número serial {}, fue creada con exito!".format(new_delivery["id"])})
    elif new_delivery == False:
        return JSONResponse(status_code=404, content={"Message":"¡La entrega no se pudo crear, porque el pedido no existe!"})
    return JSONResponse(status_code=400, content={"Message":"¡La entrega no se pudo crear, porque ya existe una para ese pedido!"})

@app.get("/delivery/", tags=["Deliveries"], response_model=EntregasSchemas)
def get_delivery_by_state(estado_entrega:str=Query(min_length=1, max_length=25, example='En Bodega')):
    title_estado_entrega = title(estado_entrega).strip()
    state_delivery = delivery.get_by_state(title_estado_entrega)
    if state_delivery:
        return JSONResponse(status_code=200, content=state_delivery)
    return JSONResponse(status_code=404, content={"Message":"¡No hay entregas con ese estado para mostrar!"})

@app.get("/delivery/{id_pedido}", tags=["Deliveries"], response_model=EntregasSchemas)
def get_delivery_by_order(id_pedido:int=Path(gt=0)):
    delivery_order = delivery.get_by_order(id_pedido)
    if delivery_order:
        return JSONResponse(status_code=200, content=delivery_order)
    return JSONResponse(status_code=404, content={"Message":"¡No hay entregas hechas para ese pedido!"})

@app.put("/delivery/{serial}", tags=["Deliveries"], response_model=dict)
def update_state_delivery(serial:int=Path(gt=0), estado_entrega:str=Query(min_length=1, max_length=25, example='Entregado')):
    title_estado_entrega = title(estado_entrega).strip()
    new_delivery = delivery.update_state(serial, title_estado_entrega)
    if new_delivery:
        return JSONResponse(status_code=201, content={"Message":"¡Estado de entrega actualizado con exito!"})
    return JSONResponse(status_code=404, content={"Message":"¡El estado no se pudo actualizar, porque no existe esa entrega en la base de datos!"})

@app.put("/delivery/", tags=["Deliveries"], response_model=dict)
def update_date_delivery(id_pedido:int=Query(gt=0), fecha_entrega:str=Query(min_length=5, max_length=25, example='2000-00-00')):
    correct_date = fecha_entrega.replace(' ','')
    new_delivery = delivery.update_date(id_pedido, correct_date)
    if new_delivery:
        return JSONResponse(status_code=201, content={"Message":"¡Fecha de entrega actualizada con exito!"})
    return JSONResponse(status_code=404, content={"Message":"¡La fecha no se pudo actualizar, porque no existe una entrega con ese pedido en la base de datos!"})

@app.delete("/delivey/{id_pedido}", tags=["Deliveries"], response_model=dict)
def delete_delivered_deliveries(id_pedido:int=Path(gt=0)):
    less_deliveries = delivery.delete_done_deliveries(id_pedido)
    if less_deliveries:
        return JSONResponse(status_code=200, content={"Message":"¡Entrega eliminada con exito!"})
    elif less_deliveries==False:
        return JSONResponse(status_code=404, content={"Message":"¡La entrega no se pudo eliminar, porque no existe ese pedido en la base de datos!"})
    return JSONResponse(status_code=400, content={"Message":"¡La entrega no se pudo eliminar, porque ese pedido no tiene estado de Entregado!"})

#----ERRORDELIVERY----
@app.post("/mview/{id_entrega}", tags=["Mview"], response_model=dict)
def create_error_delivery(data:ErrorDeliveriesSchema, id_entrega:int=Path(gt=0)):
    data_dict = data.model_dump()
    new_mview = error_delivery.insert(data_dict,id_entrega)
    if new_mview:
        return JSONResponse(status_code=201, content={"Message":"¡Aviso del error de la entrega creado con exito!"})
    elif new_mview == False:
        return JSONResponse(status_code=404, content={"Message":"¡El aviso no se pudo crear, porque esa entrega no esta guardada con estado de error!"})
    return JSONResponse(status_code=400, content={"Message":"¡No se pudo crear el aviso, porque ya existe uno para esa entrega!"})

@app.get("/mview", tags=["Mview"], response_model=EntregasSchemas)
def error_deliveries_mview():
    mview = error_delivery.get_all()
    if mview:
        return JSONResponse(status_code=200, content=mview)
    return JSONResponse(status_code=404, content={"Message":"¡No hay entregas actualizadas con errores de entrega!"})

@app.delete("/mview/{id_entrega}", tags=["Mview"], response_model=dict)
def delete_error_delivery(id_entrega:int=Path(gt=0)):
    less_mview = error_delivery.delete(id_entrega)
    if less_mview:
        return JSONResponse(status_code=200, content={"Message":"¡Aviso eliminado con exito!"})
    return JSONResponse(status_code=404, content={"Message":"¡El aviso no se pudo eliminar, porque no existe en la base de datos!"})

#------BILL-------
@app.post("/bill/{id_pedido}", tags=["Bills"], response_model=dict)
def create_bill(data:OrdenesComprasSchemas, id_pedido:int=Path(gt=0), id_proveedor:int=Query(gt=0)):
    data.estado_orden = data.estado_orden.title()
    data_dict = data.model_dump()
    new_bill = bill.insert(data_dict,id_pedido,id_proveedor)
    if new_bill:
        return JSONResponse(status_code=201, content={"Message":"¡Orden de compra creada con exito!"})
    elif new_bill==False:
        return JSONResponse(status_code=404, content={"Message":"¡La orden de compra no se pudo crear, porque el proveedor y el pedido no existen en la base de datos!"})
    return JSONResponse(status_code=400, content={"Message":"¡La orden de compra no se pudo crear, vuelva a intentarlo!"})

@app.get("/bill/{id_pedido}", tags=["Bills"], response_model=OrdenesComprasSchemas)
def get_by_order(id_pedido:int=Path(gt=0)):
    order_buy = bill.get_one(id_pedido)
    if order_buy:
        return JSONResponse(status_code=200, content=order_buy)
    return JSONResponse(status_code=404, content={"Message":"¡No hay ninguna orden de compra para este pedido en la base de datos!"})

@app.get("/bill/", tags=["Bills"], response_model=OrdenesComprasSchemas)
def get_client_buys(id_cliente:int=Query(gt=0)):
    client_buys = bill.get_all_client_buys(id_cliente)
    if client_buys:
        return JSONResponse(status_code=200, content=client_buys)
    elif client_buys==False:
        return JSONResponse(status_code=404, content={"Message":"¡Este cliente no existe en la base de datos!"})
    return JSONResponse(status_code=400, content={"Message":"¡Este cliente no ha hecho ninguna compra!"})

@app.put("/bill/{id_pedido}", tags=["Bills"], response_model=dict)
def update_state_buy(id_pedido:int=Path(gt=0), estado_orden:str=Query(min_length=1, max_length=15)):
    title_estado_orden = title(estado_orden).strip()
    new_bill = bill.update_state(title_estado_orden,id_pedido)
    if new_bill:
        return JSONResponse(status_code=201, content={"Message":"¡Estado de orden de compra actualizado con exito!"})
    return JSONResponse(status_code=404, content={"Message":"¡El estado no se pudo actualizar, porque no existe ese pedido en la base de datos!"})

@app.delete("/bill/{id_pedido}", tags=["Bills"], response_model=dict)
def delete_done_bill(id_pedido:int=Path(gt=0)):
    less_done_bill = bill.delete_done_buy(id_pedido)
    if less_done_bill:
        return JSONResponse(status_code=200, content={"Message":"¡Orden de compra eliminada con exito!"})
    elif less_done_bill==False:
        return JSONResponse(status_code=404, content={"Message":"¡La orden de compra no se pudo eliminar, porque no existe ese pedido en la base de datos!"})
    return JSONResponse(status_code=400, content={"Message":"¡La orden de compra no se pudo eliminar, porque ese pedido no tiene un estado de Terminado!"})
