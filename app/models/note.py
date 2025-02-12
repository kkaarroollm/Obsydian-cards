from datetime import datetime

from pydantic import BaseModel, field_validator


class Note(BaseModel):
    title: str
    content: str
    tags: set[str]
    updated_at: datetime

    class Config:
        frozen = True
        extra = "forbid"

    @field_validator("title", "content")
    def check_non_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError(f"{cls.__name__}: Field must be a non-empty string.")
        return value

    @field_validator("tags", mode="before")
    def clean_tags(cls, value: set[str]) -> set[str]:
        tags = {tag.strip().lower() for tag in value if tag.strip()}
        if not tags:
            raise ValueError(f"{cls.__name__}: Tags must be a non-empty set of strings.")
        return tags
