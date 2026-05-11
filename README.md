# Whisper Transcripción y Diarización

Esta es una aplicación local con interfaz gráfica (Gradio) que utiliza [Faster-Whisper](https://github.com/SYSTRAN/faster-whisper) para la transcripción de audio y [SpeechBrain](https://speechbrain.github.io/) para la diarización de oradores (diferenciación de voces).

Se ejecuta de forma local utilizando Docker y no requiere conexión a servicios externos ni tokens de autenticación de HuggingFace.

## Características Principales

1.  **Diarización y Transcripción Opcional:** Puedes elegir si deseas realizar solo la transcripción rápida con Whisper o si también quieres identificar a los oradores (diarización).
2.  **Faster-Whisper:** Utiliza la implementación optimizada `faster-whisper` para mayor velocidad.
3.  **Diarización Local sin Tokens:** Utiliza el modelo `spkrec-ecapa-voxceleb` de SpeechBrain, que no requiere cuentas ni tokens de HuggingFace, ejecutándose 100% de manera local y privada.
4.  **Interfaz en Gradio:** Una interfaz web sencilla y fácil de usar.
5.  **Multilingüe:** La interfaz gráfica está disponible en Español, Catalán e Inglés.
6.  **Múltiples Formatos de Exportación:** Puedes descargar los resultados en los formatos `.txt`, `.srt` y `.vtt`.
7.  **Soporte CPU y GPU:** Posibilidad de elegir forzar la ejecución en CPU o aprovechar la aceleración CUDA de tu tarjeta gráfica NVIDIA.

---

## Requisitos Previos

*   [Docker](https://docs.docker.com/get-docker/) instalado en tu sistema.
*   (Opcional, pero recomendado) Tarjeta gráfica NVIDIA y [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html) instalado para soporte de GPU.

---

## Instalación y Ejecución con Docker

### 1. Construir la Imagen de Docker

Abre una terminal en el directorio principal del repositorio y ejecuta:

```bash
docker build -t whisper-diarization .
```

### 2. Ejecutar el Contenedor

#### Opción A: Ejecución en CPU (Para sistemas sin tarjeta gráfica NVIDIA)

Si no tienes una GPU compatible, o quieres forzar el uso del procesador (CPU), ejecuta:

```bash
docker run -p 7860:7860 whisper-diarization
```

#### Opción B: Ejecución con GPU (Recomendado)

Si tienes una tarjeta gráfica NVIDIA y has instalado el *NVIDIA Container Toolkit*, utiliza el flag `--gpus all` para un rendimiento mucho mayor:

```bash
docker run --gpus all -p 7860:7860 whisper-diarization
```

### 3. Acceder a la Interfaz

Una vez que el contenedor esté corriendo, abre tu navegador web y visita:

[http://localhost:7860](http://localhost:7860)

---

## Uso de la Interfaz

1.  **Idioma de la Interfaz:** Selecciona Español, Catalán o Inglés en la esquina superior izquierda.
2.  **Subir Audio/Vídeo:** Selecciona o arrastra el archivo multimedia que deseas procesar.
3.  **Tamaño del Modelo:** Elige el tamaño del modelo de Whisper (tiny, base, small, medium, large-v2, large-v3). Los modelos más grandes son más precisos pero más lentos y consumen más memoria RAM/VRAM.
4.  **Número de Oradores:**
    *   Deja en `0` para que el sistema detecte automáticamente la cantidad de oradores.
    *   Ingresa un número específico (ej. 2) si sabes exactamente cuántas personas están hablando.
5.  **Habilitar Diarización:** Marca esta casilla si deseas diferenciar quién está hablando. Si solo te interesa el texto (más rápido), desmárcala.
6.  **Ajustes Avanzados:**
    *   **Beam Size:** Ajusta el tamaño de la búsqueda (por defecto 5).
    *   **Tipo de Cómputo:** Puedes elegir el tipo de precisión (ej. `int8`, `float16`).
    *   **Dispositivo:** Por defecto está en `auto` (detectará si tienes GPU). Puedes forzar el uso de `cpu` o `cuda`.
7.  **Transcribir y Diarizar:** Pulsa el botón para iniciar el proceso.
8.  **Resultados y Descargas:** Al finalizar, verás el texto en la pantalla y podrás descargar los archivos generados (.txt, .srt, .vtt).
