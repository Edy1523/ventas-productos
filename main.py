from fastapi import FastAPI, Query, Path
from config.handle_db import HandleClientes, HandleEmpleados, HandleProveedores
from schemas.tables_schemas import ClientesSchema, EmpleadosSchema, ProveedoresSchema
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from middleware.error_handler import ErrorHandler

#-->Aplication variables
app = FastAPI()
app.title = "Entregas Condor ltda."
app.add_middleware(ErrorHandler) #Manejador de errores, que muestra el error sin saltar un error que detenga toda la aplicacion

#-->Handle DB variables
client = HandleClientes()
employee = HandleEmpleados()
supplier = HandleProveedores()

#-------HOME---------
@app.get("/", tags=['Home'])
def home():
    return "App has been started"

#-------CLIENT---------
@app.post("/client", tags=['Clients'], response_model=dict)
def create_client(client_data:ClientesSchema):
    data_dict = client_data.model_dump()
    new_client = client.insert(data_dict)
    if new_client:
        return JSONResponse(status_code=201, content={"Message":"¡Cliente creado con exito!"})
    return JSONResponse(status_code=400, content={"Message":"¡El cliente no se pudo crear, porque tiene la id duplicada de otro cliente!"})

@app.get("/client", tags=["Clients"])
def get_all_clients():
    all_clients = client.get_all()
    if all_clients:
        return JSONResponse(status_code=200, content=jsonable_encoder(all_clients))
    return JSONResponse(status_code=404, content={"Message":"¡No hay clientes por mostrar!"})
    
@app.get("/client/{id}", tags=["Clients"], response_model=ClientesSchema)
def get_one_client(id:int = Path(gt=0)):
    one_client = client.get_one(id)
    if one_client:
        return JSONResponse(status_code=200, content=jsonable_encoder(one_client))
    return JSONResponse(status_code=404, content={"Message":"¡Cliente no encontrado!"})

@app.put("/client/{id}", tags=["Clients"], response_model=dict)
def update_client(data:ClientesSchema, id:int= Path(gt=0)):
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

#-------EMPLOYEE---------
@app.post("/employee", tags=['Employees'], response_model=dict)
def create_employee(employee_data:EmpleadosSchema):
    data_dict = employee_data.model_dump()
    new_employee = employee.insert(data_dict)
    if new_employee:
        return JSONResponse(status_code=201, content={"Message":"¡Empleado creado con exito!"})
    return JSONResponse(status_code=400, content={"Message":"¡El empleado no se pudo crear, porque tiene la id duplicada de otro empleado!"})
    
@app.get("/employee", tags=['Employees'])
def get_all_employees():
    employees = employee.get_all()
    if employees:
        return JSONResponse(status_code=200, content=jsonable_encoder(employees))
    return JSONResponse(status_code=404, content={"Message":"¡No hay empleados por mostrar!"})

@app.get("/employee/{id}", tags=['Employees'], response_model=EmpleadosSchema)
def get_one_employee(id:int = Path(gt=0)) -> EmpleadosSchema:
    one_employee = employee.get_one(id)
    if one_employee:
        return JSONResponse(status_code=200, content=jsonable_encoder(one_employee))
    return JSONResponse(status_code=404, content={"Message":"¡Empleado no encontrado!"})

@app.put("/employee/{id}", tags=['Employees'], response_model=dict)
def update_employee(id:int, data:EmpleadosSchema):
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

#-------SUPPLIER-------
@app.post("/supplier", tags=["Suppliers"], response_model=dict)
def create_supplier(data:ProveedoresSchema):
    data_dict = data.model_dump()
    new_supplier = supplier.insert(data_dict)
    if new_supplier:
        return JSONResponse(status_code=201, content={"Message":"¡Proveedor creado con exito!"})
    return JSONResponse(status_code=400, content={"Message":"¡El proveedor no se pudo crear, porque tiene la id duplicada de otro proveedor!"})

@app.get("/suplier", tags=["Suppliers"])
def get_all_suppliers():
    suppliers = supplier.get_all()
    if suppliers:
        return JSONResponse(status_code=200, content=jsonable_encoder(suppliers))
    return JSONResponse(status_code=404, content={"Message":"¡No hay proveedores para mostrar!"})

@app.get("/supplier/{id}", tags=["Suppliers"], response_model=ProveedoresSchema)
def get_one_suppliers(id:int = Path(gt=0)):
    one_supplier = supplier.get_one(id)
    if one_supplier:
        return JSONResponse(status_code=200, content=jsonable_encoder(one_supplier))
    return JSONResponse(status_code=404, content={"Message":"¡Proveedor no encontrado!"})

@app.put("/supplier/{id}", tags=["Suppliers"], response_model=dict)
def update_supplier(id:int, data:ProveedoresSchema):
    data_dict = data.model_dump()
    new_supplier = supplier.update(data_dict, id)
    if new_supplier:
        return JSONResponse(status_code=201, content={"Message":"¡Proveedor actualizado con exito!"})
    return JSONResponse(status_code=404, content={"Message":"¡El proveedor no se pudo actualizar, vuelva a intentarlo!"})

@app.delete("/supplier/{id}", tags=["Suppliers"], response_model=dict)
def delete_supplier(id:int = Path(gt=0)):
    less_supplier = supplier.delete(id)
    if less_supplier:
        return JSONResponse(status_code=201, content={"Message":"¡Proveedor eliminado con exito!"})
    return JSONResponse(status_code=400, content={"Message":"¡El proveedor no se pudo eliminar, vuelva a intentarlo!"})