import subprocess
import uuid
import textwrap


# -----------------------------
# FORMATA TEMPO DO SRT
# -----------------------------
def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds - int(seconds)) * 1000)

    return f"{hours:02}:{minutes:02}:{secs:02},{millis:03}"


# -----------------------------
# DIVIDE TEXTO SEM QUEBRAR TIMING
# -----------------------------
def split_text_proportionally(text, start, end):

    MAX_CHARS = 42  # padrão streaming

    chunks = textwrap.wrap(text, MAX_CHARS)

    # se não precisa dividir
    if len(chunks) == 1:
        return [(text, start, end)]

    total_chars = sum(len(chunk) for chunk in chunks)
    total_duration = end - start

    results = []
    current_start = start

    for chunk in chunks:

        proportion = len(chunk) / total_chars
        chunk_duration = total_duration * proportion

        current_end = current_start + chunk_duration

        results.append((chunk, current_start, current_end))

        current_start = current_end

    return results


# -----------------------------
# CRIA O SRT
# -----------------------------
def create_srt(segments):

    srt_filename = f"legenda_{uuid.uuid4().hex}.srt"
    index = 1

    with open(srt_filename, "w", encoding="utf-8") as f:

        for segment in segments:

            text = " ".join(segment['text'].split())
            start = segment['start']
            end = segment['end']

            pieces = split_text_proportionally(text, start, end)

            for chunk, chunk_start, chunk_end in pieces:

                f.write(f"{index}\n")
                f.write(f"{format_time(chunk_start)} --> {format_time(chunk_end)}\n")
                f.write(f"{chunk}\n\n")

                index += 1

    return srt_filename


# -----------------------------
# QUEIMA LEGENDA NO VÍDEO
# -----------------------------
def burn_subtitles(video_path, subtitle_path):

    output_video = f"video_legendado_{uuid.uuid4().hex}.mp4"

    # evita bug no Windows
    subtitle_path = subtitle_path.replace("\\", "/")

    # estilo profissional
    style = (
        "Fontname=Arial,"
        "Fontsize=14,"
        "PrimaryColour=&H0000FFFF,"  # amarelo
        "OutlineColour=&H00000000,"
        "BorderStyle=1,"
        "Outline=1,"
        "Shadow=0,"
        "Alignment=2,"
        "MarginV=20"
    )

    vf_string = f"subtitles='{subtitle_path}':force_style='{style}'"

    command = [
        "ffmpeg",
        "-y",
        "-i", video_path,
        "-vf", vf_string,
        output_video
    ]

    subprocess.run(command, check=True)

    return output_video
