from typing import TYPE_CHECKING
from core.models import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from core.models import Poll, Option


class Vote(Base):
    __tablename__ = "votes"

    poll_id: Mapped[int] = mapped_column(ForeignKey("polls.id"))
    choice_id: Mapped[int] = mapped_column(ForeignKey("options.id"))
