# Servicio de Imágenes - "El Artista" para Carl IA

Este es un servicio de backend construido con FastAPI que expone un modelo de IA para generar imágenes a partir de texto.

## Cómo Ejecutarlo en un Hugging Face Space

1.  **Crea un nuevo Space:** Ve a [Hugging Face Spaces](https://huggingface.co/new-space) y crea un nuevo Space.
2.  **Elige el SDK:** Selecciona el SDK de **"Docker"** y elige la plantilla **"Blank"**.
3.  **Sube los Archivos:** Sube los archivos de esta carpeta (`app.py`, `requirements.txt` y este `README.md`) a tu nuevo Space.
4.  **Configura el Puerto:** En la configuración del Space, asegúrate de que el puerto de la aplicación sea **7860**.
5.  **Crea un `Dockerfile`:** Crea un archivo llamado `Dockerfile` en tu Space con el siguiente contenido:

    ```Dockerfile
    FROM python:3.9-slim
    WORKDIR /code
    COPY ./requirements.txt /code/requirements.txt
    RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
    COPY . /code/
    CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
    ```

El Space instalará las dependencias y ejecutará el servicio. Una vez que esté en línea, podrás hacerle peticiones a la URL de tu Space.
