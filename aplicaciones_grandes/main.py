from fastapi import FastAPI
from routers import users

app = FastAPI(title="Mi Aplicación Modular con FastAPI")

# Conectamos el router a nuestra aplicación principal
app.include_router(users.router)

@app.get("/")
async def root():
    return {"message": "Bienvenido a la API principal"}