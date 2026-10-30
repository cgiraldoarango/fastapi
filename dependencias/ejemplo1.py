from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException

app = FastAPI()



async def get_skip_limit(skip: str | int = 0, limit: str | int = 100):
    return {"skip": skip, "limit": limit}


@app.get("/")
async def get_root():
    return {"Message": "Hello everyone"}

@app.get("/items/")
async def get_items(datos: Annotated[get_skip_limit, Depends(get_skip_limit)]):
    return {"mi-limite":datos["limit"],"mi_salto":datos['skip']} 
