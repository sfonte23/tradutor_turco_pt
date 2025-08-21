import yt_dlp
import os

def download_video(url, pasta, nome_video):
    if not os.path.exists(pasta):
        os.makedirs(pasta)
    output_path = os.path.join(pasta, nome_video)
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': output_path,
        'merge_output_format': 'mp4',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    print(f"Vídeo salvo em {output_path}")
    return output_path

if __name__ == "__main__":
    url = input("Digite a URL do vídeo do YouTube: ")
    pasta = input("Digite o nome da pasta onde salvar: ")
    nome_video = input("Digite o nome do arquivo de vídeo (ex: video.mp4): ")
    download_video(url, pasta, nome_video)
