import openai
from typing import List
from domain.models.chat_message import ChatMessage
from application.interfaces.chat_model_interface import ChatModelInterface

class OpenAIClient(ChatModelInterface):
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        """
        Configura o cliente OpenAI.
        :param api_key: Chave de API da OpenAI.
        :param model: Modelo a ser usado (padrão: gpt-4).
        """
        openai.api_key = api_key
        self.model = model

    def chat(self, messages: List[ChatMessage], use_context: bool) -> str:
        """
        Envia mensagens ao modelo OpenAI e retorna a resposta.
        :param messages: Lista de mensagens (contexto e input do usuário).
        :return: Resposta gerada pelo modelo.
        """
        formatted_messages = [{"role": msg.role, "content": msg.content} for msg in messages]
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=formatted_messages
            )
            return response["choices"][0]["message"]["content"]
        except Exception as e:
            raise RuntimeError(f"Erro ao se comunicar com a API OpenAI: {e}")
