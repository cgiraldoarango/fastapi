from fastapi import FastAPI

app = FastAPI()


@app.get("/files/{file_path:path}")
async def get_path(file_path: str):
    return {'archivo':file_path}
