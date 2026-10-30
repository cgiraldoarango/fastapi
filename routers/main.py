# main.py
from fastapi import FastAPI
from routers import books

app = FastAPI(title="Mi API de Libros Modular", version="1.0")

# Incluimos el router de libros
app.include_router(books.router)

@app.get("/")
async def root():
    return {"message": "Bienvenido a la API modular de FastAPI"}