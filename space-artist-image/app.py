# space-artist-image/app.py
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
import torch
from diffusers import AutoPipelineForText2Image
import os

# Inicializar la aplicación FastAPI
app = FastAPI()

# --- Configuración del Modelo ---
# Usaremos un modelo muy pequeño y rápido, optimizado para CPU.
# "Lykon/dreamshaper-8-lcm" es una buena opción para prototipos rápidos.
model_id = "Lykon/dreamshaper-8-lcm"
pipe = AutoPipelineForText2Image.from_pretrained(
    model_id,
    torch_dtype=torch.float32, # Usamos float32 para CPU
    variant="fp32"
)
# No moveremos el pipeline a CUDA, se quedará en CPU.

# --- Definición de la Petición ---
class ImageRequest(BaseModel):
    prompt: str

# --- Endpoint de la API ---
@app.post("/generate-image/")
async def generate_image(request: ImageRequest):
    """
    Recibe un prompt de texto y genera una imagen.
    """
    try:
        prompt = request.prompt
        print(f"Recibido prompt: {prompt}")

        # Generar la imagen
        # Usamos pocas iteraciones para que sea rápido en CPU
        image = pipe(
            prompt=prompt,
            num_inference_steps=4,
            guidance_scale=7.5
        ).images[0]

        # Guardar la imagen temporalmente
        output_path = "generated_image.png"
        image.save(output_path)

        print(f"Imagen generada y guardada en {output_path}")

        # Devolver la imagen como un archivo
        return FileResponse(output_path, media_type="image/png")

    except Exception as e:
        print(f"Error durante la generación de imagen: {e}")
        raise HTTPException(status_code=500, detail="Error al generar la imagen.")

# --- Endpoint de Bienvenida ---
@app.get("/")
def read_root():
    return {"status": "Servicio de generación de imágenes 'El Artista' está en línea."}
