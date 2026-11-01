from fastapi import APIRouter, Depends, HTTPException, Header

# Función de dependencia que valida una cabecera de seguridad
async def verify_bookstore_token(x_token: str = Header(...)):
    if x_token != "admin-secreto-123":
        raise HTTPException(status_code=403, detail="Token de librería inválido o ausente")
    return {"libreria_autorizada": True}

# Creamos el APIRouter aplicando la dependencia a nivel de router completo
router = APIRouter(
    prefix="/books",
    tags=["Books"],
    dependencies=[Depends(verify_bookstore_token)] # <--- ¡Aquí ocurre la magia!
)

@router.get("/")
def get_books():
    # Esta ruta está protegida automáticamente por la dependencia del router
    return [{"id": 1, "title": "FastAPI Avanzado"}, {"id": 2, "title": "Arquitectura Modular"}]

@router.post("/")
def create_book():
    # Esta ruta también está protegida automáticamente sin repetir código
    return {"mensaje": "Libro creado exitosamente"}