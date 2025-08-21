import os
import re

def tempo_em_milisegundos(tempo):
    h, m, s_ms = tempo.split(":")
    s, ms = s_ms.split(",")
    return (int(h) * 3600 + int(m) * 60 + int(s)) * 1000 + int(ms)

def juntar_legendas(pasta_legendas, caminho_saida):
    """Junta todos os arquivos .srt de uma pasta em um único arquivo ordenado por tempo."""
    if os.path.isfile(caminho_saida):
        print(f"⚠️ Legenda final já existe: {caminho_saida}")
        return caminho_saida

    arquivos_srt = sorted([
        os.path.join(pasta_legendas, f) for f in os.listdir(pasta_legendas)
        if f.lower().endswith(".srt")
    ])

    if not arquivos_srt:
        print(f"❌ Nenhum arquivo .srt encontrado em {pasta_legendas}")
        return None

    blocos = []
    for arquivo in arquivos_srt:
        with open(arquivo, "r", encoding="utf-8") as f:
            conteudo = f.read()

        for bloco in re.split(r'\n\s*\n', conteudo.strip()):
            linhas = bloco.split("\n")
            if len(linhas) >= 3:
                tempo = linhas[1]
                inicio, _ = tempo.split(" --> ")
                texto = "\n".join(linhas[2:])
                blocos.append((tempo_em_milisegundos(inicio), tempo, texto))

    blocos.sort(key=lambda x: x[0])

    with open(caminho_saida, "w", encoding="utf-8") as f:
        for i, (_, tempo, texto) in enumerate(blocos, start=1):
            f.write(f"{i}\n{tempo}\n{texto}\n\n")

    print(f"✅ Legenda final salva em: {caminho_saida}")
    return caminho_saida
