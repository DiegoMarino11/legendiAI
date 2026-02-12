import gradio as gr
from transcription import transcribe_video
from subtitle_generator import create_srt, burn_subtitles


def process_video(video_path):

    try:
        print("Vídeo recebido:", video_path)

        # 1️⃣ Transcreve
        segments = transcribe_video(video_path)

        # 2️⃣ Cria legenda
        srt_file = create_srt(segments)

        # 3️⃣ Queima legenda no vídeo
        output_video = burn_subtitles(video_path, srt_file)

        print("Vídeo gerado:", output_video)

        return output_video

    except Exception as e:
        print("ERRO REAL:", e)
        raise e


demo = gr.Interface(
    fn=process_video,
    inputs=gr.File(type="filepath", label="Envie seu vídeo"),
    outputs=gr.File(label="Baixar vídeo legendado"),
    title="🎙️ LegendiAI",
    description="Envie um vídeo e receba ele legendado automaticamente com IA."
)

demo.launch()
