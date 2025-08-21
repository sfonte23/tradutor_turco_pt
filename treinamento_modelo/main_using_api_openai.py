from openai import OpenAI
from pydub import AudioSegment
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI()

# Receber inputs
pasta_base = input("Digite o nome da pasta do projeto (ex: s03e02): ")
nome_video = input("Digite o nome do arquivo de vídeo (ex: video.mp4): ")

caminho_pasta = os.path.join(os.getcwd(), pasta_base)
if not os.path.exists(caminho_pasta):
    os.makedirs(caminho_pasta)

caminho_video = os.path.join(caminho_pasta, nome_video)
extensao_arquivo = nome_video.split(".")[-1]

# Pastas para salvar chunks e legendas parciais
pasta_chunks = os.path.join(caminho_pasta, "audio_chunks_tr")
pasta_legendas = os.path.join(caminho_pasta, "legendas_chunks_pt")

os.makedirs(pasta_chunks, exist_ok=True)
os.makedirs(pasta_legendas, exist_ok=True)

def arquivo_existe(nome_arquivo):
    return os.path.isfile(nome_arquivo)

def ms_para_timestamp(ms):
    horas = ms // (3600 * 1000)
    minutos = (ms % (3600 * 1000)) // (60 * 1000)
    segundos = (ms % (60 * 1000)) // 1000
    milissegundos = ms % 1000
    return f"{horas:02}:{minutos:02}:{segundos:02},{milissegundos:03}"

# Verifica se já existem chunks prontos
arquivos_chunks = sorted([
    os.path.join(pasta_chunks, f) for f in os.listdir(pasta_chunks)
    if f.lower().endswith(".mp3")
])

if arquivos_chunks:
    print(f"⚠️ Encontrados {len(arquivos_chunks)} chunks existentes em '{pasta_chunks}'. Pulando conversão e corte...")
else:
    # Converter vídeo para mp3
    caminho_audio = os.path.join(caminho_pasta, "audio.mp3")
    print("🎬 Convertendo vídeo para áudio MP3...")
    if arquivo_existe(caminho_audio):
        print(f"⚠️  Já existe o arquivo {caminho_audio}. Pulando conversão.")
    else:
        audio = AudioSegment.from_file(caminho_video, format=extensao_arquivo)
        audio.export(caminho_audio, format="mp3")

    # Carregar áudio e dividir em chunks de 10 minutos
    print("⏳ Carregando áudio MP3 e dividindo em chunks de 10 minutos...")
    audio = AudioSegment.from_mp3(caminho_audio)
    chunk_length_ms = 10 * 60 * 1000
    chunks = [audio[i:i + chunk_length_ms] for i in range(0, len(audio), chunk_length_ms)]

    arquivos_chunks = []
    for idx, chunk in enumerate(chunks):
        parte_mp3 = os.path.join(pasta_chunks, f"parte_{idx}.mp3")
        print(f"💾 Exportando chunk {idx + 1} como {parte_mp3}...")
        chunk.export(parte_mp3, format="mp3")
        arquivos_chunks.append(parte_mp3)

legenda_final_pt = ""
contador = 1
offset_ms = 0

# Processar cada chunk encontrado
for idx, parte_mp3 in enumerate(arquivos_chunks):
    legenda_chunk = os.path.join(pasta_legendas, f"legenda_pt_parte_{idx}.srt")

    if arquivo_existe(legenda_chunk):
        print(f"⚠️  Legenda traduzida {legenda_chunk} já existe. Pulando transcrição e tradução do chunk {idx + 1}...")
        with open(legenda_chunk, "r", encoding="utf-8") as f:
            texto = f.read()

        for bloco in texto.strip().split("\n\n"):
            linhas = bloco.split("\n")
            if len(linhas) >= 3:
                tempo = linhas[1]
                if " --> " not in tempo:
                    continue
                inicio, fim = tempo.split(" --> ")
                inicio_ms = offset_ms + (int(inicio[0:2]) * 3600 + int(inicio[3:5]) * 60 + int(inicio[6:8])) * 1000 + int(inicio[9:12])
                fim_ms = offset_ms + (int(fim[0:2]) * 3600 + int(fim[3:5]) * 60 + int(fim[6:8])) * 1000 + int(fim[9:12])
                legenda_final_pt += f"{contador}\n{ms_para_timestamp(inicio_ms)} --> {ms_para_timestamp(fim_ms)}\n" + "\n".join(linhas[2:]) + "\n\n"
                contador += 1
        offset_ms += len(AudioSegment.from_mp3(parte_mp3))
        continue

    print(f"🎤 Transcrevendo áudio chunk {idx + 1} (em turco)...")
    with open(parte_mp3, "rb") as f:
        transcricao = client.audio.transcriptions.create(
            file=f,
            model="whisper-1",
            language="tr",
            response_format="srt"
        )

    print(f"🔄 Tradução do chunk {idx + 1} para português iniciada...")
    traducao = client.responses.create(
        model="gpt-4o-mini",
        input=f"Traduza para português mantendo o formato SRT e estilo conversacional:\n\n{transcricao}"
    )

    with open(legenda_chunk, "w", encoding="utf-8") as f:
        f.write(traducao.output_text)

    for bloco in traducao.output_text.strip().split("\n\n"):
        linhas = bloco.split("\n")
        if len(linhas) >= 3:
            tempo = linhas[1]
            if " --> " not in tempo:
                continue
            inicio, fim = tempo.split(" --> ")
            inicio_ms = offset_ms + (int(inicio[0:2]) * 3600 + int(inicio[3:5]) * 60 + int(inicio[6:8])) * 1000 + int(inicio[9:12])
            fim_ms = offset_ms + (int(fim[0:2]) * 3600 + int(fim[3:5]) * 60 + int(fim[6:8])) * 1000 + int(fim[9:12])
            legenda_final_pt += f"{contador}\n{ms_para_timestamp(inicio_ms)} --> {ms_para_timestamp(fim_ms)}\n" + "\n".join(linhas[2:]) + "\n\n"
            contador += 1

    offset_ms += len(AudioSegment.from_mp3(parte_mp3))

# Salvar legenda final com mesmo nome do vídeo, mas extensão .srt
nome_legenda_final = os.path.splitext(nome_video)[0] + ".srt"
caminho_legenda_final = os.path.join(caminho_pasta, nome_legenda_final)
print(f"💾 Salvando legenda final em português no arquivo {caminho_legenda_final}...")
with open(caminho_legenda_final, "w", encoding="utf-8") as f:
    f.write(legenda_final_pt)

print(f"✅ Legenda em português gerada: {caminho_legenda_final}")
