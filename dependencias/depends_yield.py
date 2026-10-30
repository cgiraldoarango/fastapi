"""📖 Nivel 4: ¿Qué son las dependencias con yield y para qué sirven?
Hasta ahora hemos usado dependencias con return. La función hace su trabajo, 
retorna un valor, y FastAPI lo inyecta en el endpoint. Pero, ¿qué pasa si 
necesitas ejecutar código después de que la petición haya terminado? 
(Por ejemplo, cerrar una conexión a la base de datos para no dejarla abierta 
consumiendo memoria).

Aquí es donde entra en juego la palabra clave yield de Python (creando un generador):

Fase de Configuración (Setup): Todo el código que escribas antes del yield se 
ejecuta antes de que llegue la petición a tu endpoint. El valor que pones al 
lado de yield es el que se inyecta en tu ruta.

Fase de Limpieza (Teardown): Todo el código que escribas después del yield se ejecuta 
después de que el endpoint haya respondido al cliente.

Manejo seguro con try...finally: Si ocurre un error durante la ejecución de la petición, 
FastAPI garantiza que el código de limpieza posterior al yield (o dentro de un bloque finally) 
se ejecute de todas formas, evitando fugas de memoria o conexiones huérfanas.

💻 Ejemplo Oficial Básico:
Imagina que simulamos una conexión a una base de datos que debe abrirse al iniciar 
la petición y cerrarse (o limpiarse) al terminar:"""

from fastapi import FastAPI, Depends

app = FastAPI()

# 1. Creamos una dependencia usando yield
async def get_database_session():
    # SETUP: Se ejecuta antes de la petición
    print(">>> Abriendo conexión a la base de datos...")
    db_session = {"connection": "Activa", "status": "OK"}
    
    try:
        yield db_session # Inyecta este objeto en el endpoint
    finally:
        # TEARDOWN: Se ejecuta siempre al terminar la petición (haya error o éxito)
        print("<<< Cerrando conexión a la base de datos de forma segura...")

# 2. La inyectamos en nuestro endpoint
@app.get("/items/")
async def read_items(db: dict = Depends(get_database_session)):
    return {"message": "Operación realizada", "db_status": db["status"]}