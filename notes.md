# Open LLM VTuber

Basically, a websocket server.

- Python FastAPI webserver (router & websocket)


Flow
- If preload, initialized speech recognition (ASR) and  Text to Speech (TTS)
  - init
    - ASRFactory and TTSFactory for switching between models