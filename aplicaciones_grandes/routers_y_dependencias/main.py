from fastapi import FastAPI
from routers import books

app = FastAPI(title="Mi Librería Empresarial")

# Conectamos el router a la aplicación principal
app.include_router(books.router)

@app.get("/")
def root():
    return {"mensaje": "Bienvenido al sistema público de la API"}