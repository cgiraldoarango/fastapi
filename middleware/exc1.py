from fastapi import FastAPI, Depends, HTTPException, status, Path, Body, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
import jwt
from pwdlib import PasswordHash
from typing import Annotated
from datetime import datetime, timedelta, timezone
from datetime import time

"""instancia de fastapi"""
app = FastAPI(title="Middleware . cga")

"""instancia del Passwordhash"""
pshash = PasswordHash.recommended()

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

jwtencode: str

"""Esquema para autenticación de usuarios"""
oauth2_schema = OAuth2PasswordBearer(tokenUrl="token")

"""**************MODELS******************"""


class User(BaseModel):
    username: str
    full_name: str
    email: str
    enabled: bool


class UserInDB(User):
    password_hash: str


class Token(BaseModel):
    access_token: str
    token_type: str


"""==============END MODELS========="""


"""********************Funcion para crear hash*********************"""


def create_hash(plainpassword: str):
    return pshash.hash(plainpassword)


"""===============fin funcion hash================"""

bd_users = {
    "cga": {
        "username": "cga",
        "full_name": "carlos giraldo arango",
        "email": "cga@gmail.com",
        "password_hash": create_hash("cga123"),  # clave cga123
        "enabled": True,
    },
    "pedro": {
        "username": "pedro",
        "full_name": "pedro gomez martinez",
        "email": "pedro@gmail.com",
        "password_hash": create_hash("pedro123"),  # clave cga123
        "enabled": False,
    },
}

bd_libros = {
    "uno": {"id": "uno", "titulo": "titulo uno"},
    "dos": {"id": "dos", "titulo": "titulo dos"},
}

"""*********************FUNCIONES****************"""
"""Calcular el tiempo con un middleware
"""


@app.middleware("http")
async def get_tiempo(request: Request, call_next):
    start_time = datetime.now().time().microsecond

    response = await call_next(request)

    finall_time = datetime.now().time().microsecond - start_time
    response.headers["X-Process-time-cga"] = str(finall_time)
    return response


# VERIFICAR EL HASH
def verify_hash(plain_password: str, hash_password):
    return pshash.verify(plain_password, hash_password)


# obtener el usuario
def get_user(bd, username: str, password: str):
    user_in = bd.get(username)
    if not user_in:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
        )
    validate_user = verify_hash(password, user_in["password_hash"])
    if validate_user:
        return user_in


# crear token
def create_token(jcode: dict, ky: str, algorithm: str, delta: timedelta | None = None):
    global jwtencode
    jsencode = jcode.copy()
    if delta:
        exp = datetime.now(timezone.utc) + timedelta(delta)
    else:
        exp = datetime.now(timezone.utc) + timedelta(minutes=15)

    jsencode.update({"exp": exp})
    jwtencode = jwt.encode(algorithm=algorithm, payload=jsencode, key=ky)
    return jwtencode


"""Obtener un dict a partir del token"""


def get_dict_by_token(token: Token) -> dict:
    decodejwt = jwt.decode(token, SECRET_KEY, ALGORITHM)
    return decodejwt


"""=========================FIN FUNCIONES=============="""

""" ************************ENDPOINTS******************"""


@app.post("/token")
async def get_token(
    data_form: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = get_user(bd_users, data_form.username, data_form.password)
    user["sub"] = data_form.username
    token_return = create_token(
        algorithm=ALGORITHM,
        jcode=user,
        ky=SECRET_KEY,
        delta=ACCESS_TOKEN_EXPIRE_MINUTES,
    )

    return {"access_token": token_return, "token_type": "bearer"}


@app.post("/me")
async def get_me(
    usuario: Annotated[str, Depends(oauth2_schema)], name: Annotated[str, Body()]
):
    ##prueba obtener los datos del usuario a partir del token
    datos_user = get_dict_by_token(jwtencode)
    user = User(**datos_user)
    return user


@app.get("/libros")
async def get_libro(token: Annotated[str, Depends(oauth2_schema)]):
    user_by_token = get_dict_by_token(token)
    if user_by_token["enabled"]:
        return {"user": user_by_token["sub"], "libros": bd_libros}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="No está activo"
        )
