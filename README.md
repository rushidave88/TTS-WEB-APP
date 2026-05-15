
# 🎙️ Coqui XTTS-v2 FastAPI Web App

A modern, fast, and multilingual Text-to-Speech (TTS) web application built from scratch. It uses a **FastAPI** backend, a vanilla **HTML/CSS/JS** frontend, and integrates **Coqui XTTS-v2** for high-quality, zero-shot voice cloning and speech generation.

## 📂 Project Folder Structure

Ensure your project directory looks exactly like this:

```text
TTS-WEB-APP/
├── app/
│   ├── __init__.py         # Empty file to mark directory as a module
│   ├── cleanup.py          # Background task to delete old audio files
│   ├── main.py             # FastAPI application and routing
│   └── tts_service.py      # Coqui TTS logic and generation
├── audio/                  # Generated .wav files will be saved here automatically
├── static/                 
│   ├── index.html          # Frontend UI
│   ├── script.js           # Frontend logic and API calls
│   └── style.css           # Modern styling
├── venv/                   # Python virtual environment
├── default_speaker.wav     # (CRITICAL) 3-5 second sample voice file for cloning
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation

```

## ⚙️ Prerequisites & Setup

To deploy or test this application on a new machine, the following setup is required.

### Prerequisites:

* Python **3.9, 3.10, or 3.11** installed.
* **Audio Reference Sample (Required):** You must place a file named `default_speaker.wav` in the root directory (A sample voice audio to train model for TTS).
* **Duration:** 3 to 5 seconds.
* **Quality:** Clean audio with a single speaker and no background noise.
* **Impact:** The AI will clone this specific voice. For best results in a specific language (like Hindi), use a native speaker sample.



### Installation Steps:

**1. Initialize Virtual Environment:**

```bash
python -m venv venv
venv\Scripts\activate

```

**2. Install Dependencies:**
All dependencies, including the specific CUDA-enabled GPU versions of PyTorch, are locked in the `requirements.txt` file.

```bash
pip install -r requirements.txt

```

**3. First-Time Model Initialization:**
Upon the first execution, the backend will automatically download the ~1.87 GB XTTS-v2 model weights.

## 🚀 How to Run the Application

**1. Start the Server:**
Execute the following command in the terminal:

```bash
uvicorn app.main:app --reload

```

**2. Access the Interfaces:**

* **Web User Interface:** `http://localhost:8000`
* **Swagger API Documentation:** `http://localhost:8000/docs`

## ✨ Application Workflow & Features

* **Zero-Shot Voice Cloning:** When a user clicks "Generate," the AI analyzes the acoustic properties of `default_speaker.wav` and uses those characteristics to synthesize the inputted text in the selected language.
* **Dynamic Language Loading:** On load, the frontend queries the backend to determine supported languages and populates the UI dropdown.
* **Non-Blocking Architecture:** Audio generation is offloaded to an asynchronous background thread (`asyncio.to_thread`) to keep the server responsive.
* **Automated Storage Management:** A background worker (`cleanup.py`) runs every 5 minutes to delete generated files older than 10 minutes.

