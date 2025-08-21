import os
import re
import pandas as pd

BASE_DIR = "C:/Users/Sergio/Desktop/translate_turco_pt_offline"
pares = []

for episodio in sorted(os.listdir(BASE_DIR)):
    caminho_ep = os.path.join(BASE_DIR, episodio)
    if not os.path.isdir(caminho_ep) or not episodio.startswith("S03E"):
        continue

    pasta_tr = os.path.join(caminho_ep, "legendas_chunks_tr")
    pasta_pt = os.path.join(caminho_ep, "legendas_chunks_pt")

    if not os.path.exists(pasta_tr) or not os.path.exists(pasta_pt):
        print(f"⚠️ Pastas de legendas não encontradas para {episodio}")
        continue

    print(f"📂 Processando {episodio}...")

    for arquivo_tr in sorted(os.listdir(pasta_tr)):
        if not arquivo_tr.endswith(".srt"):
            continue

        caminho_tr = os.path.join(pasta_tr, arquivo_tr)
        # Extrair apenas o número da parte
        numero_parte = arquivo_tr.split("_")[-1]  # exemplo: "0.srt"
        caminho_pt = os.path.join(pasta_pt, f"legenda_pt_parte_{numero_parte}")

        if not os.path.exists(caminho_pt):
            print(f"⚠️ Tradução PT não encontrada para {arquivo_tr} em {episodio}")
            continue

        # Função para extrair falas e verificar contadores
        def extrair_falas_e_verificar(path):
            falas = []
            contador_esperado = 1
            contador_faltando = []
            with open(path, "r", encoding="utf-8") as f:
                for linha in f:
                    linha = linha.strip()
                    if not linha:
                        continue
                    if linha.isdigit():
                        num = int(linha)
                        if num != contador_esperado:
                            contador_faltando.append((contador_esperado, num))
                            contador_esperado = num
                        contador_esperado += 1
                        continue
                    if "-->" in linha:
                        continue
                    falas.append(linha)
            return falas, contador_faltando

        falas_tr, faltando_tr = extrair_falas_e_verificar(caminho_tr)
        falas_pt, faltando_pt = extrair_falas_e_verificar(caminho_pt)

        if faltando_tr:
            print(f"⚠️ Contadores faltando em {arquivo_tr} (TR): {faltando_tr}")
        if faltando_pt:
            print(f"⚠️ Contadores faltando em {arquivo_tr} (PT): {faltando_pt}")

        for tr_texto, pt_texto in zip(falas_tr, falas_pt):
            pares.append({"translation": {"tr": tr_texto, "pt": pt_texto}})

# Salvar dataset
os.makedirs("dados", exist_ok=True)
df = pd.DataFrame(pares)
csv_path = os.path.join("dados", "pares_tr_pt.csv")
df.to_csv(csv_path, index=False, encoding="utf-8")

print(f"✅ Dataset criado com {len(pares)} pares de frases.")
print(f"📄 Arquivo salvo em: {csv_path}")
