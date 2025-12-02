# Carl IA - Un Ecosistema de IA Distribuido

¡Bienvenido al repositorio de Carl IA! Este proyecto implementa un asistente de IA conversacional con la capacidad de coordinar múltiples modelos de IA "especialistas" para realizar tareas complejas como la generación de imágenes, música y más.

La arquitectura está diseñada para ser modular y escalable, utilizando Hugging Face Spaces para desplegar cada componente de forma independiente.

---

## Arquitectura del Proyecto

El proyecto está dividido en tres componentes principales:

1.  **`frontend/`**: La interfaz de chat con la que interactúa el usuario. Es una aplicación web estática construida con HTML, CSS y JavaScript.
2.  **`space-orchestrator/`**: El "Cerebro" de Carl. Este es un servicio de backend que recibe los mensajes del usuario, utiliza un Modelo de Lenguaje (LLM) para interpretar la intención y llama a otros servicios de IA cuando es necesario.
3.  **`space-artist-image/`**: Un servicio "especialista" dedicado a la generación de imágenes. Recibe órdenes del orquestador y devuelve la imagen generada.

---

## Cómo Desplegar el Ecosistema en Hugging Face

Para poner en marcha a Carl, necesitas desplegar los dos servicios de backend en Hugging Face Spaces y configurar el frontend para que apunte al orquestador.

### Paso 1: Desplegar el Servicio de Imágenes ("El Artista")

1.  **Ve a la carpeta `space-artist-image/`.**
2.  Sigue las instrucciones detalladas en el archivo **`space-artist-image/README.md`**.
3.  Una vez desplegado, copia la URL de tu nuevo Space. La necesitarás para el siguiente paso.

### Paso 2: Desplegar el Servicio Orquestador ("El Cerebro")

1.  **Ve a la carpeta `space-orchestrator/`.**
2.  Sigue las instrucciones del archivo **`space-orchestrator/README.md`**.
3.  **Importante:** Durante la configuración, asegúrate de añadir la URL del Space del "Artista" como un "secret" llamado `IMAGE_SERVICE_URL`.
4.  Una vez desplegado, copia la URL de este Space.

### Paso 3: Configurar y Probar el Frontend

1.  **Abre el archivo `frontend/script.js`**.
2.  Busca la línea que dice: `const ORCHESTRATOR_URL = "http://localhost:8000/chat/";`.
3.  **Reemplaza la URL de ejemplo** con la URL de tu Space "Cerebro" que copiaste en el paso anterior.
4.  ¡Listo! Ahora puedes abrir el archivo `frontend/index.html` en tu navegador. El chat se conectará a tu backend en Hugging Face.

---

## Modelos de IA Recomendados (Para Futuras Mejoras)

A continuación se encuentra una lista de modelos de IA de código abierto recomendados para escalar y mejorar las capacidades de Carl. Todos tienen licencias que permiten su uso comercial.

### Generación de Video
- **WanVideo 2.1:** [GitHub](https://github.com/Wan-Video/Wan2.1), [Hugging Face](https://huggingface.co/Wan-AI/Wan2.1-T2V-14B)
  - **Licencia:** Apache 2.0

### Generación de Imágenes
- **Stable Diffusion:** [GitHub](https://github.com/CompVis/stable-diffusion), [Hugging Face](https://huggingface.co/stabilityai/stable-diffusion-3-medium)
  - **Licencia:** CreativeML OpenRAIL-M
- **FLUX.1 (schnell):** [Hugging Face](https://huggingface.co/black-forest-labs/FLUX.1-schnell)
  - **Licencia:** Apache 2.0

### Modelos de Lenguaje (LLM)
- **Llama 3:** [GitHub](https://github.com/meta-llama/llama3), [Hugging Face](https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct)
  - **Licencia:** Llama 3 License

### Generación de Música
- **Riffusion:** [GitHub](https://github.com/riffusion/riffusion), [Hugging Face](https://huggingface.co/riffusion/riffusion-model-v1)
  - **Licencia:** MIT (para uso auto-hospedado)

### Edición y Eliminación de Fondo
- **withoutBG:** [GitHub](https://github.com/withoutbg/withoutbg)
  - **Licencia:** Apache 2.0
- **Stable Diffusion (Inpainting/Outpainting):** Mismos enlaces que arriba.
