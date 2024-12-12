from abc import ABC, abstractmethod
from typing import List
from domain.models.chat_message import ChatMessage

class ChatModelInterface(ABC):
    """
    Interface para definir como os modelos de linguagem devem ser implementados.
    """

    @abstractmethod
    def chat(self, messages: List[ChatMessage]) -> str:
        """
        Método abstrato para enviar mensagens ao modelo de linguagem.
        :param messages: Lista de mensagens (contexto e input do usuário).
        :return: Resposta gerada pelo modelo.
        """
        pass
