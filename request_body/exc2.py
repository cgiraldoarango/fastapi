from fastapi import FastAPI, Query, HTTPException, status
from typing import Annotated
from pydantic import BaseModel, Field
from enum import Enum
app = FastAPI()

class Category(str, Enum):
    novela="Novela"
    ficcion="Ficción"
    misterio="Misterio"

class Book(BaseModel):
    titulo: Annotated[str, Field(..., min_length=5)]="Sin titulo"
    autor: Annotated[str, Field(..., min_length=5)]="sin autor"
    paginas: Annotated[int | None, Field(ge=1)] = 100
    precio: Annotated[float, Field(..., ge=0)]
    category: Annotated[Category, Field(...)]=Category.ficcion



books = {
    3: {"titulo": "La lucha", "category": "error"},
    1: {"titulo": "El coronel no tiene quien le escriba", "category": "Novela"},
    2: {"titulo": "El otoño del patriarca", "category": "Novela"},
}


@app.get("/books/")
async def get_books(
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int | None, Query(le=100)] = 100,
):
    book_list = list(books.values())
    return book_list[skip : skip + limit]


@app.get("/books/title")
async def get_books_by_title(
    title: Annotated[
        str | None,
        Query(
            pattern=r"^[A-Za-zÁÉÍÓÚÑ]+( [A-Za-zÁÉÍÓÚÑ]+)*$",
            min_length=2,
            title="Título del libro",
            description="Palabras de descripción del libro",
            deprecated=False,
            examples=["Coronel", "Otoño"],
        ),
    ] = None,
):
    if title is None:
        return list(books.values())
    books_select = []
    for book in books.values():
        if title.lower() in book["titulo"].lower():
            books_select.append(book)
    return books_select


@app.post("/books/nuevo")
async def create_new_book(book: Book):
    keys = []
    for key, values in books.items():
        keys.append(key)

    maximo = max(keys)
    new_id = int(maximo) + 1
    books[new_id] = book.model_dump()
    return books


@app.put("/books/update/{book_id}")
async def update_book_by_id(book_id: int, book: Book):
    if book_id not in books.keys():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Book not found, id:{book_id}"
        )
    books[book_id] = book.model_dump()
    return books[book_id]
