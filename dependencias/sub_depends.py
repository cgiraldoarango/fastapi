from fastapi import FastAPI, Depends, Header, HTTPException
from typing import Annotated

app = FastAPI()

# 1. Dependencia base: Extrae un token de las cabeceras HTTP
async def get_query_or_token(q: str | None = None, token: str | None = Header(None)):
    if token:
        return token
    if q:
        return q
    raise HTTPException(status_code=400, detail="No token or query provided")

# 2. Sub-dependencia: Depende de la primera para hacer algo adicional
async def get_current_user(token: Annotated[str, Depends(get_query_or_token)]):
    # Aquí simularíamos buscar al usuario en base de datos usando el token
    if token == "cga-admin-secret":
        return {"username": "Carlos Giraldo", "role": "admin"}
    return {"username": "Invitado", "role": "user"}

# 3. Endpoint final: Solo depende de la última sub-dependencia
@app.get("/users/me")
async def read_user_me(current_user: Annotated[dict, Depends(get_current_user)]):
    return {"message": "Acceso concedido", "user": current_user}