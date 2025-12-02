# space-orchestrator/app.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import json
import os
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# Inicializar la aplicación FastAPI
app = FastAPI()

# --- Middleware de CORS ---
# Permite que el frontend (desde cualquier origen) se comunique con este backend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite solicitudes de cualquier origen
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos HTTP (GET, POST, etc.)
    allow_headers=["*"],  # Permite todas las cabeceras
)

# --- Configuración del Modelo de Lenguaje ---
# Usaremos un LLM muy pequeño, ideal para clasificación de intenciones y CPU.
# "microsoft/phi-2" es una buena opción de tamaño reducido.
model_id = "microsoft/phi-2"
tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
# Configuramos el pad_token para eliminar warnings durante la generación.
tokenizer.pad_token = tokenizer.eos_token
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
    Devuelve una respuesta estructurada.
    """
    # Prompt de sistema mucho más directo y con ejemplos claros (Few-shot prompting)
    system_prompt = """Tu tarea es clasificar la intención del usuario y responder SOLAMENTE con un objeto JSON. No añadas texto antes ni después.

Ejemplos:
Usuario: hola como estas
Tu JSON: {"action": "chat", "response": "¡Hola! Estoy bien, gracias por preguntar. ¿En qué puedo ayudarte hoy?"}

Usuario: puedes crear una foto de un gato con sombrero
Tu JSON: {"action": "generate_image", "prompt": "un gato con sombrero"}

Usuario: quiero hablar
Tu JSON: {"action": "chat", "response": "Claro, ¡hablemos! ¿De qué te gustaría conversar?"}
"""

    full_prompt = f"{system_prompt}\nUsuario: {user_prompt}\nTu JSON:"

    # Tokenizamos la entrada para obtener su longitud
    inputs = tokenizer(full_prompt, return_tensors="pt")
    input_ids = inputs.input_ids
    attention_mask = inputs.attention_mask
    input_length = input_ids.shape[1]

    # Generamos la respuesta, pidiendo solo los tokens *nuevos*
    outputs = model.generate(
        input_ids,
        attention_mask=attention_mask,
        max_new_tokens=150,  # Suficiente para un JSON de respuesta
        pad_token_id=tokenizer.eos_token_id
    )

    # Aislamos y decodificamos *únicamente* la parte nueva de la respuesta
    generated_tokens = outputs[0, input_length:]
    generated_text = tokenizer.decode(generated_tokens, skip_special_tokens=True)

    # --- Parseador de JSON sobre el texto aislado ---
    try:
        start = generated_text.find('{')
        end = generated_text.rfind('}') + 1
        if start != -1 and end != -1:
            json_part = generated_text[start:end]
            response_json = json.loads(json_part)
            return response_json
        else:
            raise ValueError("No se encontró un objeto JSON en el texto generado.")

    except (json.JSONDecodeError, ValueError) as e:
        print(f"Error al decodificar la respuesta del LLM: {e}")
        print(f"Texto generado problemático: {generated_text}")
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
