"""En términos sencillos, una dependencia es simplemente 
una función (o cualquier objeto llamable) que se encarga 
de realizar una tarea previa, validar algo o preparar datos 
antes de que se ejecute la función principal de tu endpoint. 
FastAPI se encarga de ejecutarla automáticamente, pasarle los 
parámetros que necesite y entregarle el resultado a tu endpoint."""

from fastapi import FastAPI, Depends
from typing import Annotated

app = FastAPI()

# 1. Creamos la función de dependencia
async def common_parameters(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}

# 2. La inyectamos en el endpoint usando Depends
@app.get("/items/")
async def read_items(commons: Annotated[dict, Depends(common_parameters)]):
    return {"message": "Lista de items", "pagination": commons}