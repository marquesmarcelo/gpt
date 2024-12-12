from domain.models.chat_message import ChatMessage
from application.use_cases.chat_interaction import ChatInteraction
from infrastructure.llama.llama_rest_client import LlamaRestClient
from infrastructure.openai.openai_client import OpenAIClient
from infrastructure.vector_store.chroma_vector_store import ChromaVectorStore
from infrastructure.file_loader.file_loader import FileLoader
import os
from dotenv import load_dotenv

# Carregar variáveis do arquivo .env
load_dotenv()

openai_api_key = os.environ.get("OPENAI_API_KEY")
llama_api_url = os.environ.get("LLAMA_API_URL")
load_file = os.environ.get("LOAD_FILE").lower()
file_path = os.environ.get("FILE_PATH").lower()
use_context = os.environ.get("USE_CONTEXT").lower()

vector_store = ChromaVectorStore(persist_directory="chroma_db")

def main():
    # Configurar qual modelo usar: "openai", "llama" ou "llama-pdf"
    modelo_escolhido = "llama"  # Altere para o modelo desejado

    if modelo_escolhido == "openai":
        # Configurar o cliente OpenAI
        chat_model = OpenAIClient(api_key=openai_api_key, vector_store=vector_store)
    elif modelo_escolhido == "llama":
        # Configurar o cliente Llama com ou sem vetores
        chat_model = LlamaRestClient(api_url=llama_api_url, vector_store=vector_store)
    else:
        raise ValueError(f"Modelo '{modelo_escolhido}' não é suportado.")

    # Criar caso de uso de interação
    chat_interaction = ChatInteraction(chat_model)

    # Modo "llama-pdf": adicionar arquivo ao banco de vetores antes da consulta
    if load_file == "yes":
        
        print(f"Adicionando arquivo '{file_path}' ao banco de vetores...")
        file_loader = FileLoader(file_path, vector_store=vector_store)
        
        file_loader.add_file()
        print("Arquivo adicionado com sucesso!")

    active = True
    
    print("Bem-vindo ao Chat Interativo! Digite '/sair' para encerrar.")
    while active:       
        entrada_usuario = input("Você: ")
        if entrada_usuario.lower() == "/sair":
            print(f"Adeus!") 
            break
        else:
            messages = [
                ChatMessage(role="user", content=entrada_usuario)
            ]
            resposta = chat_interaction.send_message(messages, use_context)
            print(f"ChatBot {modelo_escolhido}: {resposta}")    

if __name__ == "__main__":
    main()