from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, StringConstraints

from app.models.tag import Tag

NonEmptyStr = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]


class Note(BaseModel):
    title: NonEmptyStr
    content: NonEmptyStr
    tags: set[Tag]
    updated_at: datetime

    model_config = ConfigDict(frozen=True, extra="forbid")
