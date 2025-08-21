import os
from faster_whisper import WhisperModel

def ms_para_timestamp(ms):
    horas = ms // (3600 * 1000)
    minutos = (ms % (3600 * 1000)) // (60 * 1000)
    segundos = (ms % (60 * 1000)) // 1000
    milissegundos = ms % 1000
    return f"{horas:02}:{minutos:02}:{segundos:02},{milissegundos:03}"

def transcrever_chunks(arquivos_chunks, pasta_legendas, idioma="tr", modelo_nome="medium", device="cpu", forcar=False):
    """
    Transcreve todos os chunks de áudio, criando arquivos .srt individuais e um final concatenado.
    arquivos_chunks deve ser lista de tuplas (arquivo, offset_ms).
    """
    os.makedirs(pasta_legendas, exist_ok=True)

    model = WhisperModel(modelo_nome, device=device, compute_type="int8")
    legenda_final = ""
    contador = 1

    for idx, (parte_mp3, offset_ms) in enumerate(arquivos_chunks):
        legenda_chunk = os.path.join(pasta_legendas, f"legenda_parte_{idx}.srt")

        if os.path.isfile(legenda_chunk) and not forcar:
            print(f"⚠️ Legenda do chunk {idx+1} já existe. Pulando...")
            with open(legenda_chunk, encoding="utf-8") as f:
                legenda_chunk_text = f.read()
        else:
            print(f"⏳ Processando chunk {idx+1}...")
            segments, _ = model.transcribe(parte_mp3, language=idioma)

            temp_srt = ""
            for seg in segments:
                inicio_ms = offset_ms + int(seg.start * 1000)
                fim_ms = offset_ms + int(seg.end * 1000)
                temp_srt += f"{contador}\n{ms_para_timestamp(inicio_ms)} --> {ms_para_timestamp(fim_ms)}\n{seg.text.strip()}\n\n"
                contador += 1

            legenda_chunk_text = temp_srt
            with open(legenda_chunk, "w", encoding="utf-8") as f:
                f.write(legenda_chunk_text)

        legenda_final += legenda_chunk_text

    return legenda_final
