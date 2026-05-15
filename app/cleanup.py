import os
import time
import asyncio

async def delete_old_audio_files(directory: str, max_age_minutes: int = 10):
    """Background task to delete audio files older than specified minutes."""
    while True:
        try:
            current_time = time.time()
            if os.path.exists(directory):
                for filename in os.listdir(directory):
                    filepath = os.path.join(directory, filename)
                    if filepath.endswith(".wav"):
                        file_age = current_time - os.path.getmtime(filepath)
                        if file_age > (max_age_minutes * 60):
                            os.remove(filepath)
                            print(f"Cleaned up old file: {filepath}")
        except Exception as e:
            print(f"Cleanup error: {e}")
            
        # Run cleanup check every 5 minutes
        await asyncio.sleep(300)