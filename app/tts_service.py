import os
from TTS.api import TTS
import torch

class TTSService:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Loading XTTS-v2 on {self.device}...")
        
        self.model_name = "tts_models/multilingual/multi-dataset/xtts_v2"
        self.tts = TTS(model_name=self.model_name).to(self.device)
        
        self.BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        self.language_map = {
            "en": "English", "hi": "Hindi", "es": "Spanish", "fr": "French",
            "de": "German", "it": "Italian", "pt": "Portuguese", "pl": "Polish",
            "tr": "Turkish", "ru": "Russian", "nl": "Dutch", "cs": "Czech",
            "ar": "Arabic", "zh-cn": "Chinese (Simplified)", "hu": "Hungarian",
            "ko": "Korean", "ja": "Japanese"
        }

    def get_languages(self):
        try:
            model_codes = self.tts.languages if hasattr(self.tts, 'languages') else list(self.language_map.keys())
            return {code: self.language_map.get(code, code.upper()) for code in model_codes}
        except Exception:
            return self.language_map

    def generate_audio(self, text: str, language: str, gender: str, output_path: str, user_voice_path: str = None):
        # Selection Logic
        if gender == "user" and user_voice_path:
            speaker_wav = user_voice_path
        elif gender == "female":
            speaker_wav = os.path.join(self.BASE_DIR, "female_speaker.wav")
        else:
            speaker_wav = os.path.join(self.BASE_DIR, "male_speaker.wav")

        if not os.path.exists(speaker_wav):
            raise FileNotFoundError(f"Speaker file not found: {speaker_wav}")
            
        self.tts.tts_to_file(
            text=text, 
            file_path=output_path, 
            speaker_wav=speaker_wav, 
            language=language
        )
        return output_path