import subprocess

def converter_para_mp4_compatível(caminho_arquivo_entrada, caminho_arquivo_saida):
    cmd = [
        "ffmpeg",
        "-i", caminho_arquivo_entrada,
        "-c:v", "libx264",  # vídeo H.264
        "-preset", "veryfast",
        "-progress", "pipe:1",
        "-crf", "23",
        "-c:a", "aac",      # áudio AAC
        "-b:a", "192k",     # bitrate do áudio
        "-movflags", "+faststart",  # para streaming rápido (bom pra players)
        caminho_arquivo_saida
    ]
    try:
        subprocess.run(cmd, check=True)
        print(f"✅ Conversão para MP4 compatível concluída: {caminho_arquivo_saida}")
    except subprocess.CalledProcessError as e:
        print("❌ Erro na conversão:", e)

if __name__ == "__main__":
    caminho_video_mp4 = r"C:\Users\Sergio\Desktop\tradutor\S03E02\S03E02.mp4"
    caminho_video_mov = caminho_video_mp4.rsplit('.', 1)[0] + ".mov"
    converter_para_mp4_compatível(caminho_video_mp4, caminho_video_mov)
