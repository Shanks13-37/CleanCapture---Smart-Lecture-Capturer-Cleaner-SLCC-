from flask import Flask, render_template, request, send_file
from audio_processor import process_uploaded_audio
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/process", methods=["POST"])
def process():
    # Debug: show incoming keys
    print("Form keys:", list(request.form.keys()))
    print("File keys:", list(request.files.keys()))

    if "audio" not in request.files:
        return "⚠️ No audio file received", 400

    audio = request.files["audio"]
    audio_path = os.path.join(UPLOAD_FOLDER, audio.filename)
    audio.save(audio_path)

    cleaned_path, metadata_path, transcript = process_uploaded_audio(audio_path)

    return render_template("result.html",
        cleaned_audio=cleaned_path,
        metadata_file=metadata_path,
        transcript=transcript
    )

@app.route("/download/<path:filename>")
def download(filename):
    return send_file(filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
