from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated

app = FastAPI(title="Librería CGA - Explicación OAuth2")

# 1. Definimos el esquema indicando la URL donde se obtendrá el token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# 2. Creamos la ruta POST "/token" que procesa el formulario de login 
# (Aquí es donde apunta el 'tokenUrl' configurado arriba)
@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    # Simulamos la validación de usuario y contraseña en base de datos
    if form_data.username != "cga" or form_data.password != "secreto":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario o contraseña incorrectos"
        )
    
    # Retornamos el token de acceso requerido por el estándar OAuth2
    return {"access_token": form_data.username, "token_type": "bearer"}

# 3. Ruta protegida que utiliza el esquema para validar el token recibido
@app.get("/books/secure")
async def read_secure_books(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"message": "¡Acceso concedido!", "token_utilizado": token}