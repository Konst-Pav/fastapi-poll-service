from pydantic import BaseModel

from core.schemas.option import OptionCreate


class ChoiceResult(BaseModel):
    option_id: int
    vote_count: int


class PollResult(BaseModel):
    poll_id: int
    result: list[ChoiceResult]
