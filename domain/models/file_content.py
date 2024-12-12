from typing import List

class FileContent:
    def __init__(self, segments: List[str]):
        """
        Representa o conteúdo do PDF como uma lista de segmentos.
        :param segments: Lista de segmentos de texto extraídos do PDF.
        """
        self.segments = segments

    @staticmethod
    def from_raw_text(raw_text: str) -> 'FileContent':
        """
        Converte texto bruto em uma instância de FileContent.
        :param raw_text: Texto bruto extraído do PDF.
        :return: Instância de FileContent contendo os segmentos do texto.
        """
        # Divide o texto bruto em segmentos (exemplo: por linhas)
        segments = raw_text.split("\n")
        return FileContent(segments)

