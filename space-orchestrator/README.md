# Servicio Orquestador - "El Cerebro" para Carl IA

Este es el backend principal de Carl IA. Utiliza un Modelo de Lenguaje (LLM) para interpretar las peticiones de los usuarios y coordinar acciones, como llamar a otros servicios (por ejemplo, el generador de imágenes).

## Cómo Ejecutarlo en un Hugging Face Space

1.  **Crea un nuevo Space:** Ve a [Hugging Face Spaces](https://huggingface.co/new-space) y crea un nuevo Space.
2.  **Elige el SDK:** Selecciona el SDK de **"Docker"** y elige la plantilla **"Blank"**.
3.  **Sube los Archivos:** Sube los archivos de esta carpeta (`app.py`, `requirements.txt` y este `README.md`) a tu nuevo Space.
4.  **Configura el Puerto:** En la configuración del Space, asegúrate de que el puerto de la aplicación sea **7860**.
5.  **Añade una Variable de Entorno (Secret):**
    *   Ve a la configuración de tu Space y busca la sección "Secrets".
    *   Crea un nuevo "secret" con el nombre `IMAGE_SERVICE_URL`.
    *   En el valor, pega la URL completa de tu Space de generación de imágenes (el que creamos en el paso anterior). Por ejemplo: `https://tu-usuario-tu-space-artista.hf.space/generate-image/`.
6.  **Crea un `Dockerfile`:** Crea un archivo llamado `Dockerfile` en tu Space con el siguiente contenido:

    ```Dockerfile
    FROM python:3.9-slim
    WORKDIR /code
    COPY ./requirements.txt /code/requirements.txt
    RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
    COPY . /code/
    CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
    ```

El Space instalará las dependencias y ejecutará el servicio. Este actuará como el punto de entrada principal para tu frontend.
