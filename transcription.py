import whisper

model = whisper.load_model("small")  # ou tiny

def transcribe_video(video_path):

    result = model.transcribe(
        video_path,
        language="pt",
        temperature=0
    )

    return result["segments"]


