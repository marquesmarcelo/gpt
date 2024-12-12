class ChatMessage:
    def __init__(self, role: str, content: str):
        """
        Representa uma mensagem em uma interação com o modelo.
        :param role: Pode ser "user" ou "assistant".
        :param content: O conteúdo da mensagem.
        """
        self.role = role
        self.content = content
