from fastapi import FastAPI, Depends, Form, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from fastapi.responses import HTMLResponse

app = FastAPI(title="Formulario personal")

oath2_schema = OAuth2PasswordBearer(tokenUrl="token")

db_users = {
    "cga": {"user": "cga", "password_hash": "hash_cga"},
    "pedro": {"user": "pedro", "password_hash": "hash_pedro"},
}

db_books = {
    "uno": {"title": "libro uno"},
    "dos": {"title": "libro dos"},
    "tres": {"title": "libro tres"},
}


def simulate_hash(pass_enter: str):
    return "hash_" + pass_enter


@app.get("/")
async def get_root():
    return {"message": "Bienvenido"}


"""obtener los libros"""


@app.get("/books")
async def get_books(token: Annotated[str, Depends(oath2_schema)]):
    return db_books


@app.post("/token")
async def login(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    usuario = db_users.get(username)
    if not usuario or usuario["password_hash"] != simulate_hash(password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="error usuario",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"access_token": password, "token_type": "bearer"}
