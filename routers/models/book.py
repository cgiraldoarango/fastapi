# models/book.py
from enum import Enum
from pydantic import BaseModel, Field
from typing import Annotated

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
    category: Category | None = None