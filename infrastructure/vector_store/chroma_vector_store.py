import chromadb
from chromadb.utils import embedding_functions
from typing import List, Tuple
from application.interfaces.vector_store_interface import VectorStoreInterface

class ChromaVectorStore(VectorStoreInterface):
    def __init__(self, persist_directory: str = "chroma_db"):
        """Inicializa o ChromaVectorStore com persistência."""
        self.persist_directory = persist_directory
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collection_name = "file_segments"
        self.embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
        self.collection = self._get_or_create_collection()

    def _cleanup_inconsistent_collections(self):
        """Remove coleções inconsistentes antes de carregar."""
        try:
            collections = self.client.list_collections()
            print(f"Verificando {len(collections)} coleções existentes.")
            for col in collections:
                if not col.name.startswith(self.collection_name):
                    print(f"Removendo coleção inconsistente: {col.name}")
                    self.client.delete_collection(name=col.name)
        except Exception as e:
            print(f"Erro ao limpar coleções inconsistentes: {e}")

    def _get_or_create_collection(self):
        """Cria ou recupera a coleção do banco."""
        self._cleanup_inconsistent_collections()
        try:
            existing_collections = [col.name for col in self.client.list_collections()]
            if self.collection_name not in existing_collections:
                print(f"Coleção '{self.collection_name}' não encontrada. Criando uma nova coleção.")
                return self.client.create_collection(
                    name=self.collection_name, embedding_function=self.embedding_fn
                )
            print(f"Coleção '{self.collection_name}' encontrada. Carregando...")
            return self.client.get_collection(name=self.collection_name)
        except Exception as e:
            print(f"Erro ao acessar coleções: {e}")
            print("Tentando recriar a coleção...")
            return self.client.create_collection(
                name=self.collection_name, embedding_function=self.embedding_fn
            )

    def add_to_index(self, segments: List[str], metadatas: List[dict]) -> None:
        """Adiciona segmentos de texto ao banco."""
        self.collection.add(
            documents=segments,
            metadatas=metadatas,
            ids=[f"segment_{i}" for i in range(len(segments))],
        )
        print(f"{len(segments)} segmentos adicionados ao banco.")

    def query(self, query_text: str, top_k: int) -> Tuple[List[str], List[dict]]:
        """
        Consulta o banco de vetores e retorna os segmentos mais similares com metadados.
        :param query_text: Texto da consulta.
        :param top_k: Número de resultados mais relevantes.
        :return: Lista de textos (documentos) e seus metadados.
        """
        try:
            results = self.collection.query(
                query_texts=[query_text], n_results=top_k
            )
            # Extrair documentos como strings
            documents = results["documents"][0] if "documents" in results else []
            metadatas = results["metadatas"][0] if "metadatas" in results else []
            return documents, metadatas
        except Exception as e:
            print(f"Erro ao consultar o banco de vetores: {e}")
            return [], []
    
    def get_all_hashes(self) -> List[str]:
        """
        Retorna todas as hashes dos arquivos armazenados no banco de vetores.
        :return: Lista de hashes.
        """
        try:
            # Recupera todos os metadados da coleção
            all_metadatas = self.collection.get(include=["metadatas"])["metadatas"]
            return [metadata["hash"] for metadata in all_metadatas if "hash" in metadata]
        except Exception as e:
            print(f"Erro ao recuperar hashes: {e}")
            return []