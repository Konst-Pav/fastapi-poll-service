from pydantic import BaseModel

from core.schemas.option import OptionCreate


class PollBase(BaseModel):
    title: str
    description: str | None
    options: list[OptionCreate]


class PollCreate(PollBase):
    pass


class PollRead(PollBase):
    id: int
