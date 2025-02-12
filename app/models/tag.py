from typing import Annotated

from pydantic import BaseModel, ConfigDict, StringConstraints

TagStr = Annotated[str, StringConstraints(pattern=r"^[a-zA-Z0-9/_-]+$", strip_whitespace=True, to_lower=True)]


class Tag(BaseModel):
    tag: TagStr

    model_config = ConfigDict(frozen=True, extra="forbid")
