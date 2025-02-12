from datetime import datetime

import yaml

from app.models.tag import Tag
from app.notes_reader.loader import NotesLoader


def test_no_md_files(get_empty_dir):
    loader = NotesLoader(get_empty_dir, tags=[Tag(tag="any")])
    notes = loader.load()
    assert notes == []


def test_ignore_non_md_files(get_empty_dir):
    (get_empty_dir / "some_file.txt").write_text("Just some text", encoding="utf-8")

    loader = NotesLoader(get_empty_dir, tags=[Tag(tag="any")])
    notes = loader.load()
    assert notes == []


def test_load_single_md_file_with_matching_tag(get_files_dir):
    dir_ = get_files_dir("note_with_tag1.md")
    content = (dir_ / "note_with_tag1.md").read_text(encoding="utf-8")

    loader = NotesLoader(dir_, tags=[Tag(tag="tag1")])
    notes = loader.load()
    assert len(notes) == 1
    note = notes[0]

    assert note.title == "note_with_tag1"
    assert note.content.strip() == content.strip()
    assert note.tags == {Tag(tag="tag1")}
    assert isinstance(note.updated_at, datetime)


def test_load_single_md_file_with_non_matching_tag(get_files_dir):
    dir_ = get_files_dir("note_with_tag1.md")
    loader = NotesLoader(dir_, tags=[Tag(tag="tag2")])
    notes = loader.load()
    assert notes == []


def test_load_single_md_file_tags(get_files_dir):
    dir_ = get_files_dir("note_with_no_tags.md")
    loader = NotesLoader(dir_, tags=[Tag(tag="tag1")])
    notes = loader.load()
    assert notes == []


def test_load_multiple_md_files(get_files_dir):
    files = {"note_with_tag1.md", "note_with_tag2.md"}
    dir_ = get_files_dir(*files)
    loader = NotesLoader(dir_, tags=[Tag(tag="tag1"), Tag(tag="tag2")])
    notes = loader.load()
    assert len(notes) == len(files)


def test_load_file_yaml_error(monkeypatch, get_files_dir):
    dir_ = get_files_dir("note_with_tag1.md")

    def fake_yaml_error(*_args, **_kwargs):
        raise yaml.YAMLError("Error loading yaml")

    monkeypatch.setattr("yaml.safe_load", fake_yaml_error)

    loader = NotesLoader(dir_, tags=[Tag(tag="tag1")])
    notes = loader.load()
    assert notes == []
