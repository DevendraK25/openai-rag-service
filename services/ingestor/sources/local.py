# sources/local.py
from pathlib import Path
from sources.base import BaseSource

class LocalSource(BaseSource):
    def __init__(self, path="./data"):
        self.path = path

    def list_files(self):
        return list(Path(self.path).glob("*.txt"))

    def read_file(self, file_path):
        return Path(file_path).read_text()
