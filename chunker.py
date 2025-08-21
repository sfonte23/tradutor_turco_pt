import os
from pydub import AudioSegment

def criar_chunks(caminho_audio, pasta_chunks, duracao_minutos=10, forcar=False):
    """
    Divide áudio em chunks de X minutos (default=10).
    Retorna lista de tuplas (arquivo_chunk, offset_ms).
    """
    if os.path.exists(pasta_chunks) and not forcar:
        arquivos_chunks = sorted([
            os.path.join(pasta_chunks, f) for f in os.listdir(pasta_chunks)
            if f.lower().endswith(".mp3")
        ])
        if arquivos_chunks:
            print(f"⚠️ {len(arquivos_chunks)} chunks já existentes. Pulando corte.")
            # offsets = idx * duracao_minutos*60*1000
            return [(arq, idx * duracao_minutos * 60 * 1000) for idx, arq in enumerate(arquivos_chunks)]

    print("✂️ Criando chunks de áudio...")
    os.makedirs(pasta_chunks, exist_ok=True)
    audio = AudioSegment.from_mp3(caminho_audio)
    chunk_length_ms = duracao_minutos * 60 * 1000
    arquivos_chunks = []

    for idx, i in enumerate(range(0, len(audio), chunk_length_ms)):
        parte_mp3 = os.path.join(pasta_chunks, f"parte_{idx}.mp3")
        audio[i:i + chunk_length_ms].export(parte_mp3, format="mp3")
        arquivos_chunks.append((parte_mp3, i))  # salva também o offset em ms

    print(f"✅ {len(arquivos_chunks)} chunks criados.")
    return arquivos_chunks
