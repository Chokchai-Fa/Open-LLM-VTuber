import sys
import os
from pathlib import Path
import scipy
from .tts_interface import TTSInterface
import torch
import re

from transformers import AutoProcessor, SeamlessM4TModel, SeamlessM4Tv2Model
import torchaudio
import torch
import scipy


# from transformers import AutoModel, AutoProcessor

# from pythaitts import TTS

# processor = AutoProcessor.from_pretrained("wannaphong/seamless-tts-v1.0")
# model = AutoModel.from_pretrained("wannaphong/seamless-tts-v1.0")

device = "cuda" if torch.cuda.is_available() else "cpu"


current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)


# Check out doc at https://github.com/rany2/seamless-tts
# Use `seamless-tts --list-voices` to list all available voices


class TTSEngine(TTSInterface):

    def __init__(self, voice="en-US-AvaMultilingualNeural"):
        self.voice = voice

        self.temp_audio_file = "temp"
        self.file_extension = "wav"
        self.new_audio_dir = "cache"

        self.processor = AutoProcessor.from_pretrained("facebook/seamless-m4t-v2-large")
        self.model = SeamlessM4Tv2Model.from_pretrained("facebook/seamless-m4t-v2-large").to(device)       


        # facebook/hf-seamless-m4t-v2-medium
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
            text_inputs = self.processor(text = text, src_lang="tha", return_tensors="pt").to(device)
            audio_array_from_text = self.model.generate(
                **text_inputs,
                tgt_lang="tha",
                speaker_id=7,
                # spkr_id =7,
                num_beams=4,
                speech_do_sample=True,
                speech_temperature=0.6
            )[0].cpu().numpy().squeeze()

            # sample_rate = model.config.sampling_rate
            sample_rate = 18000
            scipy.io.wavfile.write(file_name, rate=sample_rate, data=audio_array_from_text)
            

        except Exception as e:
            print(f"\nError: seamless-tts unable to generate audio: {e}")
            print("It's possible that seamless-tts is blocked in your region.")
            return None


        # try:
        #     communicate = seamless_tts.Communicate(text, self.voice)
        #     communicate.save_sync(file_name)
        # except Exception as e:
        #     print(f"\nError: seamless-tts unable to generate audio: {e}")
        #     print("It's possible that seamless-tts is blocked in your region.")
        #     return None

        return file_name


# en-US-AvaMultilingualNeural
# en-US-EmmaMultilingualNeural
# en-US-JennyNeural
