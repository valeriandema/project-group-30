from abc import ABC, abstractmethod
from pathlib import Path


class StorageInterface(ABC):
    def __init__(self, file_path: Path):
        self.file_path = file_path

    @abstractmethod
    def save(self, data: object) -> bool:
        """Save data to file."""
        pass

    @abstractmethod
    def load(self) -> object:
        """Load data from file."""
        pass
