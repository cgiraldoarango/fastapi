from fastapi import FastAPI, APIRouter, Depends
from typing import Annotated

router = APIRouter(prefix="/books",tags=["Books cga"])

app= FastAPI(title="Api yield CGA")

app.include_router(router=router)

def get_book_db_session(user: str):
    print("<<Opening session...>>")
    db={'user':user,'state':'Active'}
    try:
        yield db
    
    finally:
        print("<<Cerrando sesion>>")
    
@router.post("/db-register")
async def set_register(data:  Annotated[dict, Depends(get_book_db_session)]):
    return data


@router.get("/")
async def get_rout():
    return {'message': "hello everyone"}