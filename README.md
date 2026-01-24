# Carl - Un Modelo de Lenguaje Transformer desde Cero

Este repositorio documenta el viaje de construir **Carl**, un modelo de lenguaje basado en la arquitectura Transformer, completamente desde cero.

## Visión del Proyecto

El objetivo principal de este proyecto no es competir con los modelos de última generación, sino **aprender en profundidad los fundamentos de las redes neuronales y el aprendizaje profundo**. Al construir cada componente desde la base, desde las operaciones con matrices hasta la capa de atención, obtenemos una comprensión que ningún framework de alto nivel puede ofrecer.

Nuestro objetivo final es tener un modelo funcional, llamado Carl, capaz de generar texto, construido sobre nuestra propia biblioteca de redes neuronales.

## Filosofía Principal

- **Desde los Primeros Principios:** No usaremos bibliotecas de alto nivel como TensorFlow o PyTorch para el núcleo del modelo. Cada operación matemática, cada estructura de datos y cada algoritmo de entrenamiento se implementará manualmente.
- **Rendimiento y Control:** El núcleo de la biblioteca está escrito en **C** para obtener un control total sobre la gestión de la memoria y el rendimiento computacional.
- **Facilidad de Uso:** Una interfaz en **Python** actúa como un *wrapper* sobre el núcleo de C, proporcionando una API amigable y sencilla para construir, entrenar y utilizar los modelos.

## Arquitectura Tecnológica

El proyecto se divide en dos componentes principales:

1.  **`carl_core` (El Núcleo en C):**
    - Contiene toda la lógica de bajo nivel.
    - Implementa estructuras de datos para matrices (`Matrix`) y redes neuronales (`NeuralNetwork`, `Layer`).
    - Contiene las funciones matemáticas para operaciones como la multiplicación de matrices, la adición de sesgos y las funciones de activación.
    - Se compila como una biblioteca compartida (`.so`) para que pueda ser utilizada por otros lenguajes.

2.  **`python_interface` (La Interfaz de Python):**
    - Utiliza la biblioteca `ctypes` de Python para cargar y comunicarse con la biblioteca C.
    - Proporciona clases de Python (`NeuralNetwork`, `Matrix`) que encapsulan la complejidad del manejo de punteros y la memoria de C.
    - Ofrece una API limpia y "pythónica" para interactuar con el núcleo del modelo.

## Progreso Actual

**Hito 1: La Base de la Red Neuronal - ¡Completado!**

Hemos construido con éxito la base fundamental de nuestra biblioteca:

- ✅ **Operaciones de Matriz en C:** Creación, destrucción, copia y multiplicación de matrices.
- ✅ **Estructura de Red Neuronal Prealimentada (Feed-Forward):** Definición de capas y de la red en C.
- ✅ **Propagación Hacia Adelante (Forward Propagation):** Implementación del algoritmo que procesa una entrada a través de la red para producir una salida.
- ✅ **Wrapper de Python:** Una interfaz funcional que permite controlar el núcleo de C desde Python.
- ✅ **Prueba de Integración:** Un script de prueba (`run_xor.py`) que demuestra que todo el sistema funciona de un extremo a otro.

## Hoja de Ruta (Roadmap)

Nuestro próximo objetivo es hacer que nuestra red pueda aprender. A partir de ahí, construiremos los bloques necesarios para llegar a la arquitectura Transformer.

-   **Hito 2: Aprendizaje (Retropropagación)**
    -   [ ] Implementar la derivada de la función de activación (Sigmoide).
    -   [ ] Implementar el algoritmo de **retropropagación (Backpropagation)** en C para calcular los gradientes.
    -   [ ] Implementar la **actualización de pesos y sesgos** (descenso de gradiente) en C.
    -   [ ] Crear un bucle de entrenamiento en Python para entrenar la red para resolver el problema XOR.

-   **Hito 3: Hacia un Transformer**
    -   [ ] Implementar más funciones de activación (ej. ReLU, Softmax).
    -   [ ] Implementar la capacidad de guardar y cargar modelos entrenados.
    -   [ ] Diseñar e implementar una capa de **Embedding** para procesar texto.
    -   [ ] Implementar la capa de **Atención (Attention)**, el corazón del Transformer.
    -   [ ] Ensamblar la arquitectura completa del Transformer (Encoder/Decoder).

## Cómo Compilar y Probar

1.  **Compilar el Núcleo de C:**
    Desde el directorio raíz, ejecuta `make`. Esto creará la biblioteca compartida en el directorio `lib/`.
    ```bash
    make
    ```

2.  **Ejecutar las Pruebas:**
    Para verificar que todo funciona correctamente, puedes ejecutar el conjunto de pruebas de integración.
    ```bash
    python3 -m unittest tests/test_integration.py
    ```

3.  **Ver el Ejemplo:**
    Para ver una demostración de la propagación hacia adelante, ejecuta el script `run_xor.py`.
    ```bash
    python3 run_xor.py
    ```
