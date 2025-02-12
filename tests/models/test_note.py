import pytest

from app.models import Note


def test_empty_title_raises_error(fake):
    with pytest.raises(ValueError, match="Field must be a non-empty string."):
        Note(title="", content=fake.paragraph(nb_sentences=3), tags=set(), updated_at=fake.date_time_this_year())


def test_empty_content_raises_error(fake):
    with pytest.raises(ValueError, match="Field must be a non-empty string."):
        Note(title=fake.sentence(nb_words=6), content="", tags=set(), updated_at=fake.date_time_this_year())


def test_empty_tags_raises_error(fake):
    with pytest.raises(ValueError, match="Tags must be a non-empty set of strings."):
        Note(
            title=fake.sentence(nb_words=6),
            content=fake.paragraph(nb_sentences=3),
            tags=set(),
            updated_at=fake.date_time_this_year(),
        )


def test_tags_with_empty_string_raise_error(fake):
    with pytest.raises(ValueError, match="Tags must be a non-empty set of strings."):
        Note(
            title=fake.sentence(nb_words=6),
            content=fake.paragraph(nb_sentences=3),
            tags={"  ", " "},
            updated_at=fake.date_time_this_year(),
        )


def test_tags_are_stripped(fake, tags):
    note = Note(
        title=fake.sentence(nb_words=6),
        content=fake.paragraph(nb_sentences=3),
        tags={f" {tag} " for tag in tags},
        updated_at=fake.date_time_this_year(),
    )
    assert note.tags == tags


def test_tags_are_lowercased(fake, tags):
    note = Note(
        title=fake.sentence(nb_words=6),
        content=fake.paragraph(nb_sentences=3),
        tags={tag.upper() for tag in tags},
        updated_at=fake.date_time_this_year(),
    )
    assert note.tags == {tag.lower() for tag in tags}
