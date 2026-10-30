"""Primera dependencia"""
from fastapi import FastAPI, Depends, HTTPException, status, Query
from pydantic import Field
from typing import Annotated

app = FastAPI(title="Cga-ejemplo")


def verify_token(
    token: Annotated[
        str,
        Query(..., min_length=5),
    ],
):
    if token != "cga2026":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido"
        )
    return token


@app.get("/")
async def get_root():
    return {"message": "Welcome from cga api"}


@app.get("/books/secure/")
async def get_secure_books(token: Annotated[str, Depends(verify_token)]):
    return {"message": "cliente autorizado"}
