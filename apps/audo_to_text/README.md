### Packaged required
- brew install ffmpeg

## Python Packages
- openai-whisper
- streamlit-webrtc
- soundfile
- fpdf


### How to run

1. CLI
    - Go to root dir gen-ai-gl
    - Run following command
        - poetry run python -m cli.cli --audio sample_files/first.wav

2. Streamlit UI
    - Export Following environment variables
        - export STREAMLIT_SERVER_PORT=8502
        - export STREAMLIT_SERVER_HEADLESS=true
    - Go to dir apps/audo_to_text
    - poetry run streamlit run main.py