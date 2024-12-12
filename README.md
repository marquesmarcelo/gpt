# Introdução

Este é um projeto criado para demonstrar uma integração entre o Llhama e o Python podendo servir como ponto de base para uma aplicação web.

# Configurações iniciais

## Instalação do servidor REST do Ollama localmente usando docker e WSL

Abrir a console do WSL (usei o Ubuntu)

Configurar o repositório

```bash
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey \
    | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list \
    | sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' \
    | sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
sudo apt-get update
```

Instalar o NVIDIA Container Toolkit packages (você precisa ter uma placa de vídeo da NVIDIA)

```bash
sudo apt-get install -y nvidia-container-toolkit
```
```bash
docker run -d --gpus=all -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
```

Executar um modelo localmente. Estou colocando o llama3.2 por conta do tamanho de 2GB. Quanto maior o modelo, mais memória é necessário.

```bash
docker exec -it ollama ollama run llama3.2
```

## Configuração da OpenAI - ChatGPT (ainda não esta funcional e precisa de uma conta com creditos)

Conta na OpenAI: Certifique-se de que você tenha uma conta na OpenAI.

API Key: Acesse a página de configurações da OpenAI (`https://platform.openai.com/api-keys`) gere uma chave de API.

# Instalação de pacotes no projeto

Abra a console da máquina WSL e instale os pacotes necessários:

```bash
pip install openai PyPDF2 chromadb sentence-transformers
```

# Configuração de váriáveis de ambiente

Crie o arquivo `.env` ou configure no sistema operacional as seguintes variáveis de ambiente (não esqueça de adaptar para o seu ambiente)

```bash
OPENAI_API_KEY= "coloque_aqui_a_chave_da_openai"
LLAMA_API_URL= "http://localhost:11434"
USE_CONTEXT = "Yes"
LOAD_FILE = "Yes"
FILE_PATH = "/home/marques/github/gpt/assets/base_treinamento.pdf"
```

Explicações:

* `LOAD_FILE` e `FILE_PATH` são utilizados para carregar um PDF no banco de vetores e o conteúdo deste PDF é utilizado nas consultas caso `USE_CONTEXT` seja `Yes`. Como carregar o conteúdo de um arquivo é algo feito para o treinamento do chat, você pode usar esta função e carregar quantos arquivos quiser, alterando o `FILE_PATH` para cada novo arquivo e reexecutando a aplicação.