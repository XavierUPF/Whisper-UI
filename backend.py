import os
import torch
import numpy as np
from faster_whisper import WhisperModel
import torchaudio
from speechbrain.inference.speaker import EncoderClassifier
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import silhouette_score
import librosa

def transcribe_and_diarize(audio_path, model_size, num_speakers, beam_size, compute_type):
    # 1. Setup device for both Whisper and SpeechBrain
    device = "cuda" if torch.cuda.is_available() else "cpu"
    compute_type_actual = compute_type if device == "cuda" else "int8"
    
    # 2. Transcribe with faster-whisper
    print(f"Loading whisper model {model_size} on {device}...")
    model = WhisperModel(model_size, device=device, compute_type=compute_type_actual)
    
    print("Transcribing...")
    segments, info = model.transcribe(audio_path, beam_size=beam_size, vad_filter=True)
    
    # Collect segments: (start, end, text)
    transcript_segments = []
    for segment in segments:
        transcript_segments.append({
            "start": segment.start,
            "end": segment.end,
            "text": segment.text.strip()
        })
    
    if not transcript_segments:
        return []

    # 3. Load audio for diarization
    print("Loading audio for diarization...")
    signal, fs = torchaudio.load(audio_path)
    
    # Resample to 16000Hz (required by SpeechBrain)
    if fs != 16000:
        resampler = torchaudio.transforms.Resample(orig_freq=fs, new_freq=16000)
        signal = resampler(signal)
        fs = 16000
        
    # Convert stereo to mono if necessary
    if signal.shape[0] > 1:
        signal = signal.mean(dim=0, keepdim=True)

    # 4. Load SpeechBrain Speaker Recognition Model
    print("Loading SpeechBrain model...")
    # This model runs locally and does not require HuggingFace tokens
    classifier = EncoderClassifier.from_hparams(
        source="speechbrain/spkrec-ecapa-voxceleb",
        run_opts={"device": device},
        savedir="tmp_speechbrain"
    )

    # 5. Extract embeddings for each transcription segment
    print("Extracting embeddings for segments...")
    embeddings = []
    valid_segments = []
    
    for seg in transcript_segments:
        start_sample = int(seg["start"] * fs)
        end_sample = int(seg["end"] * fs)
        
        # Make sure segment length is valid
        if end_sample <= start_sample:
            continue
            
        # Ensure we don't go out of bounds
        end_sample = min(end_sample, signal.shape[1])
        
        audio_segment = signal[:, start_sample:end_sample]
        
        # Pad if too short (minimum 0.1s)
        if audio_segment.shape[1] < 1600:
            padding = 1600 - audio_segment.shape[1]
            audio_segment = torch.nn.functional.pad(audio_segment, (0, padding))
            
        with torch.no_grad():
            embedding = classifier.encode_batch(audio_segment)
            # Flatten to 1D
            embedding = embedding.squeeze().cpu().numpy()
            embeddings.append(embedding)
            valid_segments.append(seg)
            
    if not valid_segments:
        return []

    embeddings = np.array(embeddings)
    
    # 6. Cluster embeddings to find speakers
    print("Clustering speakers...")
    if num_speakers == 0:
        # Auto-detect number of speakers using silhouette score
        best_num = 1
        best_score = -1
        max_speakers = min(10, len(embeddings) - 1)
        
        if max_speakers > 1:
            for k in range(2, max_speakers + 1):
                clustering = AgglomerativeClustering(n_clusters=k, metric='cosine', linkage='average')
                labels = clustering.fit_predict(embeddings)
                score = silhouette_score(embeddings, labels, metric='cosine')
                if score > best_score:
                    best_score = score
                    best_num = k
                    best_labels = labels
            
            if best_score < 0.05:
                # If silhouette score is very low, assume just 1 speaker
                final_labels = np.zeros(len(embeddings), dtype=int)
            else:
                final_labels = best_labels
        else:
            final_labels = np.zeros(len(embeddings), dtype=int)
    else:
        # Use specified number of speakers
        n_clusters = min(num_speakers, len(embeddings))
        if n_clusters > 1:
            clustering = AgglomerativeClustering(n_clusters=n_clusters, metric='cosine', linkage='average')
            final_labels = clustering.fit_predict(embeddings)
        else:
            final_labels = np.zeros(len(embeddings), dtype=int)

    # 7. Map labels back to segments
    results = []
    for seg, label in zip(valid_segments, final_labels):
        results.append({
            "start": seg["start"],
            "end": seg["end"],
            "speaker": f"Speaker {label + 1}",
            "text": seg["text"]
        })

    print("Diarization complete!")
    return results
