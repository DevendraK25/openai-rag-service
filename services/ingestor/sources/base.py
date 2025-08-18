# sources/base.py
from abc import ABC, abstractmethod

class BaseSource(ABC):
    @abstractmethod
    def list_files(self):
        """Return list of file identifiers"""
        pass

    @abstractmethod
    def read_file(self, file_identifier):
        """Return the content of a file/blob"""
        pass
