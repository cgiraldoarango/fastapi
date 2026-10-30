"""📖 Nivel 2: ¿Qué significa usar una Clase como Dependencia?
Hasta ahora hemos usado funciones simples (como verify_token o 
common_parameters) dentro de Depends(). Sin embargo, en Python, 
una clase también es un objeto llamable.

Cuando le pasas una clase directamente a Depends (por ejemplo, 
Depends(MiClase)), FastAPI hace lo siguiente por debajo:

Analiza el método de inicialización (__init__) de esa clase.
Extrae todos los parámetros que recibe el constructor (parámetros 
de consulta, cabeceras, etc.).

Instancia la clase automáticamente ejecutando MiClase(...) con los 
valores que envió el cliente.

Te entrega el objeto ya creado directamente en el parámetro de tu 
endpoint.

¿Por qué es tan útil?
Es ideal cuando tienes un grupo de parámetros relacionados (por ejemplo, 
parámetros de paginación, filtros de búsqueda, ordenamiento) que quieres 
encapsular en un solo objeto para reutilizarlos limpiamente en muchos 
endpoints.

💻 Ejemplo Oficial Básico:
Imagina que queremos manejar la paginación y búsqueda de elementos 
usando una clase:"""

from fastapi import FastAPI, Depends
from typing import Annotated

app = FastAPI(title="Dependencias con clases")

# 1. Creamos una clase que encapsula los parámetros comunes
class CommonQueryParams:
    def __init__(self, skip: int = 0, limit: int = 10, q: str | None = None):
        self.skip = skip
        self.limit = limit
        self.q = q

# 2. La usamos como dependencia en el endpoint
@app.get("/items/")
async def read_items(commons: Annotated[CommonQueryParams, Depends(CommonQueryParams)]):
    response = {"skip": commons.skip, "limit": commons.limit}
    if commons.q:
        response.update({"q": commons.q})
    return response