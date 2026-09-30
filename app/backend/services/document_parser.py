import os
import pypdf
import docx
from typing import Dict, Any, List

class DocumentParser:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.extension = os.path.splitext(file_path)[1].lower()
    
    def parse(self) -> str:
        """Parses the document and returns raw text content."""
        if self.extension == ".pdf":
            return self._parse_pdf()
        elif self.extension in [".docx", ".doc"]:
            return self._parse_docx()
        elif self.extension == ".txt":
            return self._parse_txt()
        else:
            raise ValueError(f"Unsupported file format: {self.extension}")
    
    def _parse_pdf(self) -> str:
        text = ""
        with open(self.file_path, "rb") as file:
            reader = pypdf.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() + "\n"
        return text

    def _parse_docx(self) -> str:
        doc = docx.Document(self.file_path)
        return "\n".join([para.text for para in doc.paragraphs])

    def _parse_txt(self) -> str:
        with open(self.file_path, "r", encoding="utf-8") as file:
            return file.read()
