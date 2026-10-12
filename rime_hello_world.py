import json
import os
import urllib.request
import io
import wave
import pyaudio
from dotenv import load_dotenv

load_dotenv() 

def TTS_agent(text_to_speak):
    RIME_API_KEY = os.environ["RIME_API_KEY"]

    headers = {
        "Accept": "audio/wav",
        "Authorization": f"Bearer {RIME_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "text": text_to_speak,
        "speaker": "celeste",
        "modelId": "coda"
    }

    data = json.dumps(payload).encode("utf-8")

    request = urllib.request.Request(
        "https://users.rime.ai/v1/rime-tts",
        data=data,
        headers=headers,
        method="POST"
    )

    print("\n🔊 Rime is speaking...")
    
    # Read the audio data directly into memory
    with urllib.request.urlopen(request) as response:
        audio_bytes = response.read() 

    # Play the audio stream directly from memory using PyAudio
    with wave.open(io.BytesIO(audio_bytes), 'rb') as wf:
        p = pyaudio.PyAudio()
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)
        
        chunk_size = 1024
        data = wf.readframes(chunk_size)
        
        while data:
            stream.write(data)
            data = wf.readframes(chunk_size)
            
        stream.stop_stream()
        stream.close()
        p.terminate()