from fastapi import FastAPI, Depends, HTTPException, status
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI(title="api credenciales")


@app.get("/")
async def get_root():
    return {"message": "Hello"}


oauth2_schema = OAuth2PasswordBearer(tokenUrl="token")


@app.post("/token")
async def login(data_form: Annotated[OAuth2PasswordRequestForm, Depends()]):
    if data_form.username != "carlosg" or data_form.password != "123456":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="error credentials"
        )
    return {"access_token": "secreto_" + data_form.username, "token_type": "bearer"}


@app.get("/books/")
async def get_books(token: Annotated[str, Depends(oauth2_schema)]):
    return {"token": token}
