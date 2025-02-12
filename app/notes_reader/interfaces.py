from abc import ABC, abstractmethod
from pathlib import Path

from app.models.note import Note


class NotesLoaderABC(ABC):
    @property
    @abstractmethod
    def dir_path(self) -> Path:
        raise NotImplementedError

    @abstractmethod
    def load(self) -> list[Note]:
        raise NotImplementedError
