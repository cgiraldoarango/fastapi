from fastapi import FastAPI, Path
from enum import Enum

app = FastAPI()


class Categories(str, Enum):
    ficcion = "Ficcion"
    novela = "Novela"
    misterio = "Misterio"


books = {
    1: {"titulo": "Cien años de soledad", "category": "Novela"},
    2: {"titulo": "martin pesacador", "category": "Ficcion"},
    3: {"titulo": "la maría", "category": "Novela"},
}


@app.get("/")
async def get_root():
    return {"greeting": "hello everyone"}


@app.get("/books/")
async def get_books():
    return books


@app.get("/books/{book_id}")
async def get_book_by_id(book_id: int = Path(..., gt=0, le=100)):
    if not book_id in books:
        return {"message": "Book not found"}
    return books[book_id]


@app.get("/books/category/{category}")
async def get_books_by_category(category: Categories):
    seleccion =[]
    for key, values in books.items():
        if values["category"]==category:
            seleccion.append({'category':values['category'],'title':values['titulo']})
               
                
           
    
    if seleccion:
        return seleccion
    return {'Message': 'No encontrados'}
