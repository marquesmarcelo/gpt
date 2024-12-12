from typing import List
from domain.models.chat_message import ChatMessage
from application.interfaces.chat_model_interface import ChatModelInterface

class ChatInteraction:
    def __init__(self, chat_model: ChatModelInterface):
        self.chat_model = chat_model

    def send_message(self, messages, use_context):
        """
        Envia uma mensagem ao modelo, utilizando o banco de vetores para enriquecer o contexto.
        :param messages: Lista de mensagens do usuário.
        :return: Resposta do modelo.
        """
        print(use_context)
        if (use_context == "yes"):
            # Última mensagem do usuário
            user_message = messages[-1].content

            # Consulta ao banco de vetores
            context_segments, metadatas = self.chat_model.vector_store.query(user_message, top_k=5)
    
            # Combine o contexto do banco de vetores com a mensagem
            context = "\n".join(context_segments)
            
            enriched_message = (
                f"Contexto fornecido:\n"
                f"{context}\n\n"
                f"Pergunta:\n"
                f"{user_message}\n\n"
                f"Regras:\n"
                f"1. Responda com base apenas no contexto fornecido acima.\n"
                f"2. Quando conseguir montar uma resposta, não precisa informar que esta utilizando o contexto como base.\n"
                f"3. Se o contexto não for suficiente para responder, diga: "
                f"'Não há informações suficientes no contexto fornecido.'"
            )

            # Substitua a última mensagem pelo texto enriquecido
            messages[-1].content = enriched_message

        # Enviar mensagem ao modelo
        return self.chat_model.chat(messages)
