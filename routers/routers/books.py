# routers/books.py
from fastapi import APIRouter, HTTPException, Query, status
from typing import Annotated
from database import books
from models.book import Book, BookUpdate, Category

router = APIRouter(prefix="/books", tags=["Books"])

@router.get("/")
async def get_books(
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int | None, Query(le=100)] = 100,
):
    book_list = list(books.values())
    return book_list[skip : skip + limit]

@router.get("/title")
async def get_books_by_title(
    title: Annotated[str | None, Query(min_length=2)] = None,
):
    if title is None:
        return list(books.values())
    return [book for book in books.values() if title.lower() in book["titulo"].lower()]

@router.post("/nuevo")
async def create_new_book(book: Book):
    new_id = max(books.keys()) + 1 if books else 1
    books[new_id] = book.model_dump()
    return {"message": "Libro creado", "id": new_id, "book": books[new_id]}

@router.put("/{book_id}")
async def update_book_by_id(book_id: int, book: Book):
    if book_id not in books:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    books[book_id] = book.model_dump()
    return books[book_id]

@router.delete("/{book_id}")
async def delete_book(book_id: int):
    if book_id not in books:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    del books[book_id]
    return {"message": "Book deleted successfully"}