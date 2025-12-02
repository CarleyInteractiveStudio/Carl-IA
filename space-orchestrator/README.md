# Servicio Orquestador - "El Cerebro" para Carl IA

Este es el backend principal de Carl IA. Utiliza un Modelo de Lenguaje (LLM) para interpretar las peticiones de los usuarios y coordinar acciones con otros servicios, como el generador de imágenes.

## Cómo Ejecutarlo en un Hugging Face Space

**IMPORTANTE:** Al crear el Space, asegúrate de seleccionar **Docker** como el SDK. No uses Gradio, Streamlit ni Static.

1.  **Crea un nuevo Space:** Ve a [Hugging Face Spaces](https://huggingface.co/new-space).
    -   Dale un nombre a tu Space.
    -   En "Select the Space SDK", elige **Docker** y luego la plantilla **"Blank"**.
2.  **Añade el Secret:**
    -   Antes de subir los archivos, ve a la pestaña "Settings" de tu Space.
    -   Busca la sección "Secrets" y crea un nuevo "secret" con el nombre `IMAGE_SERVICE_URL`.
    -   En el valor, pega la URL completa de tu Space de generación de imágenes (el que creaste en el paso anterior). Por ejemplo: `https://tu-usuario-tu-space-artista.hf.space/generate-image/`.
3.  **Sube los Archivos:** Ve a la pestaña "Files" y sube todos los archivos de esta carpeta (`app.py`, `requirements.txt` y este `README.md`).
4.  **Crea el `Dockerfile`:**
    -   En la misma pestaña "Files", haz clic en "Add file" y selecciona "Create a new file".
    -   Nombra el archivo `Dockerfile` (sin extensión).
    -   Pega el siguiente contenido y guarda el archivo:
    ```Dockerfile
    FROM python:3.9-slim

    WORKDIR /code

    COPY ./requirements.txt /code/requirements.txt

    RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

    COPY . /code/

    CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
    ```

El Space se construirá automáticamente. Esto puede tardar varios minutos la primera vez mientras descarga el modelo. Una vez que veas el estado "Running", ¡tu servicio estará en línea y listo para recibir peticiones del frontend!
