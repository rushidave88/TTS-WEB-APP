
# 🎙️ Coqui Voice Lab: AI TTS & Voice Cloning

A sophisticated, high-performance Text-to-Speech (TTS) web application. This project features a **FastAPI** backend and a vanilla **HTML/CSS/JS** frontend, utilizing **Coqui XTTS-v2** for high-quality, zero-shot voice cloning. Users can generate speech using presets or record their own voice in real-time to create an instant digital clone.

## 📂 Project Folder Structure

Ensure your project directory looks exactly like this for the application to function correctly:

```text
TTS-WEB-APP/
├── app/
│   ├── __init__.py         # Marks directory as a module
│   ├── cleanup.py          # Background worker to delete old audio/uploads
│   ├── main.py             # FastAPI routing and audio conversion logic
│   └── tts_service.py      # Coqui TTS engine and inference logic
├── audio/                  # Generated TTS .wav outputs (Auto-managed)
├── uploads/                # Temporary user recordings for cloning (Auto-managed)
├── static/                 
│   ├── index.html          # Modern, responsive UI
│   ├── script.js           # MediaRecorder logic and API interaction
│   └── style.css           # Professional styling
├── venv/                   # Python virtual environment
├── ffmpeg.exe              # (CRITICAL) Binary for audio conversion
├── ffprobe.exe             # (CRITICAL) Binary for audio analysis
├── male_speaker.wav        # Preset male voice sample
├── female_speaker.wav      # Preset female voice sample
├── default_speaker.wav     # Original default sample voice
├── requirements.txt        # Project dependencies
└── README.md               # Project documentation

```

## 🚀 Key Features

* **Real-Time Voice Cloning:** Record 3-5 seconds of audio directly in the browser to instantly clone your voice.
* **Intelligent UI Stop-Logic:** The audio player automatically stops, resets, and hides when switching between voice options to prevent audio overlap.
* **Multilingual Support:** Synthesize speech in over 16 languages (Hindi, English, Spanish, etc.) with a single click.
* **Automatic Audio Sanitization:** Uses **FFmpeg** and **Pydub** on the backend to convert browser-recorded WebM/Ogg files into 16-bit PCM WAV files required by the AI engine.
* **Automated Storage Management:** The `cleanup.py` worker runs every 10 minutes to purge both generated results and temporary user uploads.

## ⚙️ Setup & Installation

### Prerequisites:

* Python **3.9, 3.10, or 3.11**.
* **NVIDIA GPU (Recommended):** The app is configured for CUDA to ensure fast, real-time generation.
* **FFmpeg Binaries:** `ffmpeg.exe` and `ffprobe.exe` must be in the root folder to handle "Clone My Voice" recordings.

### Installation Steps:

**1. Initialize Virtual Environment:**

```bash
python -m venv venv
venv\Scripts\activate

```

**2. Install Dependencies:**

```bash
pip install -r requirements.txt

```

**3. Model Download:**
On the first run, the system will download the ~1.8GB XTTS-v2 model weights automatically.

## 🏃 How to Run the Application

**1. Start the Server:**

```bash
uvicorn app.main:app --reload

```

**2. Access the Application:**

* **Web Interface:** `http://localhost:8000`
* **API Docs (Swagger):** `http://localhost:8000/docs`

## 🎤 Cloning Your Voice

1. Select the **"Clone My Voice"** radio button.
2. Click **🎤 Start Recording** and speak clearly for 5 seconds.
3. Click **🛑 Stop**. The UI will confirm with "✅ Voice Captured!".
4. Type your text in the input area and click **Generate Speech**.
5. The backend will convert your recording using FFmpeg and use it as a reference for the TTS engine.

## 📄 Important Notes

* **Privacy:** Recorded voice samples are stored in the `uploads/` folder and are automatically deleted by the background cleanup task.
* **Audio Quality:** For best cloning results, ensure your recording environment is quiet and your microphone is clear.