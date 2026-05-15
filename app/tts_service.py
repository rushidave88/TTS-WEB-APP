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
        
        # Full name mapping for XTTS-v2 supported languages
        self.language_map = {
            "en": "English",
            "hi": "Hindi",
            "es": "Spanish",
            "fr": "French",
            "de": "German",
            "it": "Italian",
            "pt": "Portuguese",
            "pl": "Polish",
            "tr": "Turkish",
            "ru": "Russian",
            "nl": "Dutch",
            "cs": "Czech",
            "ar": "Arabic",
            "zh-cn": "Chinese (Simplified)",
            "hu": "Hungarian",
            "ko": "Korean",
            "ja": "Japanese"
        }

    def get_languages(self):
        """Returns a dictionary of {code: Full Name} for the UI dropdown."""
        # Use model's internal list if available, otherwise fallback to our map
        try:
            model_codes = self.tts.languages if hasattr(self.tts, 'languages') else list(self.language_map.keys())
            # Return only the languages in our map that the model actually supports
            return {code: self.language_map.get(code, code.upper()) for code in model_codes}
        except Exception:
            return self.language_map

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