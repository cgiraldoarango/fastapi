from fastapi import APIRouter, HTTPException

# Creamos el router con un prefijo común y una etiqueta para la documentación
router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# Base de datos simulada en memoria
fake_users_db = {"1": {"name": "Alice"}, "2": {"name": "Bob"}}

@router.get("/")
async def get_users():
    return fake_users_db

@router.get("/{user_id}")
async def get_user(user_id: str):
    if user_id not in fake_users_db:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return fake_users_db[user_id]