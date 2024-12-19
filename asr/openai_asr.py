import numpy as np
from .asr_interface import ASRInterface
import soundfile as sf
from openai import OpenAI
import os


class VoiceRecognition(ASRInterface):
    def __init__(self) -> None:
        self.client = OpenAI()

    def transcribe_np(self, audio: np.ndarray) -> str:
        temp_file = "voice.mp3"
        try:
            # Save the numpy array as an audio file
            sf.write(temp_file, audio, 16000)

            # Open the file in binary mode for the API call
            with open(temp_file, "rb") as audio_file:
                transcription = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file  # Pass the file object here
                )

            return transcription.text

        except Exception as e:
            print(f"Error during transcription: {e}")
            raise

        finally:
            # Ensure the temporary file is deleted
            if os.path.exists(temp_file):
                os.remove(temp_file)
                print("debug: temporary file removed")
