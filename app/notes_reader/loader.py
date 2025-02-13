import re
from pathlib import Path
from typing import Any, Iterable

import yaml

from app.models import Note, Tag
from app.notes_reader.interfaces import NotesLoaderABC


class NotesLoader(NotesLoaderABC):
    MD_SUFFIX = ".md"

    def __init__(self, dir_path: Path, tags: Iterable[Tag]) -> None:
        self._tags = set(tags)
        self.dir_path = dir_path

    @property
    def dir_path(self) -> Path:
        return self._dir_path

    @dir_path.setter
    def dir_path(self, dir_path: Path) -> None:
        self._dir_path = dir_path

    def _validate_tags(self, tags: set[Tag]) -> bool:
        """Checks if the note has all the required tags."""
        return bool(tags & self._tags)

    @staticmethod
    def _extract_file_metadata(content: str) -> Any:
        """Extracts metadata from the Obsydian note file."""
        match_ = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
        if not match_:
            return {}
        try:
            return yaml.safe_load(match_.group(1))
        except yaml.YAMLError:
            return {}

    def load(self) -> list[Note]:
        """Loads notes from the directory. Returns a list of Note objects."""
        notes = []
        for file in self.dir_path.iterdir():
            if not file.is_file() or file.suffix != self.MD_SUFFIX:
                continue

            with file.open("r", encoding="utf-8") as f:
                content = f.read()

            metadata = self._extract_file_metadata(content)
            tags = {Tag(tag=tag) for tag in metadata.get("tags", set()) if tag}

            if self._validate_tags(tags):
                notes.append(Note(tags=tags, content=content, title=file.stem, updated_at=file.stat().st_mtime))
        return notes
