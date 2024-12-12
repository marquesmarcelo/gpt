from abc import ABC, abstractmethod
from typing import List, Tuple

class VectorStoreInterface(ABC):
    @abstractmethod
    def add_to_index(self, segments: List[str], metadatas: List[dict]) -> None:
        """Adiciona segmentos de texto ao banco de vetores com metadados."""
        pass

    @abstractmethod
    def query(self, query_text: str, top_k: int) -> List[dict]:
        """Consulta o banco de vetores e retorna os segmentos mais similares com metadados."""
        pass
