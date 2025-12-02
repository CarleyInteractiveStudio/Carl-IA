# Modelos de IA Open Source para Carl IA

Este documento contiene una lista curada de modelos de Inteligencia Artificial de código abierto recomendados para potenciar las funcionalidades de **Carl IA**. Todos los modelos listados tienen licencias que permiten su uso comercial.

---

## 1. Generación de Video

### WanVideo 2.1
- **Descripción:** Un modelo de última generación desarrollado por Alibaba que convierte imágenes en videos de alta calidad. A menudo supera a otras soluciones de código abierto y compite con modelos privados.
- **Licencia:** [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0) (Permite uso comercial).
- **Ideal para:** Crear animaciones, clips cortos a partir de imágenes y contenido de video dinámico.
- **Recursos Oficiales:**
  - **GitHub:** [https://github.com/Wan-Video/Wan2.1](https://github.com/Wan-Video/Wan2.1)
  - **Hugging Face:** [https://huggingface.co/Wan-AI/Wan2.1-T2V-14B](https://huggingface.co/Wan-AI/Wan2.1-T2V-14B)

---

## 2. Generación de Imágenes

### Stable Diffusion
- **Descripción:** El modelo más conocido y versátil para generar imágenes a partir de texto. Cuenta con una comunidad enorme, muchísimos tutoriales y modelos pre-entrenados para casi cualquier estilo.
- **Licencia:** [CreativeML OpenRAIL-M](https://huggingface.co/spaces/CompVis/stable-diffusion-license) (Permisiva para uso comercial).
- **Ideal para:** Prácticamente cualquier tarea de generación de imágenes, desde arte fotorrealista hasta ilustraciones de fantasía.
- **Recursos Oficiales:**
  - **GitHub:** [https://github.com/CompVis/stable-diffusion](https://github.com/CompVis/stable-diffusion)
  - **Hugging Face:** [https://huggingface.co/stabilityai/stable-diffusion-3-medium](https://huggingface.co/stabilityai/stable-diffusion-3-medium)

### FLUX.1 (versión "schnell")
- **Descripción:** Un modelo más reciente de Black Forest Labs que destaca por entender las instrucciones con gran precisión y generar texto dentro de las imágenes de forma correcta.
- **Licencia:** [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0) (Permite uso comercial).
- **Ideal para:** Imágenes que requieren alta fidelidad al texto o que incluyen tipografía.
- **Recursos Oficiales:**
  - **Hugging Face:** [https://huggingface.co/black-forest-labs/FLUX.1-schnell](https://huggingface.co/black-forest-labs/FLUX.1-schnell)

---

## 3. Modelos de Lenguaje (LLM)

### Llama 3
- **Descripción:** Uno de los modelos más potentes de Meta, compitiendo directamente con los mejores modelos privados. Es excelente para conversar, razonar, programar y seguir instrucciones complejas.
- **Licencia:** [Llama 3 License](https://github.com/meta-llama/llama3/blob/main/LICENSE) (Permite uso comercial, con algunas condiciones).
- **Ideal para:** La función principal de chat, asistencia en programación y generación de texto creativo.
- **Recursos Oficiales:**
  - **GitHub:** [https://github.com/meta-llama/llama3](https://github.com/meta-llama/llama3)
  - **Hugging Face:** [https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct](https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct)

---

## 4. Generación de Música

### Riffusion
- **Descripción:** Un modelo que genera música a partir de texto visualizando el sonido como espectrogramas. Es muy creativo y ofrece un gran control sobre el resultado.
- **Licencia:** [MIT License](https://github.com/riffusion/riffusion/blob/main/LICENSE) (Permite uso comercial **si se ejecuta en servidores propios**).
- **Ideal para:** Crear bandas sonoras, efectos de sonido y música original.
- **Recursos Oficiales:**
  - **GitHub:** [https://github.com/riffusion/riffusion](https://github.com/riffusion/riffusion)
  - **Hugging Face:** [https://huggingface.co/riffusion/riffusion-model-v1](https://huggingface.co/riffusion/riffusion-model-v1)

---

## 5. Edición de Imágenes y Eliminación de Fondo

### withoutBG
- **Descripción:** Un modelo especializado y muy preciso diseñado exclusivamente para quitar el fondo de las imágenes de forma limpia y rápida.
- **Licencia:** [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0) (Permite uso comercial).
- **Ideal para:** La función específica de eliminar fondos de imágenes.
- **Recursos Oficiales:**
  - **GitHub:** [https://github.com/withoutbg/withoutbg](https://github.com/withoutbg/withoutbg)

### Stable Diffusion (para Edición)
- **Descripción:** Además de generar imágenes, Stable Diffusion es excelente para editar. Con técnicas como **"inpainting"** (rellenar partes de una imagen) y **"outpainting"** (expandir una imagen), puedes hacer ediciones complejas.
- **Ideal para:** Añadir, quitar o modificar objetos en una imagen, cambiar estilos y mucho más.
- **Recursos:** Los mismos que en la sección de Generación de Imágenes.
