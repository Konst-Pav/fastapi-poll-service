from pydantic import BaseModel

from core.schemas.option import OptionCreate


class VoteBase(BaseModel):
    poll_id: int
    choice_id: int


class VoteCreate(VoteBase):
    pass
