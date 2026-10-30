from fastapi import FastAPI, HTTPException, status

app = FastAPI(title="Library - cga")

books={
    1:{'titulo':'libro1'},
    2:{'titulo':'libro2'},
    3:{'titulo':'libro3'}
}

@app.get("/books/{book_id}")
async def get_book_by_id(book_id:int):
    if book_id not in books.keys():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Libro no encontrado; id: {book_id}")
    return books[book_id]        