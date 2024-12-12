import PyPDF2

class PDFLoaderPyPDF:
    @staticmethod
    def load_text_from_pdf(pdf_path: str) -> str:
        """
        Carrega e retorna o texto de um arquivo PDF.
        :param pdf_path: Caminho para o arquivo PDF.
        :return: Texto extraído do PDF como uma string.
        """
        try:
            with open(pdf_path, "rb") as pdf_file:
                reader = PyPDF2.PdfReader(pdf_file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text()
            return text
        except Exception as e:
            raise RuntimeError(f"Erro ao carregar o PDF '{pdf_path}': {e}")
