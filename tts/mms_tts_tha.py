import scipy
import sys
import os
from .tts_interface import TTSInterface

from transformers import VitsModel, AutoTokenizer
import torch
import numpy as np

device = "cuda" if torch.cuda.is_available() else "cpu"

tokenizer = AutoTokenizer.from_pretrained("facebook/mms-tts-tha")

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

class TTSEngine(TTSInterface):

    def __init__(self, voice="en-US-AvaMultilingualNeural"):
        self.voice = voice

        self.temp_audio_file = "temp"
        self.file_extension = "wav"
        self.new_audio_dir = "cache"


        self.model = VitsModel.from_pretrained("facebook/mms-tts-tha")

        if not os.path.exists(self.new_audio_dir):
            os.makedirs(self.new_audio_dir)

    def generate_audio(self, text, file_name_no_ext=None):
        """
        Generate speech audio file using TTS.
        text: str
            the text to speak
        file_name_no_ext: str
            name of the file without extension


        Returns:
        str: the path to the generated audio file

        """
        file_name = self.generate_cache_file_name(file_name_no_ext, self.file_extension)

        try:
            inputs = tokenizer(text, return_tensors="pt")
            with torch.no_grad():
                output = self.model(**inputs).waveform

                output_np = output.cpu().numpy().squeeze()            

                sample_rate = 25000
                scipy.io.wavfile.write(file_name, rate=sample_rate, data=output_np)

        except Exception as e:
            print(f"\nError: mms_tts_tha unable to generate audio: {e}")
            print("It's possible that mms_tts_tha is blocked in your region.")
            return None

        return file_name
