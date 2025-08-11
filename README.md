# Carl - Una IA que Aprende Desde Cero

## 1. Objetivo del Proyecto

El objetivo de este proyecto es crear a **Carl**, una Inteligencia Artificial que no se basa en un vasto conocimiento preexistente (como modelos tipo GPT). En su lugar, Carl está diseñado para **aprender todo desde cero** a través de la interacción directa con el usuario.

La meta es simular un proceso de aprendizaje natural, permitiendo que Carl desarrolle su propia "base de conocimiento", "personalidad" y "gustos" a partir de las conversaciones que tenga. La inspiración para este enfoque proviene de la idea de una conciencia que se forma a través de la experiencia, como se explora en [este video](https://www.youtube.com/watch?v=u1a7GOJ1cY0).

## 2. Metodología y Arquitectura

Actualmente, Carl está en su primera versión (v0.1), implementado como un sencillo programa de consola en Python.

- **Cerebro y Lógica:** El núcleo de Carl es el script `carl.py`. No utilizamos ninguna librería de IA externa. La lógica se basa en un sistema de **reglas simples** que analizan el texto del usuario en busca de patrones.
- **Memoria:** Carl tiene una memoria persistente gracias al archivo `memoria.json`. Cuando Carl aprende algo nuevo (como su nombre), lo guarda en este archivo. Al reiniciar la conversación, Carl carga este archivo para recordar lo que ha aprendido.
- **Aprendizaje:** En esta fase inicial, el aprendizaje es explícito. Por ejemplo, para que aprenda su nombre, debes decírselo directamente con una frase como: `tu nombre es Carl`.

## 3. ¿Cómo Hablar con Carl?

Interactuar con la versión actual de Carl es muy sencillo.

1.  Abre una terminal (como la que viene integrada en Visual Studio Code).
2.  Asegúrate de estar en la carpeta raíz del proyecto.
3.  Ejecuta el siguiente comando:
    ```bash
    python carl.py
    ```
4.  ¡Listo! El programa se iniciará y podrás comenzar a chatear con Carl. Para terminar la conversación, simplemente escribe `adios`.

## 4. Visión a Futuro

Este es solo el primer paso de un proyecto muy ambicioso. La visión a largo plazo para Carl incluye:

- **Aprendizaje Implícito:** Que pueda deducir información sin que se la digan explícitamente.
- **Desarrollo de Gustos:** Exponer a Carl a diferentes estímulos (música, libros, etc.) para que pueda formar preferencias.
- **Comprensión Emocional:** Que pueda reconocer y reaccionar a las emociones expresadas por el usuario.
- **Entorno Virtual:** La meta final es darle a Carl un "cuerpo" en un entorno virtual donde pueda moverse, observar e interactuar con objetos de forma autónoma.

Este `README.md` evolucionará junto con Carl. ¡Gracias por ser parte de su desarrollo!
