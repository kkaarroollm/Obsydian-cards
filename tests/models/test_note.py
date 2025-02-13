import pytest
from pydantic import ValidationError

from app.models.note import Note


def test_valid_note(fake, tags):
    data = {
        "title": fake.pystr(min_chars=1, max_chars=100),
        "content": fake.pystr(min_chars=1, max_chars=1000),
        "tags": tags,
        "updated_at": fake.date_time_this_year(),
    }
    note = Note(**data)
    assert note.title == data["title"]
    assert note.content == data["content"]
    assert note.tags == data["tags"]
    assert note.updated_at == data["updated_at"]


def test_invalid_empty_title_note(fake, tags):
    with pytest.raises(ValidationError):
        Note(
            title="", content=fake.pystr(min_chars=1, max_chars=1000), tags=tags, updated_at=fake.date_time_this_year()
        )


def test_invalid_empty_content_note(fake, tags):
    with pytest.raises(ValidationError):
        Note(title=fake.pystr(min_chars=1, max_chars=100), content="", tags=tags, updated_at=fake.date_time_this_year())
