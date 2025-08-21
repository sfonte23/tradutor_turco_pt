import os
from pydub import AudioSegment

def arquivo_existe(path):
    return os.path.isfile(path)

def converter_para_mp3(caminho_entrada, caminho_saida):
    """Converte vídeo para MP3 somente se ainda não existir."""
    if arquivo_existe(caminho_saida):
        print(f"⚠️ Arquivo {os.path.basename(caminho_saida)} já existe. Pulando conversão.")
        return

    extensao = caminho_entrada.split(".")[-1].lower()
    print(f"🎬 Convertendo {os.path.basename(caminho_entrada)} para MP3...")
    audio = AudioSegment.from_file(caminho_entrada, format=extensao)
    audio.export(caminho_saida, format="mp3")
    print(f"✅ Arquivo gerado: {os.path.basename(caminho_saida)}")
