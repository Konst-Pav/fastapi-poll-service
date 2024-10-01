from typing import TYPE_CHECKING
from core.models import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from core.models import Poll


class Option(Base):
    __tablename__ = "options"

    point: Mapped[str]
    poll_id: Mapped[int] = mapped_column(ForeignKey("polls.id"))

    poll: Mapped["Poll"] = relationship(back_populates="options")
