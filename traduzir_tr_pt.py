import os
from transformers import MarianTokenizer, MarianMTModel

def carregar_modelo(caminho_modelo):
    print(f"🔄 Carregando modelo local de {caminho_modelo}...")
    tokenizer = MarianTokenizer.from_pretrained(caminho_modelo, local_files_only=True)
    model = MarianMTModel.from_pretrained(caminho_modelo, local_files_only=True)
    return tokenizer, model

def detectar_token_pt_br(tokenizer_en_pt):
    """
    Descobre automaticamente o token de língua para Português Brasil no modelo en-ROMANCE.
    Retorna uma string tipo '>>pt_BR<<' ou None se não achar (usaremos fallback '>>por_BR<<').
    """
    vocab = tokenizer_en_pt.get_vocab()
    # prioridade para pt_BR
    candidatos = [">>pt_BR<<", ">>por_BR<<", ">>pt<<", ">>por<<", ">>pt-PT<<", ">>pt_PT<<", ">>por_PT<<"]
    for tok in candidatos:
        if tok in vocab:
            return tok
    # fallback heurístico
    candidatos_auto = [t for t in vocab.keys() if t.startswith(">>") and t.endswith("<<") and ("pt" in t or "por" in t)]
    if candidatos_auto:
        return sorted(candidatos_auto, key=len)[0]
    return None


def traduzir_texto_duplo(texto, tokenizer_tr_en, model_tr_en, tokenizer_en_pt, model_en_pt, pt_token, num_beams=4, max_new_tokens=128):
    # Turco -> Inglês
    batch_en = tokenizer_tr_en([texto], return_tensors="pt", padding=True)
    translated_en = model_tr_en.generate(**batch_en, num_beams=num_beams, max_new_tokens=max_new_tokens)
    texto_en = tokenizer_tr_en.decode(translated_en[0], skip_special_tokens=True)

    # Inglês -> Português (forçando PT com token de língua)
    if pt_token is None:
        # fallback robusto
        pt_token = ">>por<<"
        # Não fazer print em excesso dentro do loop; comente ou deixe assim se quiser ver avisos
        # print("⚠️ Token de PT não encontrado no vocabulário; usando fallback '>>por<<'.")

    entrada_pt = f"{pt_token} {texto_en}"
    batch_pt = tokenizer_en_pt([entrada_pt], return_tensors="pt", padding=True)
    translated_pt = model_en_pt.generate(**batch_pt, num_beams=num_beams, max_new_tokens=max_new_tokens)
    texto_pt = tokenizer_en_pt.decode(translated_pt[0], skip_special_tokens=True)

    return texto_pt

def traduzir_arquivo_srt(caminho_arquivo, tokenizer_tr_en, model_tr_en, tokenizer_en_pt, model_en_pt, pt_token):
    with open(caminho_arquivo, "r", encoding="utf-8") as f:
        linhas = f.readlines()

    novas_linhas = []
    for linha in linhas:
        linha_strip = linha.strip()
        # Mantém linhas vazias, numeração e timestamps
        if linha_strip.isdigit() or "-->" in linha_strip or linha_strip == "":
            novas_linhas.append(linha)
        else:
            traducao = traduzir_texto_duplo(
                linha_strip,
                tokenizer_tr_en, model_tr_en,
                tokenizer_en_pt, model_en_pt,
                pt_token
            )
            novas_linhas.append(traducao + "\n")

    # --- Cria pasta legendas_chunks_pt no mesmo nível do caminho enviado ---
    pasta_origem = os.path.dirname(caminho_arquivo)
    pasta_pt = os.path.join(pasta_origem, "legendas_chunks_pt")
    os.makedirs(pasta_pt, exist_ok=True)

    # Salva o arquivo dentro da nova pasta
    novo_nome = os.path.join(pasta_pt, os.path.basename(caminho_arquivo).replace(".srt", "_pt.srt"))
    with open(novo_nome, "w", encoding="utf-8") as f:
        f.writelines(novas_linhas)
    
    print(f"✅ Arquivo traduzido salvo em: {novo_nome}")
    
def main():
    pasta = input("Digite o caminho da pasta onde estão os arquivos .srt: ").strip().strip('"')
    
    if not os.path.exists(pasta):
        print("❌ Caminho inválido!")
        return

    # Carrega os modelos locais
    tokenizer_tr_en, model_tr_en = carregar_modelo("./model_tr_en")     # opus-mt-tr-en
    tokenizer_en_pt, model_en_pt = carregar_modelo("./model_en_pt")     # opus-mt-en-ROMANCE

    # Detecta token de PT e mostra qual será usado
    pt_token = detectar_token_pt_br(tokenizer_en_pt)
    print(f"🌐 Token PT detectado: {pt_token or '>>por<< (fallback)'}")

    arquivos_srt = sorted([f for f in os.listdir(pasta) if f.lower().endswith(".srt")])
    if not arquivos_srt:
        print("❌ Nenhum arquivo .srt encontrado nessa pasta.")
        return

    for arquivo in arquivos_srt:
        print(f"📄 Traduzindo: {arquivo}")
        traduzir_arquivo_srt(
            os.path.join(pasta, arquivo),
            tokenizer_tr_en, model_tr_en,
            tokenizer_en_pt, model_en_pt,
            pt_token
        )

if __name__ == "__main__":
    main()
