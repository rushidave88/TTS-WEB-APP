from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import uuid
import os
import asyncio

# Relative imports since they are in the same 'app' folder
from .tts_service import TTSService
from .cleanup import delete_old_audio_files

app = FastAPI(title="Coqui TTS API")

# Define base directory (one level up from app/)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUDIO_DIR = os.path.join(BASE_DIR, "audio")
STATIC_DIR = os.path.join(BASE_DIR, "static")

# Ensure audio directory exists
os.makedirs(AUDIO_DIR, exist_ok=True)

# Initialize TTS Service
tts_service = TTSService()

# Mount directories using the absolute paths
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
app.mount("/audio", StaticFiles(directory=AUDIO_DIR), name="audio")

class TTSRequest(BaseModel):
    text: str
    language: str = "hi"

@app.on_event("startup")
async def startup_event():
    # Start background cleanup task
    asyncio.create_task(delete_old_audio_files(AUDIO_DIR, max_age_minutes=10))

@app.get("/")
def serve_frontend():
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))

@app.get("/languages")
async def get_languages():
    return tts_service.get_languages()

@app.post("/generate-tts")
async def generate_tts(request: TTSRequest):
    try:
        # Generate unique filename
        filename = f"output_{uuid.uuid4().hex}.wav"
        output_path = os.path.join(AUDIO_DIR, filename)
        
        # Generate audio synchronously in a background thread
        await asyncio.to_thread(
            tts_service.generate_audio, 
            request.text, 
            request.language, 
            output_path
        )
        
        return {"audio_url": f"/audio/{filename}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))