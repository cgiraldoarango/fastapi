from typing import Annotated
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse

app = FastAPI(title="Api Form-cga")

books = []


@app.post("/books/form")
async def create_books_form(
    title: Annotated[str, Form(min_length=5)],
    author: Annotated[str, Form(min_length=5)],
    price: Annotated[float, Form(ge=0)],
):
    book = {"author": author, "title": title, "price": price}
    books.append(book)
    return books


@app.get("/books/nuevo")
async def form_data():
    content = """
        <body>
        <h1>Formulario de Datos [Librería CGA]</h1>
        <form style="background-color: #f4f4f4; color: #333333; padding: 
        20px; border-radius: 8px;" action="/books/form" 
        enctype="multipart/form-data" method="post">
        <p><label>Titulo del libro</label>
        <input name="title" type="text" placeholder="titulo"/>
        </p>
        <p><label>Autor del libro</label>
        <input name="author" type="text" placeholder="author"/>
        </p>
        <p><label>Precio del libro</label>
        <input name="price" type="text" placeholder="precio" />
        </p>
        <p><input name="send" type="submit" value="MANDAR"/></p>
        </form>
        </body>
        """
    return HTMLResponse(content=content)
