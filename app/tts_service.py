import os
from TTS.api import TTS
import torch

class TTSService:
    def __init__(self):
        # Setup device (GPU if available, otherwise CPU)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Loading XTTS-v2 on {self.device}...")
        
        # Initialize Coqui XTTS-v2
        self.model_name = "tts_models/multilingual/multi-dataset/xtts_v2"
        self.tts = TTS(model_name=self.model_name).to(self.device)
        
        # Point to the root directory for the speaker file
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.default_speaker = os.path.join(BASE_DIR, "default_speaker.wav")
        
        # Hardcoded supported languages for XTTS-v2 as fallback
        self.supported_languages = ["en", "es", "fr", "de", "it", "pt", "pl", "tr", "ru", "nl", "cs", "ar", "zh-cn", "hu", "ko", "ja", "hi"]

    def get_languages(self):
        if hasattr(self.tts, 'languages') and self.tts.languages:
            return self.tts.languages
        return self.supported_languages

    def generate_audio(self, text: str, language: str, output_path: str):
        if not os.path.exists(self.default_speaker):
            raise FileNotFoundError(f"Missing speaker reference file. Please place 'default_speaker.wav' in the root directory: {self.default_speaker}")
            
        self.tts.tts_to_file(
            text=text, 
            file_path=output_path, 
            speaker_wav=self.default_speaker, 
            language=language
        )
        return output_path