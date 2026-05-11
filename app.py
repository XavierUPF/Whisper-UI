import os
import gradio as gr
from backend import transcribe_and_diarize
from i18n import get_text
import tempfile

def format_timestamp(seconds, format_type="srt"):
    """Format seconds into SRT or VTT timestamp format."""
    hours = int(seconds / 3600)
    minutes = int((seconds % 3600) / 60)
    secs = int(seconds % 60)
    ms = int((seconds - int(seconds)) * 1000)
    
    if format_type == "vtt":
        return f"{hours:02d}:{minutes:02d}:{secs:02d}.{ms:03d}"
    else: # srt
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{ms:03d}"

def generate_export_files(results):
    """Generate TXT, SRT, and VTT files from results."""
    # Create temp files
    txt_fd, txt_path = tempfile.mkstemp(suffix=".txt")
    srt_fd, srt_path = tempfile.mkstemp(suffix=".srt")
    vtt_fd, vtt_path = tempfile.mkstemp(suffix=".vtt")
    
    with os.fdopen(txt_fd, 'w', encoding='utf-8') as txt_f, \
         os.fdopen(srt_fd, 'w', encoding='utf-8') as srt_f, \
         os.fdopen(vtt_fd, 'w', encoding='utf-8') as vtt_f:
         
        vtt_f.write("WEBVTT\n\n")
        
        for i, segment in enumerate(results, start=1):
            start = segment["start"]
            end = segment["end"]
            speaker = segment["speaker"]
            text = segment["text"]
            
            # TXT format: [00:00.00] Speaker X: Text
            txt_f.write(f"[{format_timestamp(start, 'vtt')[:9]}] {speaker}: {text}\n")
            
            # SRT format
            srt_f.write(f"{i}\n")
            srt_f.write(f"{format_timestamp(start, 'srt')} --> {format_timestamp(end, 'srt')}\n")
            srt_f.write(f"{speaker}: {text}\n\n")
            
            # VTT format
            vtt_f.write(f"{format_timestamp(start, 'vtt')} --> {format_timestamp(end, 'vtt')}\n")
            vtt_f.write(f"<v {speaker}>{text}</v>\n\n")
            
    return txt_path, srt_path, vtt_path

def process_audio(audio_path, model_size, num_speakers, beam_size, compute_type, lang_code):
    if not audio_path:
        return "No audio file provided.", None, None, None
        
    try:
        results = transcribe_and_diarize(
            audio_path=audio_path,
            model_size=model_size,
            num_speakers=int(num_speakers),
            beam_size=int(beam_size),
            compute_type=compute_type
        )
        
        if not results:
            return "No speech detected.", None, None, None
            
        # Format display text
        display_text = ""
        for seg in results:
            start_str = format_timestamp(seg["start"], "vtt")[:9]
            display_text += f"[{start_str}] {seg['speaker']}: {seg['text']}\n"
            
        # Generate export files
        txt_path, srt_path, vtt_path = generate_export_files(results)
        
        return display_text, txt_path, srt_path, vtt_path
        
    except Exception as e:
        return f"Error: {str(e)}", None, None, None

def update_ui(lang_code):
    return (
        gr.update(value=get_text(lang_code, "title")),
        gr.update(value=get_text(lang_code, "description")),
        gr.update(label=get_text(lang_code, "audio_input")),
        gr.update(label=get_text(lang_code, "model_size")),
        gr.update(label=get_text(lang_code, "num_speakers")),
        gr.update(label=get_text(lang_code, "beam_size")),
        gr.update(label=get_text(lang_code, "compute_type")),
        gr.update(label=get_text(lang_code, "language_ui")),
        gr.update(value=get_text(lang_code, "transcribe_btn")),
        gr.update(label=get_text(lang_code, "transcription_output")),
        gr.update(label=get_text(lang_code, "download_txt")),
        gr.update(label=get_text(lang_code, "download_srt")),
        gr.update(label=get_text(lang_code, "download_vtt"))
    )

with gr.Blocks(title="Whisper Diarization") as app:
    # We use gr.State to keep track of the current language, defaults to 'es'
    current_lang = gr.State("es")
    
    title = gr.Markdown(f"# {get_text('es', 'title')}")
    description = gr.Markdown(get_text('es', 'description'))
    
    with gr.Row():
        with gr.Column(scale=1):
            lang_selector = gr.Dropdown(
                choices=[("Español", "es"), ("Català", "ca"), ("English", "en")],
                value="es",
                label=get_text('es', 'language_ui')
            )
            
            audio_in = gr.Audio(type="filepath", label=get_text('es', 'audio_input'))
            
            model_size = gr.Dropdown(
                choices=["tiny", "base", "small", "medium", "large-v2", "large-v3"],
                value="small",
                label=get_text('es', 'model_size')
            )
            
            num_speakers = gr.Number(
                value=0,
                label=get_text('es', 'num_speakers'),
                precision=0
            )
            
            with gr.Accordion("Advanced Settings", open=False):
                beam_size = gr.Slider(minimum=1, maximum=10, step=1, value=5, label=get_text('es', 'beam_size'))
                compute_type = gr.Dropdown(
                    choices=["default", "float16", "int8_float16", "int8"],
                    value="default",
                    label=get_text('es', 'compute_type')
                )
                
            transcribe_btn = gr.Button(get_text('es', 'transcribe_btn'), variant="primary")
            
        with gr.Column(scale=2):
            output_text = gr.Textbox(label=get_text('es', 'transcription_output'), lines=15)
            with gr.Row():
                out_txt = gr.File(label=get_text('es', 'download_txt'))
                out_srt = gr.File(label=get_text('es', 'download_srt'))
                out_vtt = gr.File(label=get_text('es', 'download_vtt'))

    # Handle language change
    lang_selector.change(
        fn=update_ui,
        inputs=[lang_selector],
        outputs=[
            title, description, audio_in, model_size, num_speakers, 
            beam_size, compute_type, lang_selector, transcribe_btn, 
            output_text, out_txt, out_srt, out_vtt
        ]
    )

    # Handle transcription
    transcribe_btn.click(
        fn=process_audio,
        inputs=[audio_in, model_size, num_speakers, beam_size, compute_type, lang_selector],
        outputs=[output_text, out_txt, out_srt, out_vtt]
    )

if __name__ == "__main__":
    app.launch(server_name="0.0.0.0", server_port=7860, share=False)
