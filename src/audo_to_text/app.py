import whisper

AUDIO_PATH = "./src/audo_to_text/sample_files/first.wav"
MODEL_NAME = "tiny"

def load_model(name: str):
    return whisper.load_model(name)

def load_and_prepare_audio(path: str, model):
    audio = whisper.load_audio(path)
    audio = whisper.pad_or_trim(audio)
    mel = whisper.log_mel_spectrogram(audio).to(model.device)
    return audio, mel

def detect_language(mel, model):
    _, probs = model.detect_language(mel)
    lang = max(probs, key=probs.get)
    return lang, probs

def decode_audio(mel, model):
    options = whisper.DecodingOptions()
    result = whisper.decode(model, mel, options)
    return result.text

def main():
    model = load_model(MODEL_NAME)
    _, mel = load_and_prepare_audio(AUDIO_PATH, model)
    lang, _ = detect_language(mel, model)
    print(f"Detected language: {lang}")
    print(f"Detected Text:")
    text = decode_audio(mel, model)
    print(text)


if __name__ == "__main__":
    main()