from fastapi import FastAPI, Header, APIRouter, Depends, Query, HTTPException, status

from typing import Annotated

app = FastAPI(title="Subdependencias cga")

booksRouter = APIRouter(prefix="/books", tags=["Books"])

app.include_router(booksRouter)

"""==================Functions============="""


async def verify_client_token(
    token: Annotated[str | None, Header()] = None,
):
    if token != "cga2026":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token"
        )
    return {"client_id": 1, "role": "editor"}


async def verify_editor_role(user: Annotated[dict, Depends(verify_client_token)]):
    if user["role"] != "editor":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="insuficient credentials"
        )
    return user

"""**************end of functions************"""

"""============endpoints==============="""
@booksRouter.get("/")
async def get_root():
    return {"message": "Wellcome-cga"}


@booksRouter.post("/publish")
async def create_book(data: Annotated[dict, Depends(verify_editor_role)]):
    return data
