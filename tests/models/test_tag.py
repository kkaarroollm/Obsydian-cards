import pytest
from pydantic import ValidationError

from app.models.tag import Tag


@pytest.mark.parametrize(
    "valid_tag",
    [
        "valid_tag",
        "valid-tag",
        "valid/tag",
        "validTag123",
        "VALID_TAG",
    ],
)
def test_valid_tag(valid_tag):
    tag = Tag(tag=valid_tag)
    assert tag.tag == valid_tag.lower()


@pytest.mark.parametrize(
    "invalid_tag",
    [
        "Invalid Tag",
        "invalid@tag",
        "tag with spaces",
        "tag*with*asterisk",
        "tag#hash",
        "#tag_with_hash",
        "",
    ],
)
def test_invalid_tags(invalid_tag):
    with pytest.raises(ValidationError):
        Tag(tag=invalid_tag)
