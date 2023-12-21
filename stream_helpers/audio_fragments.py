from pydub import AudioSegment
import base64
from io import BytesIO

def init_audio(video_file):
    audio = AudioSegment.from_file(video_file)
    return audio

def next_audio_fragment(audio, i):
    fragment_length = 1000
    fragment = audio[i:i+fragment_length]
    exported_io = BytesIO()
    fragment.export(exported_io, format="wav")
    base64_audio = base64.b64encode(exported_io.getvalue()).decode()
    
    return base64_audio
