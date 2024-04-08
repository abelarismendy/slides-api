from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import os

app = FastAPI()

class Presentation:
    def __init__(self, id, name, num_slides, img_names):
        self.id = id
        self.name = name
        self.num_slides = num_slides
        self.img_names = img_names

# Supongamos que tienes un diccionario de presentaciones
presentations = {
    "1": Presentation("1", "Presentacion 1", 2, ["s1.jpg", "s2.jpg"]),
    "2": Presentation("2", "Presentacion 2", 2, []),
}

@app.get("/presentacion/")
async def get_presentations():
    return [{"id": p.id, "name": p.name} for p in presentations.values()]

@app.get("/presentacion/{id}")
async def get_presentation(id: str):
    if id not in presentations:
        raise HTTPException(status_code=404, detail="Presentation not found")
    return presentations[id]

@app.get("/presentacion/{id}/{img_name}")
async def get_image(id: str, img_name: str):
    if id not in presentations or img_name not in presentations[id].img_names:
        raise HTTPException(status_code=404, detail="Image not found")

    # Asegúrate de que la ruta a tus imágenes sea correcta
    file_path = f"./presentations/{id}/{img_name}"
    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail="Image not found")

    return FileResponse(file_path)
