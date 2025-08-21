import re

# Caminho do arquivo original
arquivo_srt = "C:/Users/Sergio/Desktop/translate_turco_pt_offline/S03E05/S03E05.srt"
# Arquivo que será salvo com legendas corrigidas
arquivo_corrigido = "legendas_corrigidas.srt"

# Função para converter tempo em milissegundos para facilitar a ordenação
def tempo_em_milisegundos(tempo):
    h, m, s_ms = tempo.split(":")
    s, ms = s_ms.split(",")
    total = (int(h)*3600 + int(m)*60 + int(s))*1000 + int(ms)
    return total

# Lendo o arquivo SRT
with open(arquivo_srt, "r", encoding="utf-8") as f:
    conteudo = f.read()

# Dividindo por blocos de legendas
blocos = re.split(r'\n\s*\n', conteudo.strip())

# Processando cada bloco
legendas = []
for bloco in blocos:
    linhas = bloco.split("\n")
    if len(linhas) >= 3:
        numero = linhas[0]
        tempo = linhas[1]
        texto = "\n".join(linhas[2:])
        inicio, fim = tempo.split(" --> ")
        legendas.append((tempo_em_milisegundos(inicio), tempo, texto))

# Ordenando pelo tempo de início
legendas.sort(key=lambda x: x[0])

# Escrevendo o arquivo corrigido com numeração correta
with open(arquivo_corrigido, "w", encoding="utf-8") as f:
    for i, (_, tempo, texto) in enumerate(legendas, start=1):
        f.write(f"{i}\n{tempo}\n{texto}\n\n")

print(f"Arquivo corrigido salvo como {arquivo_corrigido}")
