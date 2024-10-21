from pydantic import BaseModel


class OptionBase(BaseModel):
    point: str


class OptionCreate(OptionBase):
    pass


class OptionRead(OptionBase):
    pass
