# Real-Time Speech-to-Speech Agent

This project is a real-time, bidirectional voice processing pipeline built in Python. It acts as an echo and transcription agent: it listens to your voice using a microphone, transcribes the speech to text on the screen in real-time, and immediately reads it back to you using advanced Text-to-Speech (TTS).

## 🚀 Prerequisites: API Keys

To run this project, you must generate free API keys from Groq (for fast Speech-to-Text) and Rime AI (for low-latency Text-to-Speech). 

1. **Groq API Key:** Create a free account at [console.groq.com](https://console.groq.com/) and generate an API key.
2. **Rime AI API Key:** Create a free starter account at [rime.ai](https://rime.ai/) to get your API key.

### Setting up your `.env` file
Once you have your keys, create a file named exactly `.env` in the root directory of your project (in your IDE like VS Code) and add your keys like this:

```env
GROQ_API_KEY=your_groq_api_key_here
RIME_API_KEY=your_rime_api_key_here
```
*(Note: Do not use quotes around the keys, and make sure to add `.env` to your `.gitignore` file so you don't expose your keys publicly).*

## 📁 Project Structure

This project is split into two main Python files:

*   **`rime_hello_world.py`**: This file handles the Text-to-Speech (TTS) configuration. It contains a user-defined function called `TTS_agent()` which initializes the Rime AI service.
*   **`voice_bot2.py`**: This is the main execution file for the speech-to-speech agent. It handles the microphone input, Voice Activity Detection (VAD), and Groq transcription. It imports and calls the `TTS_agent()` function from `rime_hello_world.py` to handle the final audio output.

## 🛠️ Installation & Setup

1. Ensure you have **Python 3.11 or 3.12** installed (required for audio routing libraries).
2. Create and activate a virtual environment.
3. Install the required dependencies:
   ```bash
   pip install "pipecat-ai[groq,rime,silero]" pyaudio python-dotenv
   ```

## ▶️ How to Run

To start the voice agent, run the main file from your terminal:

```bash
python voice_bot2.py
```

Wait for the "Agent is listening!" prompt in your terminal, and start speaking into your microphone!
