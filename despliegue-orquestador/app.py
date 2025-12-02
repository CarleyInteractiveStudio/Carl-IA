# space-orchestrator/app.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# --- Inicialización de la App ---
app = FastAPI()

# --- Middleware de CORS ---
# Permite la comunicación desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Configuración del Modelo de Lenguaje ---
# Usamos un modelo ligero y optimizado para CPU
model_id = "microsoft/phi-2"
tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
tokenizer.pad_token = tokenizer.eos_token
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype=torch.float32,
    trust_remote_code=True
)

# --- Definición de la Petición ---
class ChatRequest(BaseModel):
    prompt: str

# --- Lógica de Chat Simplificada ---
def generate_chat_response(user_prompt: str):
    """
    Genera una respuesta conversacional directa usando el LLM.
    """
    # El nuevo prompt del sistema: simple, directo y conversacional.
    system_prompt = """Eres Carl IA, un asistente virtual diseñado para ayudar a los usuarios. Tu objetivo es ser amable y servicial.

Actualmente, tus funciones más avanzadas (como generar imágenes, música, sitios web o videojuegos) están en desarrollo y no están disponibles por falta de recursos y servidores potentes. El objetivo del proyecto es conseguir apoyo para poder implementar estas características en el futuro utilizando modelos de código abierto.

Por ahora, tu única función es chatear con los usuarios. Responde a sus preguntas de forma natural y explica tus limitaciones si te preguntan por funciones avanzadas.
"""

    # Creamos una conversación simple: el sistema da instrucciones, el usuario pregunta.
    full_prompt = f"{system_prompt}\nUsuario: {user_prompt}\nCarl IA:"

    # Tokenizamos la entrada
    inputs = tokenizer(full_prompt, return_tensors="pt")
    input_ids = inputs.input_ids
    attention_mask = inputs.attention_mask
    input_length = input_ids.shape[1]

    # Generamos la respuesta, pidiendo solo los tokens nuevos
    outputs = model.generate(
        input_ids,
        attention_mask=attention_mask,
        max_new_tokens=150,  # Límite para la longitud de la respuesta
        pad_token_id=tokenizer.eos_token_id,
        do_sample=True, # Hace la respuesta más natural y menos repetitiva
        temperature=0.7,
        top_p=0.9
    )

    # Aislamos y decodificamos únicamente la parte nueva de la respuesta
    generated_tokens = outputs[0, input_length:]
    generated_text = tokenizer.decode(generated_tokens, skip_special_tokens=True)

    return generated_text.strip()

# --- Endpoint de la API ---
@app.post("/chat/")
async def chat_with_carl(request: ChatRequest):
    """
    Recibe un prompt del usuario y devuelve una respuesta de texto simple.
    """
    user_prompt = request.prompt
    print(f"Recibido prompt del usuario: {user_prompt}")

    # 1. Generar la respuesta del chat
    chat_response = generate_chat_response(user_prompt)
    print(f"Respuesta generada por Carl IA: '{chat_response}'")

    # 2. Devolver la respuesta directamente
    # El frontend espera un JSON con "type" y "content".
    return {"type": "text", "content": chat_response}

# --- Endpoint de Bienvenida ---
@app.get("/")
def read_root():
    return {"status": "Servicio de Chat 'Carl IA' está en línea."}
