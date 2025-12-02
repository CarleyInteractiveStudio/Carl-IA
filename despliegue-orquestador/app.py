# space-orchestrator/app.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import json
import os
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# Inicializar la aplicación FastAPI
app = FastAPI()

# --- Configuración del Modelo de Lenguaje ---
# Usaremos un LLM muy pequeño, ideal para clasificación de intenciones y CPU.
# "microsoft/phi-2" es una buena opción de tamaño reducido.
model_id = "microsoft/phi-2"
tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype=torch.float32, # float32 para CPU
    trust_remote_code=True
)

# --- URL del Servicio de Imágenes ---
# IMPORTANTE: Deberás reemplazar esto con la URL de tu Space de imágenes una vez que lo despliegues.
IMAGE_SERVICE_URL = os.getenv("IMAGE_SERVICE_URL", "http://localhost:8001/generate-image/")

# --- Definición de la Petición ---
class ChatRequest(BaseModel):
    prompt: str

# --- Lógica del "Código Secreto" ---
def generate_llm_response(user_prompt: str):
    """
    Usa el LLM para decidir si el usuario quiere una imagen o solo chatear.
    Devuelve una respuesta estructurada (nuestro "código secreto").
    """
    # Un prompt de sistema simple para guiar al LLM
    system_prompt = (
        "Eres Carl, un asistente de IA. Tu trabajo es determinar si el usuario quiere generar una imagen o simplemente chatear. "
        "Si el usuario quiere una imagen, responde en formato JSON con la clave 'action' como 'generate_image' y 'prompt' con el texto para la imagen. "
        "Si el usuario solo quiere chatear, responde con la clave 'action' como 'chat' y 'response' con tu respuesta en texto. "
        "Ejemplo para imagen: {\"action\": \"generate_image\", \"prompt\": \"un astronauta en un caballo\"}. "
        "Ejemplo para chat: {\"action\": \"chat\", \"response\": \"¡Hola! ¿Cómo puedo ayudarte hoy?\"}."
    )

    full_prompt = f"{system_prompt}\n\nUsuario: {user_prompt}\nCarl:"

    inputs = tokenizer(full_prompt, return_tensors="pt", return_attention_mask=False)

    # Generar la respuesta
    outputs = model.generate(**inputs, max_length=200)
    text_output = tokenizer.batch_decode(outputs)[0]

    # Extraer solo la respuesta JSON de Carl
    try:
        # Buscamos el inicio del JSON
        json_part = text_output.split("Carl:")[1].strip()
        # Limpiamos cualquier texto extra que el modelo pueda añadir después del JSON
        if "}" in json_part:
            json_part = json_part.split("}")[0] + "}"

        response_json = json.loads(json_part)
        return response_json
    except (json.JSONDecodeError, IndexError) as e:
        print(f"Error al decodificar la respuesta del LLM: {e}")
        print(f"Texto de salida problemático: {text_output}")
        # Si el LLM falla, damos una respuesta por defecto
        return {"action": "chat", "response": "No pude entender tu petición. ¿Podrías reformularla?"}

# --- Endpoint de la API ---
@app.post("/chat/")
async def chat_with_carl(request: ChatRequest):
    """
    Recibe un prompt del usuario, lo procesa con el LLM y actúa en consecuencia.
    """
    user_prompt = request.prompt
    print(f"Recibido prompt del usuario: {user_prompt}")

    # 1. Obtener la respuesta estructurada del LLM
    structured_response = generate_llm_response(user_prompt)
    action = structured_response.get("action")

    if action == "generate_image":
        # 2. El LLM decidió generar una imagen
        image_prompt = structured_response.get("prompt", "una imagen aleatoria")
        print(f"LLM decidió generar una imagen con el prompt: '{image_prompt}'")

        try:
            # 3. Llamar a la API del servicio de imágenes
            response_from_artist = requests.post(IMAGE_SERVICE_URL, json={"prompt": image_prompt})

            if response_from_artist.status_code == 200:
                # Si la respuesta es exitosa, devolvemos la imagen directamente
                return {"type": "image", "content": response_from_artist.content.hex()}
            else:
                raise HTTPException(status_code=500, detail="El servicio de imágenes falló.")

        except requests.exceptions.RequestException as e:
            print(f"Error al conectar con el servicio de imágenes: {e}")
            raise HTTPException(status_code=500, detail="No se pudo conectar con el servicio de imágenes.")

    elif action == "chat":
        # 4. El LLM decidió solo chatear
        chat_response = structured_response.get("response", "No sé qué decir.")
        print(f"LLM decidió chatear con la respuesta: '{chat_response}'")
        return {"type": "text", "content": chat_response}

    else:
        # 5. Respuesta por defecto si el LLM no se comporta
        return {"type": "text", "content": "Hubo un error al procesar tu solicitud."}


# --- Endpoint de Bienvenida ---
@app.get("/")
def read_root():
    return {"status": "Servicio orquestador 'El Cerebro' está en línea."}
