from typing import TYPE_CHECKING
from core.models import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship


if TYPE_CHECKING:
    from core.models import Option


class Poll(Base):
    __tablename__ = "polls"

    title: Mapped[str]
    description: Mapped[str] = mapped_column(nullable=True)

    options: Mapped[list["Option"]] = relationship(
        back_populates="poll",
        lazy="selectin",
    )
