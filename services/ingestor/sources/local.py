# sources/local.py
from pathlib import Path
from sources.base import BaseSource
from PyPDF2 import PdfReader

class LocalSource(BaseSource):
    def __init__(self, path="./data"):
        self.path = path
        self._exts = {".txt", ".pdf"}

    def list_files(self):
        p = Path(self.path)
        return [f for f in p.rglob("*") if f.suffix.lower() in self._exts]

    def read_file(self, file_path):
        p = Path(file_path)
        if p.suffix.lower() == ".pdf":
            try:
                reader = PdfReader(str(p))
                return "\n".join((page.extract_text() or "") for page in reader.pages)
            except Exception:
                return ""  # return empty string on extraction failure (or raise/log as needed)
        else:
            return p.read_text()
