from collections.abc import AsyncIterable
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Ejemplo de Stream JSON Lines")


class Item(BaseModel):
    name: str
    description: str | None = None


# Una lista simulada de elementos pesados o numerosos
items_database = [
    Item(name="Plumbus", description="Un dispositivo casero multiusos."),
    Item(
        name="Portal Gun", description="Una pistola para abrir portales dimensionales."
    ),
    Item(name="Meeseeks Box", description="Una caja que invoca a un Meeseeks."),
]


@app.get("/items/stream")
async def stream_items() -> AsyncIterable[Item]:
    for item in items_database:
        # Simulamos una pequeña pausa de procesamiento o consulta por cada ítem
        # (en la vida real aquí podrías consultar una base de datos asíncrona)
        yield item
