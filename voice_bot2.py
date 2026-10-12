import os
import io
import collections
import pyaudio
import wave
import webrtcvad
from dotenv import load_dotenv  
from groq import Groq
from rime_hello_world import TTS_agent

# Load environment variables from your .env file
load_dotenv() 

# Initialize Groq client
client = Groq()

# Audio recording configuration
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000  
FRAME_DURATION = 30  
CHUNK = int(RATE * FRAME_DURATION / 1000)

# VAD sensitivity (0: aggressive, 3: highly sensitive to silence)
vad = webrtcvad.Vad(2) 

# 📦 This variable will accumulate your entire conversation
FULL_TRANSCRIPT = ""

def transcribe_chunk(audio_bytes):
    """Sends recorded speech bytes to Groq for near-instant transcription."""
    try:
        wav_buffer = io.BytesIO()
        with wave.open(wav_buffer, 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(pyaudio.PyAudio().get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(audio_bytes)
        wav_buffer.seek(0)
        
        transcription = client.audio.transcriptions.create(
            file=("live_chunk.wav", wav_buffer.read()),
            model="whisper-large-v3",
            response_format="text",
            language="en"
        )
        return transcription.strip()
    except Exception as e:
        return f"[Error: {e}]"

def main():
    global FULL_TRANSCRIPT # Reference our accumulator variable
    
    pa = pyaudio.PyAudio()
    stream = pa.open(format=FORMAT, channels=CHANNELS, rate=RATE, 
                     input=True, frames_per_buffer=CHUNK)
    
    print("🎙️  Listening... Speak into your microphone. Press Ctrl+C when finished.")
    
    is_speaking = False
    voiced_frames = []
    ring_buffer = collections.deque(maxlen=10) 
    triggered_silence_frames = 0
    
    try:
        while True:
            frame = stream.read(CHUNK, exception_on_overflow=False)
            is_speech = vad.is_speech(frame, RATE)
            
            if not is_speaking:
                if is_speech:
                    is_speaking = True
                    print(".", end="", flush=True) # Tiny visual cue that it heard you speak
                    voiced_frames.extend(ring_buffer)
                    voiced_frames.append(frame)
                else:
                    ring_buffer.append(frame)
            else:
                voiced_frames.append(frame)
                
                if not is_speech:
                    triggered_silence_frames += 1
                else:
                    triggered_silence_frames = 0
                
                # If user is silent for ~600ms, process the chunk
                if triggered_silence_frames > 20:
                    print("⚙️", end="", flush=True) # Tiny visual cue that Groq is transcribing
                    
                    audio_to_send = b"".join(voiced_frames)
                    text = transcribe_chunk(audio_to_send)
                    
                    # Accumulate text into our global variable if transcription is valid
                    if text and not text.startswith("Error"):
                        FULL_TRANSCRIPT += text + " "
                    
                    # Reset variables for the next phrase
                    is_speaking = False
                    voiced_frames = []
                    triggered_silence_frames = 0
                    ring_buffer.clear()
                    
    except KeyboardInterrupt:
        # 🧾 This block runs the moment you hit Ctrl+C
        print("\n\n🛑 Stopping live transcription...")
        print("\n================ FULL TRANSCRIPT ================")
        if FULL_TRANSCRIPT.strip():
            print(FULL_TRANSCRIPT.strip())
            TTS_agent(FULL_TRANSCRIPT)
        else:
            print("[No speech recorded]")
        print("=================================================\n")
        
    finally:
        stream.stop_stream()
        stream.close()
        pa.terminate()

if __name__ == "__main__":
    main()