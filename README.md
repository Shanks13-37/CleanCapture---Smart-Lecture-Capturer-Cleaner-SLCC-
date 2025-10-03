# CleanCapture---Smart-Lecture-Capturer-Cleaner-SLCC-

# Lecture Audio Cleaner and Segmenter

This project processes noisy classroom lecture recordings to:
- Detect speech vs silence
- Remove background chatter
- Segment lecturer's speech
- Output cleaned audio + timestamped segments
- (Optional) Transcribe speech to text

### Tools Used:
- `librosa` for audio analysis
- `numpy`, `scipy` for signal processing
- `pandas`, `json` for indexing
- `pydub`, `soundfile` for audio manipulation
- `SpeechRecognition` for transcription
