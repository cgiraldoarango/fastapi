from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated

app = FastAPI(title="Libreria-Autenticada")
oauth2_schema = OAuth2PasswordBearer(tokenUrl="token")

bd = {
    "cga": {
        "usuario": "cga",
        "full_name": "carlos giraldo arango",
        "password_hash": "hash_secreto_cga",
    },
    "pedro": {
        "usuario": "pedro_gomez",
        "full_name": "pedro gomez martinez",
        "password_hash": "hash_secreto_pedro",
    },
}

bd_libros = {
    "uno": {"title": "titulo uno", "author": "autor1"},
    "dos": {"title": "titulo dos", "author": "author2"},
}


"""Simular el hash"""


def simulate_password_hash(plain_password: str) -> str:
    return "hash_secreto_" + plain_password


user_data = {}


@app.post("/token")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends(OAuth2PasswordRequestForm)],
):
    global user_data
    user_data = bd.get(form_data.username)

    if not user_data or user_data["password_hash"] != simulate_password_hash(
        form_data.password
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"access_token": user_data["password_hash"], "token_type": "bearer"}


@app.get("/")
async def get_root():
    return {"message": "Debes loguear para ingresar"}


@app.get("/books/")
async def get_books(token: Annotated[str, Depends(oauth2_schema)]):
    return {
        "usuario": user_data["usuario"],
        "full_name": user_data["full_name"],
        "libros": bd_libros,
    }
