from fastapi import FastAPI, Depends, Query
from typing import Annotated

app = FastAPI(title="Libreria CGA")

books = {
    1: {"titulo": "el coronel no tiene quien le escriba", "category": "novela"},
    2: {"titulo": "viaje al centro de la tierra", "category": "ficción"},
    3: {"titulo": "el coronel no tiene quien le escriba", "category": "novela"},
    4: {"titulo": "viaje al centro de la tierra", "category": "ficción"},
    5: {"titulo": "el coronel no tiene quien le escriba", "category": "suspenso"},
    6: {"titulo": "viaje al centro de la tierra", "category": "ficción"},
    7: {"titulo": "el coronel no tiene quien le escriba", "category": "novela"},
    8: {"titulo": "viaje al centro de la tierra", "category": "ficción"},
}


class BooksFilter:
    def __init__(
        self,
        skip: int = 0,
        limit: int = 100,
        query: Annotated[str | None, Query()] = None,
    ):
        self.skip = skip
        self.limit = limit
        self.query = query


@app.get("/")
async def get_root():
    return {"message": "Greetins from colombia"}


@app.get("/books/catalog")
async def get_books_catalog(params: Annotated[BooksFilter, Depends(BooksFilter)]):
    data = {"skip": params.skip, "limit": params.limit}
    resul_list = []
    if params.query:
        data["query"] = params.query
        for book in books.values():
            if book["category"] == params.query:
                resul_list.append(book)
    # return list[params.skip:params.limit+1]
    return {
        "skip": params.skip,
        "limit": params.limit,
        "datos": resul_list[params.skip : params.limit + 1],
    }
