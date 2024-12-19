import sys
import os
import scipy
from .tts_interface import TTSInterface
import torch

from gtts import gTTS
import torch
import scipy
from utils.th_tokenizer import th_tokenizer

device = "cuda" if torch.cuda.is_available() else "cpu"


current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)


# Check out doc at https://github.com/rany2/google-tts
# Use `google-tts --list-voices` to list all available voices


class TTSEngine(TTSInterface):

    def __init__(self, language):
        # self.voice = voice
        self.language = language
        self.temp_audio_file = "temp"
        self.file_extension = "mp3"
        self.new_audio_dir = "cache"

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

            if self.language == 'th':
                text = th_tokenizer(text)
                audio_obj = gTTS(text=text, lang=self.language, slow=False)
            else:
                audio_obj = gTTS(text=text, lang=self.language, slow=False)

            audio_obj.save(file_name)            

        except Exception as e:
            print(f"\nError: google-tts unable to generate audio: {e}")
            print("It's possible that google-tts is blocked in your region.")
            return None


        return file_name
    