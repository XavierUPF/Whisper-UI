TRANSLATIONS = {
    "es": {
        "title": "Transcripción y Diarización con Whisper",
        "description": "Sube un archivo de audio para transcribirlo y detectar diferentes oradores usando Faster-Whisper y SpeechBrain.",
        "audio_input": "Subir archivo de audio o video",
        "model_size": "Tamaño del modelo de Whisper",
        "num_speakers": "Número de oradores (0 = Auto)",
        "language_ui": "Idioma de la Interfaz",
        "transcribe_btn": "Transcribir y Diarizar",
        "transcription_output": "Resultado de la Transcripción",
        "download_txt": "Descargar TXT",
        "download_srt": "Descargar SRT",
        "download_vtt": "Descargar VTT",
        "beam_size": "Tamaño del Haz (Beam Size)",
        "compute_type": "Tipo de Cómputo",
        "status": "Estado:",
        "processing": "Procesando...",
        "done": "¡Completado!"
    },
    "ca": {
        "title": "Transcripció i Diarització amb Whisper",
        "description": "Puja un fitxer d'àudio per transcriure'l i detectar diferents locutors utilitzant Faster-Whisper i SpeechBrain.",
        "audio_input": "Pujar fitxer d'àudio o vídeo",
        "model_size": "Mida del model de Whisper",
        "num_speakers": "Nombre de locutors (0 = Auto)",
        "language_ui": "Idioma de la Interfície",
        "transcribe_btn": "Transcriure i Diaritzar",
        "transcription_output": "Resultat de la Transcripció",
        "download_txt": "Descarregar TXT",
        "download_srt": "Descarregar SRT",
        "download_vtt": "Descarregar VTT",
        "beam_size": "Mida del Feix (Beam Size)",
        "compute_type": "Tipus de Còmput",
        "status": "Estat:",
        "processing": "Processant...",
        "done": "Completat!"
    },
    "en": {
        "title": "Whisper Transcription & Diarization",
        "description": "Upload an audio file to transcribe and detect different speakers using Faster-Whisper and SpeechBrain.",
        "audio_input": "Upload audio or video file",
        "model_size": "Whisper Model Size",
        "num_speakers": "Number of Speakers (0 = Auto)",
        "language_ui": "UI Language",
        "transcribe_btn": "Transcribe & Diarize",
        "transcription_output": "Transcription Output",
        "download_txt": "Download TXT",
        "download_srt": "Download SRT",
        "download_vtt": "Download VTT",
        "beam_size": "Beam Size",
        "compute_type": "Compute Type",
        "status": "Status:",
        "processing": "Processing...",
        "done": "Done!"
    }
}

def get_text(lang_code, key):
    return TRANSLATIONS.get(lang_code, TRANSLATIONS["es"]).get(key, key)
