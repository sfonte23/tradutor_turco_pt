import os
from converter_audio import converter_para_mp3
from chunker import criar_chunks
from transcrever import transcrever_chunks
from juntar_legendas import juntar_legendas
from traduzir_tr_pt import carregar_modelo, detectar_token_pt_br, traduzir_arquivo_srt

def main():
    print("\n=== GERADOR DE LEGENDAS TURCAS ===")
    print("1 - Converter vídeo para MP3")
    print("2 - Criar chunks de áudio")
    print("3 - Transcrever chunks (TR)")
    print("4 - Traduzir chunks (PT)")
    print("5 - Juntar legendas finais")
    print("0 - Executar tudo (do início)\n")

    etapa = input("Escolha a etapa para iniciar (0-5): ").strip()

    pasta_base = input("Digite o nome da pasta do projeto (ex: S03E01): ")
    nome_video = input("Digite o nome do arquivo de vídeo/áudio (ex: video.mp4): ")

    caminho_pasta = os.path.join(os.getcwd(), pasta_base)
    caminho_video = os.path.join(caminho_pasta, nome_video)

    nome_audio = os.path.splitext(nome_video)[0] + ".mp3"
    caminho_audio = os.path.join(caminho_pasta, nome_audio)

    pasta_chunks = os.path.join(caminho_pasta, "audio_chunks_tr")
    pasta_legendas_tr = os.path.join(caminho_pasta, "legendas_chunks_tr")
    pasta_legendas_pt = os.path.join(caminho_pasta, "legendas_chunks_pt")
    caminho_legenda_final = os.path.join(caminho_pasta, os.path.splitext(nome_video)[0] + "_pt.srt")

    # 1 - Converter
    if etapa == "0" or etapa == "1":
        converter_para_mp3(caminho_video, caminho_audio)

    # 2 - Criar chunks
    if etapa == "0" or etapa == "2":
        arquivos_chunks = criar_chunks(caminho_audio, pasta_chunks, duracao_minutos=10)
    else:
        arquivos_chunks = [(os.path.join(pasta_chunks, f), idx*10*60*1000) 
                           for idx, f in enumerate(sorted(os.listdir(pasta_chunks))) if f.endswith(".mp3")]

    # 3 - Transcrever
    if etapa == "0" or etapa == "3":
        transcrever_chunks(arquivos_chunks, pasta_legendas_tr, idioma="tr")

    # 4 - Traduzir TR -> PT
    if etapa == "0" or etapa == "4":
        tokenizer_tr_en, model_tr_en = carregar_modelo("./model_tr_en")
        tokenizer_en_pt, model_en_pt = carregar_modelo("./model_en_pt")
        pt_token = detectar_token_pt_br(tokenizer_en_pt)
        print(f"🌐 Token PT detectado: {pt_token or '>>por<< (fallback)'}")

        arquivos_srt = sorted([f for f in os.listdir(pasta_legendas_tr) if f.lower().endswith(".srt")])
        for arquivo in arquivos_srt:
            print(f"📄 Traduzindo: {arquivo}")
            traduzir_arquivo_srt(
                os.path.join(pasta_legendas_tr, arquivo),
                tokenizer_tr_en, model_tr_en,
                tokenizer_en_pt, model_en_pt,
                pt_token
            )

    # 5 - Juntar legendas finais (ordenadas por tempo)
    if etapa == "0" or etapa == "5":
        juntar_legendas(pasta_legendas_pt, caminho_legenda_final)

if __name__ == "__main__":
    main()