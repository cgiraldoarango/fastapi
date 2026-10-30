from datetime import datetime
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

app = FastAPI(title="Cga-encoder")

class Item(BaseModel):
    title: str
    timestamp: datetime
    description: str | None = None

fake_db = {}

@app.put("/items/{id}")
async def update_item(id: str, item: Item):
    # Convertimos el modelo Pydantic a un diccionario JSON compatible 
    # (por ejemplo, 'timestamp' pasa de ser un objeto datetime a un string ISO)
    json_compatible_item_data = jsonable_encoder(item)
    
    # Ahora ya se puede guardar de forma segura en una base de datos o diccionario
    fake_db[id] = json_compatible_item_data
    return {"message": "Actualizado con éxito", "data": json_compatible_item_data}