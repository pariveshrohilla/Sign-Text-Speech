from flask import Flask, request, render_template_string, send_from_directory
import subprocess
from pathlib import Path
import os

app = Flask(__name__)

# ---------------- PATH SETUP ----------------

BASE_DIR = Path(__file__).resolve().parent      # sign text speech
ROOT_DIR = BASE_DIR.parent                      # project root

UPLOAD_FOLDER = BASE_DIR / "uploads"

STT_PROJECT_PATH = ROOT_DIR / "speech to text"
TTS_PROJECT_PATH = ROOT_DIR / "Text to speech"
SIGN_PROJECT_PATH = ROOT_DIR / "sign final"

os.makedirs(str(UPLOAD_FOLDER), exist_ok=True)

# Prevent multiple sign processes
sign_process = None

# ---------------- STT ----------------

def speech_to_text(file_path):
    result = subprocess.run(
        ["python", "main.py", str(file_path)],
        cwd=str(STT_PROJECT_PATH),
        capture_output=True,
        text=True
    )
    return result.stdout.strip()


# ---------------- TTS ----------------

def text_to_speech(text, lang):
    result = subprocess.run(
        ["python", "speech.py", text, lang],
        cwd=str(TTS_PROJECT_PATH),
        capture_output=True,
        text=True
    )

    lines = result.stdout.strip().split("\n")

    if len(lines) < 2:
        return "Error generating audio", ""

    filename = lines[0]
    output_text = lines[1]

    src = TTS_PROJECT_PATH / filename
    dst = UPLOAD_FOLDER / filename

    if src.exists():
        src.rename(dst)

    return output_text, filename


# ---------------- SIGN LANGUAGE ----------------

def run_sign_language():
    global sign_process

    if sign_process is None or sign_process.poll() is not None:
        sign_process = subprocess.Popen(
            ["python", "app.py"],
            cwd=str(SIGN_PROJECT_PATH)
        )


# ---------------- HOME ----------------

@app.route('/')
def home():
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>AI Multi Tool</title>
        <style>
            body {
                font-family: Arial;
                background: linear-gradient(135deg, #667eea, #764ba2);
                margin: 0;
            }
            .container {
                max-width: 800px;
                margin: 50px auto;
                background: white;
                padding: 30px;
                border-radius: 15px;
            }
            .card {
                background: #f4f4f4;
                padding: 20px;
                margin: 15px 0;
                border-radius: 10px;
            }
            input, select {
                width: 100%;
                padding: 10px;
                margin: 8px 0;
                border-radius: 8px;
            }
            input[type="submit"] {
                background: #667eea;
                color: white;
                border: none;
                cursor: pointer;
            }
        </style>
    </head>

    <body>
    <div class="container">
        <h2 style="text-align:center;">🚀 AI Multi Tool</h2>

        <div class="card">
            <h3>🎤 Speech to Text</h3>
            <form action="/stt" method="post" enctype="multipart/form-data">
                <input type="file" name="file" required>
                <input type="submit" value="Convert">
            </form>
        </div>

        <div class="card">
            <h3>🔊 Text to Speech</h3>
            <form action="/tts" method="post">
                <input type="text" name="text" placeholder="Enter text" required>

                <label>Language:</label>
                <select name="lang">
                    <option value="en">English 🇬🇧</option>
                    <option value="hi">Hindi 🇮🇳</option>
                </select>

                <input type="submit" value="Convert">
            </form>
        </div>

        <div class="card">
            <h3>🖐️ Sign Language</h3>
            <form action="/sign" method="post">
                <input type="submit" value="Start Sign Detection">
            </form>
        </div>

    </div>
    </body>
    </html>
    """)


# ---------------- STT ROUTE ----------------

@app.route('/stt', methods=['POST'])
def stt():
    file = request.files['file']

    path = UPLOAD_FOLDER / file.filename
    file.save(str(path))

    text = speech_to_text(path)

    return f"""
    <div style="font-family:Arial;padding:30px;">
        <h2>📝 Speech to Text Result</h2>

        <h3>🎤 Audio</h3>
        <audio controls>
            <source src="/uploads/{file.filename}">
        </audio>

        <h3>📄 Text Output</h3>
        <div style="background:#f4f4f4;padding:15px;border-radius:10px;">
            {text}
        </div>

        <br><a href="/">⬅ Back</a>
    </div>
    """


# ---------------- TTS ROUTE ----------------

@app.route('/tts', methods=['POST'])
def tts():
    text = request.form['text']
    lang = request.form['lang']

    output_text, filename = text_to_speech(text, lang)

    return render_template_string(f"""
    <html>
    <body style="font-family:Arial;text-align:center;padding:40px;">
        <h2>🔊 Result</h2>

        <p><b>Input:</b> {text}</p>
        <p><b>Output:</b> {output_text}</p>

        <audio controls autoplay>
            <source src="/uploads/{filename}">
        </audio>

        <br><br><a href="/">⬅ Back</a>
    </body>
    </html>
    """)


# ---------------- SIGN ROUTE ----------------

@app.route('/sign', methods=['POST'])
def sign():
    run_sign_language()

    return """
    <div style="font-family:Arial;padding:30px;text-align:center;">
        <h2>🖐️ Sign Language Started</h2>
        <p>Camera window should open now.</p>
        <br><a href="/">⬅ Back</a>
    </div>
    """


# ---------------- FILE SERVE ----------------

@app.route('/uploads/<filename>')
def uploads(filename):
    return send_from_directory(str(UPLOAD_FOLDER), filename)


# ---------------- RUN ----------------

if __name__ == "__main__":
    app.run(debug=True)