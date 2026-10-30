from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import HTMLResponse
from typing import Annotated

app = FastAPI(title="API de Subida de Archivos - Librería CGA")

@app.post("/books/upload-cover")
async def create_book_with_cover(
    title: Annotated[str, Form(min_length=3)],
    author: Annotated[str, Form(min_length=3)],
    cover_image: Annotated[UploadFile, File()]
):
    # Leemos el contenido del archivo de forma asíncrona
    content = await cover_image.read()
    file_size = len(content)
    
    # Aquí podrías guardar el archivo físicamente en disco o en la nube (S3, etc.)
    # Por ahora, retornamos los metadatos para verificar que llegó correctamente
    return {
        "message": "Libro y portada recibidos con éxito",
        "book_title": title,
        "author": author,
        "filename": cover_image.filename,
        "content_type": cover_image.content_type,
        "size_in_bytes": file_size
    }

@app.get("/")
async def main_form():
    # Creamos un formulario web clásico para probar la subida de archivos fácilmente
    html_content = """
    <body>
        <h1>Registro de Libros con Portada [Librería CGA]</h1>
        <form action="/books/upload-cover" enctype="multipart/form-data" method="post">
            <p>
                <label>Título del libro:</label><br>
                <input name="title" type="text" required />
            </p>
            <p>
                <label>Autor:</label><br>
                <input name="author" type="text" required />
            </p>
            <p>
                <label>Imagen de portada:</label><br>
                <input name="cover_image" type="file" accept="image/*" required />
            </p>
            <p>
                <input type="submit" value="Subir Libro y Portada" />
            </p>
        </form>
    </body>
    """
    return HTMLResponse(content=html_content)