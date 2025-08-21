# 🎬 TRADUTOR_TURCO_PT

Este projeto automatiza o processo de baixar vídeos do YouTube em turco, convertê-los para áudio MP3, transcrevê-los com o modelo **Whisper da OpenAI** e traduzi-los para o português, mantendo o formato **SRT**. Com isso, você pode assistir a vídeos turcos com legendas automáticas e sincronizadas em português.

-----

## 🚀 Funcionalidades

  - **📥 Download de Vídeo:** Baixa vídeos do YouTube em alta qualidade usando `yt-dlp`.
  - **🎼 Conversão para MP3:** Converte o vídeo para o formato de áudio MP3 com `pydub`.
  - **✂️ Processamento Otimizado:** Divide o áudio em partes de 10 minutos para um processamento mais eficiente.
  - **🗣 Transcrição:** Transcreve o áudio em turco usando o modelo `whisper-1`.
  - **🌎 Tradução Automática:** Traduz o texto transcrito para o português, preservando a formatação SRT.
  - **📄 Geração de SRT:** Gera um arquivo `.srt` final, pronto para ser usado em qualquer player.
  - **🎯 Compatibilidade:** Oferece conversão opcional de codec para garantir compatibilidade com TVs e outros dispositivos.

-----

## 📂 Estrutura do Projeto

```
TRADUTOR_TURCO_PT/
├── S03E01/
│   ├── audio_chunks/         # Áudio dividido em partes
│   ├── legendas_chunks/      # Legendas parciais traduzidas
│   └── S03E01.mov/mp4/mp3/srt
│
├── S03E02/
│   └── ...
│
├── .env                      # Chave da API da OpenAI
├── conversor_mp4.py           # Conversor para MP4 compatível (opcional)
├── download_video.py          # Script para baixar vídeos
├── main.py                    # Script principal de transcrição e tradução
├── requirements.txt           # Dependências do projeto
└── README.md
```

-----

## 🛠 Pré-requisitos

### Dependências Python

Instale todas as dependências do projeto com o seguinte comando:

```bash
pip install -r requirements.txt
```

### FFmpeg

É necessário ter o **FFmpeg** instalado no seu sistema. Você pode baixá-lo aqui:
[🔗 https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)

-----

## 🔑 Configuração

Crie um arquivo `.env` na raiz do projeto e adicione sua chave da API OpenAI:

```
OPENAI_API_KEY=sua_chave_aqui
```

-----

## 📌 Uso

1.  **Baixar o vídeo do YouTube**

    Execute este script para baixar o vídeo:

    ```bash
    python download_video.py
    ```

2.  **(Opcional) Converter codec para compatibilidade**

    Se precisar de maior compatibilidade (por exemplo, para TVs), use este script:

    ```bash
    python conversor_mp4.py
    ```

3.  **Gerar legendas em português**

    Execute o script principal para transcrever e traduzir o vídeo. O arquivo `.srt` final será salvo na mesma pasta do vídeo.

    ```bash
    python main.py
    ```

-----

## 📄 Licença

Este projeto é distribuído sob a licença **MIT**. Sinta-se à vontade para usar e modificar.

-----

## 💡 Melhorias Futuras

  - Suporte para múltiplos idiomas de origem.
  - Interface gráfica simples para facilitar o uso.
  - Opção de gerar legenda embutida (hardsub) no vídeo.

-----

## 🤝 Contribuição

Pull requests são muito bem-vindos\! Para grandes mudanças, por favor, abra uma *issue* primeiro para discutirmos o que você gostaria de alterar.