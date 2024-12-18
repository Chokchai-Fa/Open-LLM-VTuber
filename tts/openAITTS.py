import sys
import os
# import edge_tts
# from pathlib import Path
from openai import OpenAI
from .tts_interface import TTSInterface
import librosa
import soundfile as sf
from pydub import AudioSegment


current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)


# Check out doc at https://github.com/rany2/edge-tts
# Use `edge-tts --list-voices` to list all available voices


class TTSEngine(TTSInterface):

    def __init__(self, voice="en-US-AvaMultilingualNeural"):
        self.voice = voice

        self.temp_audio_file = "temp"
        self.file_extension = "mp3"
        self.new_audio_dir = "cache"


        self.client = OpenAI()

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
            # text = th_tokenizer(text)
            response = self.client.audio.speech.create(
                model="tts-1",
                voice="nova",
                input=text,
            )


            response.stream_to_file(file_name)

            # # Load the audio file
            # y, sr = librosa.load(file_name, sr=16000)  # y is a numpy array, sr is the sample rate

            # # Apply pitch shift
            # y_shifted = librosa.effects.pitch_shift(y=y, sr=sr, n_steps=2)  # Shifted by 4 half steps

            # # Save back to the same file
            # sf.write(file_name, y_shifted, sr)


            audio = AudioSegment.from_file(file_name)
    
            # Calculate the speed change factor
            factor = 2 ** (8 / 12.0)  # n_steps = 3 is the number of semitones 
            
            # Apply the speed change
            shifted_audio = audio._spawn(audio.raw_data, overrides={
                "frame_rate": int(audio.frame_rate * factor)
            }).set_frame_rate(audio.frame_rate)  # Preserve the original frame rate
            
            # Save the shifted audio
            shifted_audio.export(file_name, format="mp3")

            # communicate = edge_tts.Communicate(text, self.voice, pitch="+200Hz")
            # communicate.save_sync(file_name)
        except Exception as e:
            print(f"\nError: edge-tts unable to generate audio: {e}")
            print("It's possible that edge-tts is blocked in your region.")
            return None

        return file_name


# en-US-AvaMultilingualNeural
# en-US-EmmaMultilingualNeural
# en-US-JennyNeural
