import librosa
import numpy as np
import pandas as pd
import soundfile as sf
from scipy.signal import butter, lfilter
import speech_recognition as sr
from pydub import AudioSegment

def trim_silence(y):
    y_trimmed, _ = librosa.effects.trim(y, top_db=20)
    print("Silence trimmed")
    return y_trimmed

def highpass_filter(y, sr, cutoff=300):
    b, a = butter(1, cutoff / (0.5 * sr), btype='high')
    filtered = lfilter(b, a, y)
    print("High-pass filter applied")
    return filtered

def filter_lecturer_segments(y, sr, energy_thresh=0.03):
    intervals = librosa.effects.split(y, top_db=20)
    segments = []
    for start, end in intervals:
        segment = y[start:end]
        energy = np.mean(librosa.feature.rms(y=segment)[0])
        if energy > energy_thresh:
            start_time = librosa.samples_to_time(start, sr=sr)
            end_time = librosa.samples_to_time(end, sr=sr)
            segments.append((segment, start_time, end_time))
    print(f"Filtered to {len(segments)} lecturer segments")
    return segments

def save_cleaned_audio(segments, sr, output_file="cleaned_output.wav", metadata_file="cleaned_metadata.csv"):
    combined = np.concatenate([seg for seg, _, _ in segments])
    sf.write(output_file, combined, sr)
    print(f"Cleaned audio saved as {output_file}")

    metadata = [{"file": output_file, "start": start, "end": end} for _, start, end in segments]
    df = pd.DataFrame(metadata)
    df.to_csv(metadata_file, index=False)
    print(f"Metadata saved as {metadata_file}")
    
    return output_file, metadata_file

def transcribe_audio(file_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio)
        print("Transcription successful")
        return text
    except sr.UnknownValueError:
        return "Could not understand audio"
    except sr.RequestError:
        return "API unavailable"

def process_uploaded_audio(file_path):
    y, sr = librosa.load(file_path, sr=None)
    y = trim_silence(y)
    y = highpass_filter(y, sr)
    segments = filter_lecturer_segments(y, sr)
    cleaned_path, metadata_path = save_cleaned_audio(segments, sr)
    transcript = transcribe_audio(cleaned_path)
    return cleaned_path, metadata_path, transcript

