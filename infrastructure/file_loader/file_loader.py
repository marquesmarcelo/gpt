
import hashlib
from infrastructure.file_loader.pdf_loader_pypdf import PDFLoaderPyPDF
from domain.models.file_content import FileContent
from application.interfaces.vector_store_interface import VectorStoreInterface

class FileLoader:
    def __init__(self, file_path: str, vector_store: VectorStoreInterface):
        """
        Configura o sistema para carregar um arquivo para a base de vetores.
        :param file_path: localização do arquivo.
        """
        self.file_path = file_path
        self.vector_store = vector_store
        
    def _calculate_file_hash(self) -> str:
        """
        Calcula a hash SHA-256 do arquivo.
        :param file_path: Caminho do arquivo.
        :return: Hash do conteúdo do rquivo.
        """
        hasher = hashlib.sha256()
        with open(self.file_path, "rb") as bin_file:
            hasher.update(bin_file.read())
        return hasher.hexdigest()
    
    def add_file(self):
        """
        Adiciona texto de um arquivo ao banco de vetores, se ainda não existir.
        :param pdf_path: Caminho do arquivo PDF.
        """
        try:
            # Calcula a hash do arquivo
            pdf_hash = self._calculate_file_hash()

            # Verifica se o PDF já está no banco
            existing_hashes = self.vector_store.get_all_hashes()
            
            if pdf_hash in existing_hashes:
                print(f"O arquivo '{self.file_path}' já foi processado. Ignorando...")
                return

            # Extrai texto do PDF e processa
            raw_text = PDFLoaderPyPDF.load_text_from_pdf(self.file_path)
            file_content = FileContent.from_raw_text(raw_text)

            # Cria metadados para cada segmento
            metadatas = [{"source": self.file_path, "segment_index": i, "hash": pdf_hash} for i in range(len(file_content.segments))]
            
            # Adiciona os segmentos e metadados ao banco de vetores
            self.vector_store.add_to_index(file_content.segments, metadatas)
            print(f"Arquivo '{self.file_path}' adicionado ao banco de vetores.")
        except Exception as e:
            raise RuntimeError(f"Erro ao processar o PDF '{self.file_path}': {e}")