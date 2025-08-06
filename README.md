# Voice — Chat‑Bot 🤖

A voice‑driven chatbot system: accepts voice input via microphone, uses speech‑to‑text for transcription, sends text to a (configurable) LLM for response generation, then replies using text‑to‑speech audio output.

## 🌟 Features

- **Voice Input**: Capture user speech via microphone.
- **Real‑Time Transcription**: Convert spoken input into text using STT (e.g. OpenAI Whisper, local models, etc.).
- **LLM‑powered Chat**: Process text prompts with GPT‑style models to generate responses.
- **Voice Output**: Synthesize chatbot replies using TTS engines (e.g. ElevenLabs, Coqui, OpenAI TTS).
- **Conversation Continuity**: Retains context for multi‑turn conversations.
- **Interrupt‑friendly**: Detects silence to manage turn‑taking.
- **Configurable Backends**: Easily switch between OpenAI, Ollama, local models or other compatible systems.
- **Optional Docker Support**: For containerized deployment.

## 🚀 Quick Start

### Prerequisites

- Python 3.9+  
- A microphone (and speaker/headphones for output).
- Optional: CUDA‑enabled NVIDIA GPU for speed.
- Optional: Docker & Docker Compose for containerized setup.
- Required: API keys or local models for STT / LLM / TTS services.

### Installation (Local)

```bash
git clone https://github.com/rubrahha/Voice---Chat-Bot.git
cd Voice---Chat-Bot

python -m venv venv
source venv/bin/activate         # On Windows: `venv\Scripts\activate`

pip install -r requirements.txt
