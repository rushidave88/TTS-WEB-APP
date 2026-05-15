from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
import uuid, os, asyncio, base64, io
from pydub import AudioSegment

from .tts_service import TTSService
from .cleanup import delete_old_audio_files

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUDIO_DIR = os.path.join(BASE_DIR, "audio")
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
STATIC_DIR = os.path.join(BASE_DIR, "static")

os.makedirs(AUDIO_DIR, exist_ok=True)
os.makedirs(UPLOAD_DIR, exist_ok=True)

tts_service = TTSService()
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
app.mount("/audio", StaticFiles(directory=AUDIO_DIR), name="audio")

class TTSRequest(BaseModel):
    text: str
    language: str
    gender: str
    recorded_audio: Optional[str] = None

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(delete_old_audio_files(AUDIO_DIR, 10))
    asyncio.create_task(delete_old_audio_files(UPLOAD_DIR, 10))

@app.get("/")
def serve_frontend():
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))

@app.get("/languages")
async def get_languages():
    return tts_service.get_languages()

@app.post("/generate-tts")
async def generate_tts(request: TTSRequest):
    user_voice_path = None
    try:
        # Decode and Convert recorded voice if provided
        if request.gender == "user" and request.recorded_audio:
            audio_bytes = base64.b64decode(request.recorded_audio)
            user_voice_path = os.path.join(UPLOAD_DIR, f"ref_{uuid.uuid4().hex}.wav")
            
            # Export as standard WAV for XTTS
            audio = AudioSegment.from_file(io.BytesIO(audio_bytes))
            audio.export(user_voice_path, format="wav")

        filename = f"out_{uuid.uuid4().hex}.wav"
        output_path = os.path.join(AUDIO_DIR, filename)
        
        await asyncio.to_thread(
            tts_service.generate_audio, 
            request.text, request.language, request.gender, output_path, user_voice_path
        )
        
        return {"audio_url": f"/audio/{filename}"}
    except Exception as e:
        print(f"Server Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))