# Carl IA - Un Ecosistema de IA Distribuido

¡Bienvenido al repositorio de Carl IA! Este proyecto implementa un asistente de IA conversacional diseñado con una arquitectura de microservicios, listo para ser desplegado en Hugging Face Spaces.

---

## Cómo Desplegar el Ecosistema

Para poner en marcha a Carl, solo necesitas desplegar los dos servicios de backend y luego configurar el frontend. Hemos simplificado el proceso para que sea lo más directo posible.

### Paso 1: Desplegar el Servicio de Imágenes ("El Artista")

1.  **Descarga los archivos:** Ve a la carpeta `despliegue-artista` y descarga los tres archivos que contiene:
    *   `app.py`
    *   `requirements.txt`
    *   `Dockerfile`
2.  **Crea un nuevo Space en Hugging Face:**
    *   Ve a [Hugging Face Spaces](https://huggingface.co/new-space).
    *   Dale un nombre a tu Space (ej: `carl-ia-artista`).
    *   En "Select the Space SDK", elige **Docker** y luego la plantilla **"Blank"**.
3.  **Sube los archivos:** Sube los tres archivos que descargaste a la raíz de tu nuevo Space.
4.  **Espera a que se construya:** El Space se construirá automáticamente. Esto puede tardar varios minutos. Una vez que veas el estado "Running", ¡tu servicio estará en línea!
5.  **Copia la URL:** Guarda la URL de tu Space (ej: `https://tu-usuario-carl-ia-artista.hf.space`). La necesitarás en el siguiente paso.

### Paso 2: Desplegar el Servicio Orquestador ("El Cerebro")

1.  **Descarga los archivos:** Ve a la carpeta `despliegue-orquestador` y descarga los tres archivos que contiene.
2.  **Crea un segundo Space en Hugging Face:**
    *   Sigue los mismos pasos que antes, creando un nuevo Space con **Docker** y la plantilla **"Blank"**.
3.  **Añade el Secret:**
    *   Antes de subir los archivos, ve a la pestaña "Settings" de este nuevo Space.
    *   Busca la sección "Secrets" y crea un nuevo "secret" con el nombre `IMAGE_SERVICE_URL`.
    *   En el valor, pega la URL completa de tu Space "Artista" del paso anterior, asegurándote de que termine en `/generate-image/`.
        *   Ejemplo: `https://tu-usuario-carl-ia-artista.hf.space/generate-image/`
4.  **Sube los archivos:** Sube los tres archivos que descargaste para el orquestador.
5.  **Copia la URL:** Una vez que esté en "Running", copia la URL de este Space.

### Paso 3: Configurar y Probar el Frontend

1.  **Abre el archivo `frontend/script.js`**.
2.  Busca la línea que dice: `const ORCHESTRATOR_URL = "http://localhost:8000/chat/";`.
3.  **Reemplaza la URL de ejemplo** con la URL de tu Space "Cerebro" del paso 2, asegurándote de que termine en `/chat/`.
    *   Ejemplo: `https://tu-usuario-carl-ia-cerebro.hf.space/chat/`
4.  ¡Listo! Ahora puedes abrir el archivo `frontend/index.html` en tu navegador para chatear con Carl.

---

## Estructura del Repositorio

-   **`frontend/`**: Contiene el código de la interfaz de usuario.
-   **`despliegue-artista/`**: Archivos listos para desplegar el servicio de imágenes.
-   **`despliegue-orquestador/`**: Archivos listos para desplegar el servicio principal.
-   **`space-orchestrator/` / `space-artist-image/`**: Carpetas de desarrollo originales.
