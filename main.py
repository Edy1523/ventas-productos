from fastapi import FastAPI
from config.handle_db import HandleClientes
from schemas.clients import ClientSchema

app = FastAPI()

@app.get("/")
def home():
    return "Hi, I am Cristiano Ronaldo"

@app.post("/client")
def client(client_data:ClientSchema):
    data_dict = client_data.model_dump()
    print(data_dict)
    client = HandleClientes()
    client.insert(data_dict)