from fastapi import FastAPI, Query, HTTPException, status
from typing import Annotated
from pydantic import BaseModel, Field
from fastapi.encoders import jsonable_encoder
from enum import Enum

app = FastAPI()


class Category(str, Enum):
    novela = "Novela"
    ficcion = "Ficción"
    misterio = "Misterio"


class Book(BaseModel):
    titulo: Annotated[str, Field(..., min_length=5)] = "Sin titulo"
    autor: Annotated[str, Field(..., min_length=5)] = "sin autor"
    paginas: Annotated[int | None, Field(ge=1)] = 100
    precio: Annotated[float, Field(..., ge=0)]
    category: Annotated[Category, Field(...)] = Category.ficcion


class BookUpdate(BaseModel):
    titulo: str | None = None
    autor: str | None = None
    paginas: int | None = None
    precio: float | None = None
    category: Category | None = Category.ficcion


books = {
    3: {
        "titulo": "La lucha",
        "category": "Novela",
        "autor": "juan benites",
        "precio": 15000,
        "paginas": 100,
    },
    1: {
        "titulo": "El coronel no tiene quien le escriba",
        "category": "Novela",
        "autor": "gabriel garcia",
        "precio": 100000,
        "paginas": 243,
    },
    2: {
        "titulo": "El otoño del patriarca",
        "category": "Novela",
        "autor": "gabriel garcia",
        "precio": 100000,
        "paginas": 243,
    },
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
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book not found, id:{book_id}",
        )
    books[book_id] = book.model_dump()
    return books[book_id]


@app.patch("/books/update/{book_id}")
async def update_book_partial(book_id: int, book_update: BookUpdate):
    if book_id not in books.keys():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Book not found: {book_id}"
        )
    book = books[book_id]
    book_model = Book(**book)
    book_get = book_update.model_dump(exclude_unset=True)
    updated = book_model.model_copy(update=book_get)
    books[book_id] = jsonable_encoder(updated)
    return books[book_id]


@app.delete("/books/{book_id}")
async def delete_book(book_id: int):
    if book_id not in books.keys():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Book not found: {book_id}"
        )
    del books[book_id]
    return {"message": "libro borrado con exito"}


@app.get("/books/stats/summary")
async def get_stats_summary(category: Annotated[Category | None, Query()] = None):
    selection = []
    if category:
        selection = [value for value in books.values() if value["category"] == category]
    else:
        selection = books.values()

    counts_books = len(selection)
    values = [values["precio"] for values in selection]
    suma_total = sum(values)

    if counts_books > 0:
        average = suma_total / counts_books
        return {
            "cantidad_libros": counts_books,
            "total": f"${suma_total:,.2f}",
            "promedio:": f"${average:,.2f}",
            "precio_mayor": f"{max(values):,.2f}",
            "precio_menor": f"{min(values):,.2f}",
        }
    else:
        return {"Message": f"no hay libros de la categoria {category}"}
