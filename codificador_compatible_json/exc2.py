from datetime import datetime
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel


app=FastAPI(title="Cga-ejemplo")

#modelo de datos
class BookRegister(BaseModel):
    titulo: str
    autor: str
    precio: float
    created_at: datetime = datetime.now()

#data
books={}

@app.get("/")
async def get_start():
    return {'message':'hello everyone from colombia'}

@app.post("/book/registers")
async def book_register(id: str, book: BookRegister ):
    books[id]= jsonable_encoder(book)
    return books
    